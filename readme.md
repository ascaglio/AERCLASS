<p align="center">
  <img src="/docs/images/logo.png" width="200"><br>
  <em>Uncertainty-aware aerosol classification from optical observations</em>
</p>

**Aerosol Classification & Uncertainty Analysis Toolkit**

AERCLASS is an open-source Python package designed to apply widely used
**two-dimensional aerosol classification schemes** and quantify the
impact of **measurement uncertainties** on classification results.

The package provides a unified framework to evaluate how uncertainties
in aerosol optical properties propagate into **aerosol type
identification**, supporting more robust interpretation of atmospheric 
observations.

AERCLASS was developed primarily for atmospheric research using
**AERONET** data but can be applied to any dataset providing the
required optical variables.

------------------------------------------------------------------------

## Why AERCLASS?

Aerosol classification schemes are widely used to infer dominant aerosol
types from optical observations. These approaches typically rely on
threshold-based relationships between variables such as aerosol optical
depth (AOD), Ångström exponent (EAE), single scattering albedo (SSA),
refractive index, among others.

However, the **uncertainty associated with these measured or computed 
variables is rarely propagated into the classification itself**. As a 
result, aerosol type assignments may appear deterministic even when the 
underlying measurements contain significant uncertainty.

AERCLASS addresses this gap by providing tools to:

-   apply multiple aerosol classification schemes within a consistent
    framework
-   propagate measurement uncertainties to classification outcomes
-   estimate **misclassification rates (MR)** associated with each
    aerosol type
-   visualize classification regions and uncertainty boundaries

This allows researchers to **evaluate the robustness of aerosol
classification results** and compare the sensitivity of different
methods.

------------------------------------------------------------------------

## Key Features

-   Implementation of **seven published aerosol classification methods**
-   **Uncertainty propagation** using partial derivatives and Monte
    Carlo simulations
-   Estimation of **misclassification rates (MR)** for each aerosol type
-   Visualization tools for classification diagrams and uncertainty
    bounds
-   Compatible with **AERONET** data and external observational datasets
-   Modular and extensible architecture for adding new classification
    schemes

------------------------------------------------------------------------

## Installation

### Option 1 --- Install locally (recommended for development)

Clone the repository and install the package:

pip install -r requirements.txt pip install -e .

### Option 2 --- Install from PyPI (future release)

Once published:

pip install aerclass

------------------------------------------------------------------------

## Quick Start

Run the full classification workflow:

python run_aerclass.py

This will:

1.  Load input data
2.  Apply all implemented classification methods
3.  Propagate measurement uncertainties
4.  Calculate misclassification rates
5.  Generate figures and output tables

Results will be saved in the `output/` directory.

------------------------------------------------------------------------

## Workflow Overview

Input data → Aerosol classification → Uncertainty propagation →
Misclassification rate estimation → Visualization and analysis

------------------------------------------------------------------------

## Methods Implemented

|  ID  |  Method                   |  Variables       |  Source                 |
|:-----|:--------------------------|:---------------- |:----------------------- |
|  I   |  EAE vs AOD               |  AOD440, EAE     |  Cúneo et al. (2022)    |
|  II  |  AROD vs AOD              |  AOD1020, AOD440 |  Chen et al. (2016)     |
|  III |  FMF vs AOD               |  FMF500, AOD440  |  Barnaba & Gobbi (2004) | 
|  IVA |  SSA vs EAE               |  SSA440, EAE     |  Liu & Yi (2022)        |
|  IVB |  SSA vs EAE (fine/coarse) |  SSA440, EAE     |  Zheng et al. (2021)    |
|  V   |  AAE vs EAE               |  AAE, EAE        |  Liu & Yi (2022)        |
|  VI  |  RRI vs EAE               |  RRI440, EAE     |  Liu & Yi (2022)        |

------------------------------------------------------------------------

## Scientific Applications

AERCLASS can support research in:

-   aerosol source identification
-   atmospheric composition studies
-   air-quality monitoring
-   uncertainty analysis in remote sensing
-   evaluation of aerosol classification schemes
-   interpretation of AERONET observations

------------------------------------------------------------------------

## Citation

If you use AERCLASS in research, please acknowledge the software as 
follows:

Scagliotti, A. (2026). AERCLASS: Aerosol Classification and Uncertainty 
Analysis Toolkit (Python package).

Relevant publications related to the development and application of 
AERCLASS include:

-Scagliotti, A. F., Urquiza, J., Tames, M. F., Puliafito, S. E., & Diez,
 S. C. (2024). Uncertainties Assessment of Regional Aerosol Classification 
Schemes in South America. Earth Systems and Environment, 8(4), 1127-1158.

------------------------------------------------------------------------

## Author

**Ariel Scagliotti**\
Comisión Nacional de Energía Atómica (CNEA) -- Argentina\
https://github.com/ascaglio

------------------------------------------------------------------------

## Contributing

Contributions, suggestions, and feedback are welcome.
