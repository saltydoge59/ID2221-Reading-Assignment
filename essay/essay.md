# Moving power is not the same as cutting carbon: a critical reading of Google's carbon-aware computing system

**[Your full name]** · ID2221 Data-Intensive Computing, KTH, HT26 · Reading assignment

**Paper:** A. Radovanović et al., "Carbon-Aware Computing for Datacenters," *IEEE Transactions on Power Systems*, vol. 38, no. 2, pp. 1270-1280, 2023.

## The problem

The carbon cost of a kilowatt-hour depends on when and where it is used. A grid running on solar at midday and on gas in the evening emits very different amounts of CO2 for the same load. Cluster schedulers like Google's Borg ignore this: they start a job as soon as machines are free. The authors, all Google engineers, argue that this wastes an opportunity. Datacenters use about 1% of the world's electricity, and datacenter workloads grew more than sixfold between 2010 and 2018. Much of that work is not urgent. Google's internal batch jobs (data compaction, machine learning, simulation, video processing) only have to finish within 24 hours. If they run when the local grid is cleaner, the same computation should emit less. The authors also care about peak power, because datacenters are built for their peak, and a flatter load means fewer new buildings.

## The approach

The Carbon-Intelligent Computing System (CICS) leaves Borg's scheduling logic alone. Once a day it computes a *Virtual Capacity Curve* (VCC) for every cluster: 24 hourly caps on how much CPU the lowest-priority, delay-tolerant work may reserve. Borg's admission controller treats the VCC as the cluster's capacity, so when the cap is low, flexible jobs wait in the queue. User-facing services (Search, Maps, YouTube) and Google Cloud customers' virtual machines count as inflexible and are never delayed.

Daily pipelines feed the optimizer three inputs: forecasts of each cluster's next-day inflexible and flexible usage, a piecewise-linear model mapping CPU usage to power (under 5% error for over 95% of power domains), and hourly *average* carbon-intensity forecasts from Tomorrow (electricityMap). The optimizer chooses the hourly shape that minimises a weighted sum of expected carbon footprint and daily peak power, priced in $/kg CO2e and $/MW. Its main constraint is that total flexible usage over the day is unchanged, so work is moved rather than dropped. Capacity is set at the 97th percentile of forecast demand, so flexible work should miss its daily quota no more than about one day a month, and a cluster that keeps hitting its cap is left unshaped for a week.

The paper shows single clusters where the VCC cut flexible load by about 50% during the dirtiest hours, lowering power by roughly 8% for six hours in one cluster, for three hours in another, and not at all in a third where flexible load was small. A randomised experiment on one campus, in which each cluster was shaped or left alone each day with probability 0.5, found that average cluster power fell by 1-2% during the highest-carbon hours.

## Critical reflection

I agree with the systems design. Turning the carbon goal into a capacity signal, instead of writing a new scheduler, is the right choice for Borg, which makes hundreds of thousands of placement decisions per second: the real-time path stays cheap and the planning pipelines can fail without taking scheduling down. Planning on aggregate daily demand, which is predictable, rather than individual job arrivals, which are not, is also sound. The randomised experiment in production is stronger evidence than the trace-driven simulations common in this area, and the authors put the modest 1-2% in their conclusion rather than the 8% from their best cluster.

I disagree with the conclusion that the system reduces Google's carbon emissions, because the paper never measures that. There is no result in kilograms of CO2. The authors write that computing carbon impact from their power and intensity data "does not necessarily yield the correct result" and defer it to future work. The choice of signal makes this gap serious. Average intensity describes the grid mix at an hour. It does not say which power plant actually ramps up or down when Google moves load, and that marginal plant determines the real change in emissions. The authors concede that the right grid signal "requires further research". What the paper demonstrates is that Google can move power in time. Whether that cuts emissions, and by how much, remains open.

The experiment itself has a weakness the authors partly acknowledge. In their campus-level figure (Fig. 12) the shaped clusters draw less power than the unshaped ones for nearly the whole day, including the low-carbon evening hours when delayed work should come back. The authors explain that under aggressive shaping some flexible jobs "choose" to move to other clusters, and that this spontaneous shift "may increase or decrease carbon emissions". If some of that work landed in control clusters on the same campus, the measured 1-2% overstates the effect. If it landed somewhere dirtier, the carbon saving could be smaller still.

The ceiling is also low by design. The conservation constraint means total energy is never reduced, only rearranged. Google keeps all working machines switched on, so idle machines still draw power while work waits. Cloud customers' workloads are excluded entirely. Independent research points the same way: Sukprasert et al. (EuroSys 2024), using carbon data from 123 regions, find that the practical gains of temporal and spatial shifting are limited and will shrink as grids decarbonise.

Finally, the paper shows why D'Ignazio and Klein's call to *examine power* matters for data platforms. Google decides which work counts as "flexible", sets the internal price of carbon against the price of peak power, picks the metric, runs the experiment on its own fleet, and publishes normalised curves with no absolute numbers. No outsider can check any of it. The objective function also shows that carbon is pursued where it pays: the authors note that optimising for carbon alone would require more machines, so carbon is traded against infrastructure cost. That is a reasonable business decision, but it makes CICS an efficiency system with a carbon benefit attached rather than a climate measure. Crawford's *Atlas of AI* argues that the "cloud" has a material footprint well beyond electricity, and this paper's accounting leaves out hardware manufacturing and water. A 1-2% cut at peak hours is small next to sixfold demand growth, and calling that growth "carbon-intelligent" makes it easier to defend.

My position is that CICS is a solid systems contribution and a reasonable first step, but the claim that it advances Google's environmental goals is asserted rather than shown. A stronger paper would report estimated avoided emissions under both average and marginal signals with uncertainty bounds, track where displaced jobs went, and release anonymised traces so others could check the result. The design also suggests a fairer extension: let Cloud customers opt in to flexible scheduling, so the people paying for compute can choose to trade latency for lower emissions.

## References

1. A. Radovanović et al., "Carbon-Aware Computing for Datacenters," *IEEE Trans. Power Systems*, 38(2):1270-1280, 2023. doi:10.1109/TPWRS.2022.3173250. Preprint: arXiv:2106.11750.
2. T. Sukprasert, A. Souza, N. Bashir, D. Irwin, P. Shenoy, "On the Limitations of Carbon-Aware Temporal and Spatial Workload Shifting in the Cloud," *EuroSys 2024*. doi:10.1145/3627703.3650079.
3. A. Verma et al., "Large-scale cluster management at Google with Borg," *EuroSys 2015*.
4. C. D'Ignazio and L. F. Klein, *Data Feminism*, MIT Press, 2020.
5. K. Crawford, *Atlas of AI*, Yale University Press, 2021.
