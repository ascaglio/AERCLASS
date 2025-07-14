# AERCLASS

**Aerosol Classification and Uncertainty Analysis Toolkit**

AERCLASS is an open-source Python package designed to apply a suite of 2D aerosol classification methods and estimate their associated uncertainties. It is built with a focus on atmospheric science research and reproducibility.

---

## 📦 Features

- Implements 7 published aerosol classification schemes
- Propagates measurement uncertainties to classification outputs
- Calculates misclassification rates based on uncertainty bounds
- Includes plotting utilities for 2D distribution and error visualization
- Modular, extensible, and easy to use with AERONET and other sources

---

## 📥 Installation

You can install AERCLASS locally with:

```bash
pip install -r requirements.txt
```

Or in development mode:

```bash
pip install -e .
```

---

## 🚀 Quick Start

Run the complete classification workflow with:

```bash
python main.py
```

Or try a minimal example with just Method I:

```bash
python example.py
```

---

## 📂 Structure

```bash
AERCLASS/
├── aerclass/            # Core module (classify, plots, utils, uncertainty)
├── output/              # Generated figures and CSVs
├── data/                # Input Excel files (optional)
├── main.py              # Full workflow execution
├── example.py           # Simple usage example
├── setup.py             # Installation script
├── requirements.txt     # Dependencies
└── README.md            # This file
```

---

## 📘 Methods Implemented

| ID   | Method                  | Variables              | Source                    |
|------|--------------------------|------------------------|----------------------------|
| I    | EAE vs AOD              | AOD440, EAE            | Cúneo et al. (2022)       |
| II   | AROD vs AOD             | AOD1020, AOD440        | Chen et al. (2016)        |
| III  | FMF vs AOD              | FMF500, AOD440         | Barnaba & Gobby (2004)    |
| IVA  | SSA vs EAE              | SSA440, EAE            | Liu & Yi (2022)           |
| IVB  | SSA vs EAE (fine/coarse)| SSA440, EAE            | Zheng et al. (2021)       |
| V    | AAE vs EAE              | AAE, EAE               | Liu & Yi (2022)           |
| VI   | RRI vs EAE              | RRI440, EAE            | Liu & Yi (2022)           |

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙋 Author

**Ariel Scagliotti**  
National Atomic Energy Commission, Argentina  
[GitHub Profile](https://github.com/ascaglio)

Contributions and feedback are welcome!
