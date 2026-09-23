"""
ami_twin.py — Advanced Metering Infrastructure (AMI) blast-radius digital twin.

Forecast F4 ("The Disconnection API"): India's RDSS smart-meter rollout is
installing remotely-executable mass household disconnection capability across
state DISCOMs, concentrated in a handful of private AMI Service Providers
(AMISPs) running head-end systems (HES). Policy debate is about billing
fairness; almost none is about the fact that a compromised HES can switch off
lakhs of households at once.

This module models the *consequence surface*, not any attack technique. It
answers one question a CERT / NCIIPC / SERC analyst actually asks:

    "If one head-end is compromised, how many households can be
     simultaneously disconnected — and how much do standard OT
     mitigations shrink that number?"

No live infrastructure, no exploit code, no vendor identification. Pure
Monte-Carlo over published-style structural parameters. Everything here is
synthetic and illustrative.

Run:  python -m src.ami_twin  (or python src/ami_twin.py)
Output: assets/blast_radius.png, assets/summary.json
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict

import numpy as np


# --------------------------------------------------------------------------- #
# Structural parameters. These are deliberately generic and editable — the
# point of a digital twin is that an operator drops in their OWN numbers.
# --------------------------------------------------------------------------- #
@dataclass
class StateConfig:
    name: str = "ModelState"
    households_millions: float = 8.4          # ~ order of a mid-size DISCOM cohort
    smart_meter_penetration: float = 0.55     # fraction on AMI (rollout-stage)
    # Vendor market shares among AMISPs (must sum ~1). Concentration is the
    # single most important blast-radius driver, so it is a first-class input.
    vendor_shares: tuple = (0.42, 0.28, 0.18, 0.12)

    # --- Mitigation controls (each in [0,1] = fraction of blast radius removed)
    network_segmentation: float = 0.0         # HES cannot reach every meter cluster
    disconnect_rate_limit: float = 0.0        # command throttling on mass-disconnect
    command_signing: float = 0.0              # signed/authorised disconnect orders
    anomaly_detection: float = 0.0            # detection+auto-halt before full sweep

    n_sims: int = 20000
    seed: int = 7


@dataclass
class ScenarioResult:
    label: str
    mean_households: float
    p50_households: float
    p95_households: float
    max_households: float
    pct_of_state: float
    params: dict = field(default_factory=dict)


def _hhi(shares) -> float:
    """Herfindahl-Hirschman Index of vendor concentration (0..1)."""
    s = np.asarray(shares, dtype=float)
    return float(np.sum((s / s.sum()) ** 2))


def _combined_mitigation(cfg: StateConfig) -> float:
    """
    Mitigations compose multiplicatively on the *residual* blast radius.
    Each control removes a fraction of what the previous ones left. This is
    the honest OT model: defence-in-depth multiplies, it does not add.
    """
    residual = 1.0
    for m in (
        cfg.network_segmentation,
        cfg.disconnect_rate_limit,
        cfg.command_signing,
        cfg.anomaly_detection,
    ):
        residual *= (1.0 - float(np.clip(m, 0.0, 1.0)))
    return 1.0 - residual  # fraction removed


def simulate(cfg: StateConfig) -> ScenarioResult:
    rng = np.random.default_rng(cfg.seed)
    shares = np.asarray(cfg.vendor_shares, dtype=float)
    shares = shares / shares.sum()

    total_meters = cfg.households_millions * 1e6 * cfg.smart_meter_penetration
    meters_per_vendor = total_meters * shares

    removed = _combined_mitigation(cfg)

    # Each simulation: adversary compromises ONE head-end (single-vendor breach
    # is the base case; correlated multi-vendor breaches are a separate call).
    # Which vendor is hit is weighted by attack surface ~ vendor footprint,
    # because a bigger installed base is a bigger, more-probed target.
    attack_weights = shares  # proportional-to-footprint targeting
    hit_vendor = rng.choice(len(shares), size=cfg.n_sims, p=attack_weights)

    # Reachable meters under the hit head-end, minus mitigation, minus a
    # stochastic "operational friction" factor (not every meter answers a
    # disconnect in the attack window).
    friction = rng.beta(9, 1, size=cfg.n_sims)  # ~0.9 mean, heavy toward 1
    reachable = meters_per_vendor[hit_vendor] * (1.0 - removed) * friction

    return ScenarioResult(
        label=cfg.name,
        mean_households=float(reachable.mean()),
        p50_households=float(np.percentile(reachable, 50)),
        p95_households=float(np.percentile(reachable, 95)),
        max_households=float(reachable.max()),
        pct_of_state=float(reachable.mean() / (cfg.households_millions * 1e6) * 100),
        params={
            "hhi": round(_hhi(shares), 3),
            "penetration": cfg.smart_meter_penetration,
            "mitigation_removed_pct": round(removed * 100, 1),
        },
    )


def scenario_grid() -> list[ScenarioResult]:
    """Four canonical scenarios an analyst compares side by side."""
    out = []

    # 1. Baseline: mid rollout, concentrated market, NO mitigations.
    out.append(simulate(StateConfig(name="Baseline (no controls)")))

    # 2. Full national rollout, same market — shows the rollout-stage multiplier.
    out.append(simulate(StateConfig(
        name="Full rollout (no controls)", smart_meter_penetration=1.0)))

    # 3. Basic OT hygiene: segmentation + rate-limit only.
    out.append(simulate(StateConfig(
        name="Basic OT hygiene", smart_meter_penetration=1.0,
        network_segmentation=0.6, disconnect_rate_limit=0.7)))

    # 4. Defence-in-depth: all four controls.
    out.append(simulate(StateConfig(
        name="Defence-in-depth", smart_meter_penetration=1.0,
        network_segmentation=0.6, disconnect_rate_limit=0.7,
        command_signing=0.5, anomaly_detection=0.6)))

    return out


def main() -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(here, "assets")
    os.makedirs(assets, exist_ok=True)

    results = scenario_grid()

    # ---- chart -----------------------------------------------------------
    labels = [r.label for r in results]
    p95 = [r.p95_households / 1e6 for r in results]      # millions
    mean = [r.mean_households / 1e6 for r in results]

    fig, ax = plt.subplots(figsize=(9, 5))
    y = np.arange(len(labels))
    ax.barh(y, p95, color="#c1440e", alpha=0.35, label="P95 (bad-day) households")
    ax.barh(y, mean, color="#c1440e", label="Mean households disconnected")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Households simultaneously disconnectable (millions)")
    ax.set_title("F4 — AMI head-end compromise: modelled blast radius\n"
                 "(single-vendor breach, illustrative structural parameters)")
    for i, r in enumerate(results):
        ax.text(p95[i] + 0.02, i, f"{r.pct_of_state:.1f}% of state",
                va="center", fontsize=8, color="#333")
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    fig.savefig(os.path.join(assets, "blast_radius.png"), dpi=140)

    # ---- machine-readable summary ---------------------------------------
    summary = {
        "note": "Synthetic structural model. No real vendor or DISCOM data.",
        "scenarios": [asdict(r) for r in results],
        "headline": (
            "Concentration + full rollout with no OT controls yields the "
            "largest single-breach blast radius; layered controls collapse it "
            "multiplicatively."
        ),
    }
    with open(os.path.join(assets, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # ---- console ---------------------------------------------------------
    print(f"{'Scenario':<32}{'mean (M)':>10}{'P95 (M)':>10}{'% state':>10}")
    for r in results:
        print(f"{r.label:<32}{r.mean_households/1e6:>10.2f}"
              f"{r.p95_households/1e6:>10.2f}{r.pct_of_state:>9.1f}%")
    print("\nWrote assets/blast_radius.png and assets/summary.json")


if __name__ == "__main__":
    main()
