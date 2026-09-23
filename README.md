# Grid Blast Radius — AMI Disconnection Consequence Model

**If one smart-meter head-end were compromised, how many households could be switched off at once — and how much do standard defences reduce that number?**

Grid Blast Radius is a defensive digital twin that models the *consequence surface* of India's RDSS smart-meter rollout. It contains **no attack technique and no exploit code.** It is a Monte-Carlo consequence model for operators, regulators and CERTs to size a risk that the current policy debate does not address.

> **Forecast F4 — "The Disconnection Blast Radius."**
> The RDSS rollout is installing the ability to remotely de-energise households at national scale, concentrated in a small number of private AMI Service Providers running head-end systems. Public debate about smart meters is about prepaid billing. It is not about the fact that a compromised head-end can switch off a large share of a state's households at once, which is an IT-security problem with physical, household-level consequences.

---

## Why this is neglected

The smart-meter billing argument is well covered, including prepaid protests and rollbacks. The security conversation, where it exists, is about data privacy. The **disconnect command path** is discussed almost nowhere, and the variable that sets its reach is not tracked at all: **vendor market concentration.** This model makes that variable visible.

## What it does

Runs a Monte-Carlo over structural parameters — household base, rollout penetration, AMISP vendor shares, and four composable operational-technology controls — and reports the distribution of households a single head-end compromise could disconnect. Four scenarios are compared side by side.

## Quickstart

```bash
pip install -r requirements.txt
python src/ami_twin.py
```

Produces `assets/blast_radius.png` and `assets/summary.json`.

## Results

> **These figures are illustrative.** They come from generic structural parameters, not from any real distribution company, vendor or deployment. The point is the *shape and sensitivity* of the result, which any operator can reproduce with their own numbers. No real system is assessed here.

| Scenario | Mean (M households) | P95 (M) | % of state |
|---|---|---|---|
| Baseline (mid rollout, concentrated, no controls) | 1.25 | 1.91 | 14.9% |
| Full rollout, no controls | 2.28 | 3.48 | 27.1% |
| Basic OT hygiene (segmentation + rate-limit) | 0.27 | 0.42 | 3.3% |
| Defence-in-depth (all four controls) | 0.05 | 0.08 | 0.7% |

**What the model shows:** concentration plus full rollout with no dedicated controls places a double-digit percentage of a state's households within a single-compromise reach. Layered controls reduce it *multiplicatively*, because each control removes a share of what the previous one left. That is the case for requiring them before deployment is complete rather than after.

## Repository layout

```
grid-blast-radius/
├── README.md
├── LICENSE
├── requirements.txt
├── src/
│   └── ami_twin.py            # Monte-Carlo consequence model + scenario grid
├── docs/
│   ├── ARCHITECTURE.md        # MVP and system design
│   ├── DATA_SOURCES.md        # how to substitute real parameters
│   ├── POLICY_BRIEF.md        # brief for CERT-In / NCIIPC / MoP / SERCs
│   ├── POLICY_BRIEF.pdf       # same brief, formatted
│   └── ROADMAP.md             # phased build plan
└── assets/
    ├── blast_radius.png
    ├── summary.json
    └── infographic.svg
```

## Responsible use

This model describes **outcomes, not intrusions.** It does not explain how to compromise a head-end system, does not identify real vendors or distribution companies, and ships only synthetic structural parameters. Its purpose is to help defenders and regulators prioritise segmentation, disconnect-command controls and vendor-diversity requirements, and to let an operator demonstrate that its own exposure is small.

## Primary stakeholders

CERT-In, NCIIPC, Ministry of Power, State Electricity Regulatory Commissions, and DISCOM and AMISP security teams.

*MIT licensed. Synthetic parameters only. Defensive concept demonstrator.*
