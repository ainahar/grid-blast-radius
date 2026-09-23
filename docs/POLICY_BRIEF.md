# Grid Blast Radius: Policy & Technical Brief

## Executive Insight
**Title:** Grid Blast Radius — Sizing the Disconnection Reach of India's Smart-Meter Rollout
**Author:** Samriddhi Nahar
**Date:** September 2026

## Overview
India's smart-meter rollout under RDSS is installing something the public debate has not discussed. Every meter can be disconnected remotely, by design, because that is how prepaid metering works. Those commands are issued from head-end systems, and in most states a small number of private AMI Service Providers run them. The public argument about smart meters is about billing and prepaid tariffs. The question underneath it is different. If one head-end system were compromised, how many households could be switched off at once? This brief proposes that the answer be modelled openly, before the rollout is complete, and treated as a governance measure rather than a technical afterthought.

## Mechanism — How the Blast Radius Forms
The exposure is created by ordinary procurement and deployment decisions, not by any single technical flaw.

1. **Remote disconnection is a designed feature.** Prepaid metering requires it, so every meter in the fleet accepts a disconnect command.
2. **Commands are centralised.** Those commands are issued from a head-end system that manages a large population of meters.
3. **Operation is concentrated.** A few AMI Service Providers run head-end systems across most of a state's meters.
4. **One breach reaches one vendor's footprint.** The number of households exposed is set by that vendor's market share.
5. **Consequences are physical and household-granular.** Loss of power in a home is not a data-privacy harm. It is a direct physical effect on a household.

**Why this matters.** The size of the exposure is decided by vendor market concentration, which is a procurement outcome, not by the sophistication of any attacker. Concentration is therefore a security variable, and it is currently treated as a commercial one.

## Policy & Technical Recommendations
### Policy
- **Treat the disconnect command path as safety-critical.** Govern it separately from billing and data security, with its own requirements.
- **Set a per-state ceiling on disconnection reach.** Define the maximum share of households any single head-end may address, and require architectures to meet it through segmentation, vendor diversity, or both.
- **Treat vendor diversity as a security requirement.** A fragmented provider market caps the reach of any single compromise. A concentrated one removes the cap.
- **Require a consequence model as an assurance document.** Ask operators to submit their own blast-radius modelling to the state regulator, using their own parameters.

### Technical
- **Network segmentation.** Limit how much of a fleet one head-end system can address.
- **Rate-limiting on mass disconnection.** Convert an instantaneous sweep into a slow and detectable sequence.
- **Authorised disconnect commands.** Require commands to be signed, so forged instructions fail.
- **Anomaly-triggered halt.** Stop an unusual disconnection pattern automatically before it completes.

Controls of this kind compose multiplicatively. Each removes a share of what the previous one leaves, which is why four moderate controls reduce the modelled exposure by more than ninety percent.

## Deployment & Prototype
### Pilot Model
- **Phase 1.** One state models its own exposure using published consumer counts, rollout progress and vendor award data.
- **Phase 2.** The state regulator reviews the model alongside the operator's control self-assessment, and sets a target ceiling.
- **Phase 3.** Consequence modelling becomes a standard, shareable assurance document for AMI security across states.

### Technical Stack Overview
- **Pipeline.** Structural parameters, meaning household base, rollout penetration, vendor shares and control maturity, feed a Monte-Carlo consequence model that reports the distribution of households reachable in a single-vendor compromise.
- **Integration.** CERT-In, NCIIPC, Ministry of Power, State Electricity Regulatory Commissions, and DISCOM and AMISP security teams.

### Responsible Use
This is a consequence model. It describes outcomes, not intrusions. It contains no attack technique, identifies no real vendor or distribution company, and runs on synthetic parameters. It exists to help defenders and regulators prioritise controls, and to let an operator demonstrate that its exposure is small.

---

**Prototype Repository:** github.com/ainahar/grid-blast-radius
**Author:** Samriddhi Nahar
**Contact:** ainaharx@gmail.com | AI • Cyber • Policy Foresight
**Version:** 1.0 — Public Policy Brief
**Status:** Defensive concept demonstrator. Synthetic parameters. Not an assessment of any real system.
