# GridBlast — MVP & Software Architecture

## Design goal
A regulator or DISCOM security lead drops in their own numbers and gets a
defensible blast-radius estimate and a mitigation-value ranking in minutes. No
live-system access, ever.

## MVP scope (12 weeks)
- Single-vendor breach base case + correlated multi-vendor extension.
- Four composable OT mitigations with multiplicative residual model.
- Four canonical scenarios; PNG + JSON outputs.

## Model structure
```
StateConfig (households, penetration, vendor_shares, 4 mitigation dials)
        │
        ▼
Monte-Carlo (n sims)
  ├─ target head-end ~ vendor footprint      (bigger base = bigger target)
  ├─ reachable = meters_under_vendor
  │              x (1 - combined_mitigation)  (defence-in-depth multiplies)
  │              x operational_friction        (not every meter answers)
        │
        ▼
Distribution -> mean / P50 / P95 / max / % of state -> chart + summary.json
```

## Why these are the right knobs
| Knob | Why it dominates blast radius |
|---|---|
| vendor_shares (HHI) | one breach = one vendor's whole footprint; concentration IS the risk |
| penetration | rollout stage linearly scales exposed meters |
| network_segmentation | caps how much of a footprint one HES can reach |
| disconnect_rate_limit | throttles a mass-disconnect into a slow, detectable trickle |
| command_signing | forces authorised orders; blocks forged mass commands |
| anomaly_detection | auto-halts a sweep before completion |

## Mitigations compose multiplicatively
Defence-in-depth removes a *fraction of what the previous control left*, not an
additive share. This is the honest OT model and it is why layering four modest
controls (0.5-0.7 each) collapses the blast radius by >90%.

## Extensions (documented, staged)
- Correlated multi-vendor breach (shared component / supply-chain compromise).
- Time-to-detect vs time-to-full-sweep race model.
- Cascading load/grid-stability coupling (a research-grade add-on).

## Non-goals / guardrails
- No intrusion modelling, no CVEs, no vendor names, no DISCOM identification.
- Outputs are planning aids, not threat intelligence about any real entity.
