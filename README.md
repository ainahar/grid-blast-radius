# GridBlast — AMI Disconnection Blast-Radius Twin

**If one smart-meter head-end is compromised, how many households can be switched
off at once — and how much do standard defences shrink that number?**

GridBlast is a defensive digital-twin that models the *consequence surface* of
India's RDSS smart-meter rollout. It contains **no attack technique and no
exploit code.** It is a Monte-Carlo consequence model an operator, CERT, or
regulator uses to size a risk that the current policy debate ignores.

> Strategic Intelligence Forecast **F4 — "The Disconnection API."**
> The RDSS rollout is installing *remotely-executable mass household
> disconnection* across state DISCOMs, concentrated in a handful of private AMI
> Service Providers (AMISPs) running head-end systems. Public debate is entirely
> about billing fairness. Almost none of it is about the fact that a compromised
> head-end can de-energise lakhs of homes simultaneously — an IT-grade security
> problem with OT-grade, household-granular consequences.

---

## Why this is neglected, not obvious

Everyone can see the smart-meter *billing* fight (prepaid protests, rollbacks).
The security conversation, where it exists, is about data privacy. The
**disconnection command path** — a switch that reaches into homes — is discussed
almost nowhere, and its blast radius is set by a variable no one is tracking:
**vendor market concentration.** GridBlast makes that variable legible.

## What it does

Runs a Monte-Carlo over structural parameters — household base, rollout
penetration, AMISP vendor shares (concentration), and four composable OT
mitigations — and reports the distribution of households a single head-end breach
could disconnect. It compares four canonical scenarios side by side.

## Quickstart

```bash
pip install -r requirements.txt
python src/ami_twin.py
```

Produces `assets/blast_radius.png` and `assets/summary.json`.

## Real (illustrative) output

Running the shipped model on generic structural parameters:

| Scenario | Mean (M households) | P95 (M) | % of state |
|---|---|---|---|
| Baseline (mid rollout, concentrated, no controls) | 1.25 | 1.91 | 14.9% |
| Full rollout, no controls | 2.28 | 3.48 | 27.1% |
| Basic OT hygiene (segmentation + rate-limit) | 0.27 | 0.42 | 3.3% |
| Defence-in-depth (all four controls) | 0.05 | 0.08 | 0.7% |

**The headline:** concentration + full rollout with no OT controls puts a
double-digit percentage of a state's households inside a single-breach blast
radius. Layered controls collapse it *multiplicatively* — the case for mandating
them before, not after, full deployment. (Numbers are illustrative; the point is
the shape and the sensitivity, which an operator reproduces with their own inputs.)

## Repository layout

```
grid-blastradius/
├── README.md
├── LICENSE
├── requirements.txt
├── src/
│   └── ami_twin.py            # Monte-Carlo consequence model + scenario grid
├── docs/
│   ├── ARCHITECTURE.md        # MVP + system design
│   ├── DATA_SOURCES.md        # what to substitute for real parameters
│   ├── POLICY_BRIEF.md        # brief for CERT-In / NCIIPC / MoP / SERCs
│   ├── ROADMAP.md             # 12-week build + beyond
│   └── THOUGHT_LEADERSHIP.md  # X thread + LinkedIn article
└── assets/
    ├── blast_radius.png
    ├── summary.json
    └── infographic.svg
```

## Responsible-use boundary

GridBlast models **outcomes, not intrusions.** It does not describe how to
compromise a head-end, does not identify real vendors or DISCOMs, and ships only
synthetic structural parameters. Its purpose is to help defenders and regulators
prioritise segmentation, disconnect-command controls, and vendor-diversity
requirements. Use it to argue for defences, not to plan attacks.

## Primary stakeholders

CERT-In, NCIIPC, Ministry of Power, State Electricity Regulatory Commissions
(SERCs), and DISCOM / AMISP security teams.

*MIT licensed. Synthetic parameters only. Defensive concept demonstrator.*
