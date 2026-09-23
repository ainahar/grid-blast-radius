# GridBlast — Parameterisation Guide

GridBlast needs **structural** parameters, not sensitive operational data. An
operator can populate it entirely from internal planning figures; a regulator can
use published aggregates.

## Parameters and where they come from
| Parameter | Source (non-sensitive) |
|---|---|
| households_millions | DISCOM consumer counts (published in tariff filings) |
| smart_meter_penetration | RDSS / state AMI rollout progress reports |
| vendor_shares | AMISP award announcements per state (public tenders) |
| mitigation dials | operator's own control self-assessment (0-1 each) |

## Modelling vendor concentration (the key input)
- RDSS smart-meter contracts are awarded per state/cluster to AMISPs under a
  TOTEX / DBFOOT model. Aggregating publicly-announced awards gives approximate
  national vendor shares.
- Enter shares as a tuple; GridBlast reports the implied HHI. Higher HHI =
  larger single-breach blast radius. This is the argument for vendor-diversity
  requirements as a *security* control, not just a procurement preference.

## What NOT to feed it
- No credentials, network topology, firmware versions, or live meter data.
- The model is designed to be useful with only coarse, public structure — by
  design, so it can be shared and debated openly.

## Calibrating mitigations honestly
Set each dial from a control maturity self-assessment. If you cannot evidence a
control, set it to 0. The tool's value is the *gap* between your current dials
and defence-in-depth.
