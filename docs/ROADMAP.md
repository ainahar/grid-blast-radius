# GridBlast — Implementation Roadmap

## Phase 0 — Framing (week 0)
- Publish the threat-model boundary first: consequence modelling, not intrusion.
  This keeps the project unambiguously defensive and shareable.

## Phase 1 — MVP (weeks 1-4)
- Monte-Carlo consequence model + four scenarios (implemented).
- HHI reporting; sensitivity sweeps over penetration and concentration.
- Brief-ready chart + JSON.

## Phase 2 — Realism (weeks 5-8)
- Correlated multi-vendor breach (supply-chain / shared-component case).
- Detect-vs-sweep race model: does anomaly detection halt a mass disconnect in time?
- Parameter presets from published RDSS award aggregates (per state).

## Phase 3 — Decision support (weeks 9-12)
- Interactive dial UI (sliders for penetration, shares, mitigations).
- Mitigation-value ranking: marginal blast-radius reduction per control, for
  investment prioritisation.
- Regulator template: "minimum OT controls before X% penetration."

## Beyond 12 weeks
- Couple to a simple grid-stability model (mass disconnect -> frequency effects).
- Contribute an anonymised parameter library so states can benchmark concentration.
- Feed a proposed SERC security-conditions checklist for AMISP contracts.

## Success criteria
- A regulator can state, with a defensible model, the blast radius at current
  concentration and the minimum controls that bring it under a target threshold.
