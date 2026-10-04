# Research notes

Background for the essay and the video. Page numbers refer to the arXiv preprint (arXiv:2106.11750v1, 14 pages), which is the version I read. The published IEEE version has different page numbers and may differ slightly in wording, so check quotes against it if you can get it through the KTH library.

## Why this paper qualifies

- Published in IEEE Transactions on Power Systems, vol. 38, no. 2, March 2023 (DOI 10.1109/TPWRS.2022.3173250). That is inside the five-year window. The arXiv preprint is from June 2021, which is just outside it, so cite the journal version.
- Data-intensive platforms: it is built on Borg, and the jobs it delays are MapReduce and Flume pipelines (p. 4). Both are course topics.
- Environmental issue: datacenter carbon emissions.

## Facts used, with sources

| Claim | Where |
|---|---|
| Datacenters use about 1% of global electricity; workloads grew more than 6x from 2010 to 2018 | p. 1 (citing Masanet et al., Science 2020) |
| Flexible work must finish within 24 hours; examples are compaction, ML, simulation, video processing | p. 1 |
| User-facing services and Cloud customers' VMs are inflexible and not affected | p. 1 |
| Borg makes hundreds of thousands of placement decisions per second | p. 4 |
| All available machines are typically on unless broken | p. 4 |
| Flexible = lower-tier batch jobs; daily computation must be preserved | p. 4 |
| VCC = hourly limit; Borg uses it to compute CPU availability for flexible jobs, which queue | p. 5 |
| Design principle "User Impact Fairness": delayed users should be affected in an unbiased way | p. 5 |
| Carbon forecasts are hourly *average* intensity from Tomorrow (electricityMap) | p. 6, p. 9 |
| A cluster that keeps missing its daily flexible demand is left unshaped for a week | p. 6 |
| Power model error (MAPE) under 5% for over 95% of power domains | p. 7 |
| SLO: daily flexible capacity violated at most about one day per month (about 0.03 probability); capacity at 97th percentile | p. 9 |
| Tomorrow forecast error (MAPE) 0.4% to 26% across locations and horizons of 8 to 32 hours | p. 9 |
| Objective: λe × carbon ($/kg CO2e) + λp × peak power ($/MW/day) | p. 9, eq. (4) |
| Conservation constraint Σδ = 0 (daily flexible usage unchanged) | p. 10 |
| A carbon-only objective could increase the machine capacity needed | p. 10 |
| "the choice of the most effective grid-level signal requires further research" | p. 10 |
| Cluster X: VCC drops flexible load by about 50%, power down about 8% for 6 hours | p. 11 |
| Cluster Y: about 8% drop but only 3 hours (forecast uncertainty pushes VCC up) | p. 11 |
| Cluster Z: no meaningful change (flexible load small relative to inflexible) | p. 12 |
| About 10% of clusters are not shaped on a given day (too full, or not enough data) | p. 12 |
| Randomised experiment: each cluster shaped or not each day with probability 0.5, two months from 12 Feb 2021 | p. 12 |
| Result: average cluster power down 1-2% during the highest-carbon hours | p. 12, p. 13 |
| Under aggressive shaping, daily flexible usage falls slightly; some jobs "choose" to move to other clusters; this "may increase or decrease carbon emissions" | p. 12 |
| Computing carbon impact from power and intensity data "does not necessarily yield the correct result"; left for future research | p. 12 |
| Spatial shifting is planned future work | p. 12, p. 13 |

## Things I noticed that the essay does not have room for

- The text on p. 12 refers to "Figure 13" for the campus experiment, but the figure is numbered Fig. 12, and its caption says the data covers 1 month while the text says two months. This is a small editing slip in the preprint. Check whether the journal version fixes it before mentioning it.
- The paper says the experiment was run on "a single Google datacenter campus" (Fig. 12 caption), so the 1-2% is one campus, not the fleet.
- The authors note that grid operators could benefit by as much as EUR 1B per year from datacenter flexibility (p. 1, citing an EPEX SPOT report). This is a claim about potential, not something CICS measured.
- The paper itself mentions Microsoft's carbon-aware Kubernetes work, which uses *marginal* intensity (p. 3). This is useful if anyone asks whether marginal signals are practical.

## The counter-paper

Sukprasert, Souza, Bashir, Irwin and Shenoy, "On the Limitations of Carbon-Aware Temporal and Spatial Workload Shifting in the Cloud", EuroSys 2024, DOI 10.1145/3627703.3650079. I could only reach the abstract and search summaries, not the full text, so the essay uses only claims from the abstract:

- carbon intensity data from 123 regions covering most major cloud sites
- analyses batch and interactive workloads
- practical upper bounds on carbon reductions from shifting are limited and far from ideal
- the benefit relative to carbon-agnostic scheduling decreases as the grid gets greener

Read at least the introduction and conclusion before recording, in case you want to quote a specific number.

## Course connections

- Borg and resource management (Sep 30 lecture): VCCs work through Borg's admission control and priority tiers.
- MapReduce and batch processing: the flexible jobs are batch pipelines.
- Data Feminism, "examine power" (chapter 1): who defines "flexible", who sets the carbon price, who can verify results.
- Atlas of AI: the material footprint of computing goes beyond electricity (hardware, water). The paper's accounting is electricity only.
- Deck 01's alternative models (Sustainability-as-a-Service, community and commons clouds) fit the "let customers opt in" suggestion if you want to say more in the video.

## Before submitting

- [ ] Put your full name in the essay header and on slide 1.
- [ ] If you can get the IEEE version through KTH, check that the quotes and the 1-2% figure match it.
- [ ] Skim the Sukprasert et al. paper (see above).
- [ ] Check whether the course wants *Data Feminism* cited as 2020 (first edition) or a later printing.
- [ ] Rebuild the PDF after any edits: `python3 build/build_pdf.py essay/essay.md`, and check it is still 2 pages.
