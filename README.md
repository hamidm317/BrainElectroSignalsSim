# Brain Electrophysiological Signals Simulator

This repository aims to provide a set of tools to test and debug EEG analyzing Tools, the most beneficial points are,
- Consideration of a brain-like generating sources and sensor that simulates a real common source effect,
- Possiblity to handle the connected sources in different senses,
- Future versions will be helpful to examine the "General" Source Localization / BSS Methods.

it must be noted that this project is UNDER CONSTRUCTION!

The main parts will be explained subsequently. (UC mark indicates the Under Construction parts)

## Source Properties

It is possible to define a set of sources (1 < N < 21 up to now) that each one (or each group of sources) generate signals as user defined. (1. N source and N clusters, 2. N sources and M (<N) clusters)

These sources are placed on arbitrary points in a sphere, but default allocation is uniformly random in a sphere. Other than random user must define the source locations.

Sources may fluctuate independently ('default') or dependently. The latter requires defining the CLUSTERS of co-fluctuating sources and CONNECTION that cluster members have.

### Simple Generating Functions

The Generating Functions are listed below and will be updated gradually:

- 'WGN': Simple white Gaussian Noise ('default')
- 'SingleTone': Single Frequency Signal (may be noisy or not)
- 'CGN': Color(ful?) Gaussian Noise (filtered WGN)
- 'RandomlySmoothSpiking': A Correlated Randomly Spiking Stochastic Process with given time constants (may be noisy) (may be used for ERP Analysis)
- 'AutoRegressive': Autoregressive process (very sensitive to parameters and must be bounded to threshold)

### Connections

The possible Connections (as I remember :)) are listed below, and will be updated gradually:

- 'ASBC': All Spectral Bands Coupling
- 'SSBC': Same Spectral Band Coupling
- 'CSBC': Cross Spectral Bands Coupling

General Connection Parameters (CPs) are:

- 'Randomness': 'Stochastic' or 'Deterministic'
- 'Delay': 0 -> No lag and int values -> Number of lag in samples
- 'BandCorrelation': Only possible to be applied on SSBC and CSBC
- 'CouplingSpecs':

  - 'A2A': Amplitude of First Signal to Second One's
  - 'A2P': Amplitude of First Signal to Second One's Phase
  - 'P2P': Phase of First Signal to Second One's
  - 'P2A': Phase of First Signal to Second One's Amplitude

 More details is provide in related module folders. (IDK Where now!)

## Sensor Properties

Something about sensor properties will be left here, soon ...

## Head Properties

Same as above.
