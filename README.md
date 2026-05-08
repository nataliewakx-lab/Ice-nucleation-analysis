# Ice-nucleation-analysis
Droplet freezing assay datasets were used to quantify heterogeneous ice nucleation behaviour of cement, anhydrite and gypsum.

# Evaluating the Ice‑Nucleation Efficiency of Cement Factory Aerosols

This repository contains the code and supporting material for my undergraduate dissertation at the University of Leeds (2026).  
The project investigates the **Ice‑nucleation efficiency of Ordinary Portland Cement (OPC), Anhydrite (CaSO₄), and Gypsum (CaSO₄·2H₂O)** aerosols using droplet‑freezing assay data to assess their potential impact on mixed‑phase clouds.

## Research Background

Ice nucleating particles (INPs) play an important role in atmospheric processes by influencing the formation and properties of mixed-phase clouds, which contain both supercooled liquid droplets and ice crystals. The efficiency with which aerosols initiate ice formation can affect cloud lifetime, precipitation processes, and the Earth’s radiative balance, making ice nucleation an important factor in climate and weather modelling.

Mineral dusts and industrial aerosols have been identified as potential atmospheric INPs, although the ice-nucleating behaviour of cement-related aerosols remains relatively underexplored. This project investigates the ice-nucleation efficiency of cement factory aerosol analogues using droplet freezing assays to better understand their potential atmospheric impacts.

The analysis focuses on calculating the fraction of frozen droplets as a function of temperature to compare the freezing behaviour of different cement-related materials against control samples. The project combines environmental science, experimental analysis, and scientific computing workflows using Python-based data analysis techniques.

---

## Repository Structure
```
ice-nucleation-analysis/
│
├── README.md
├── requirements.txt
├── data/
│   ├── blank_control_run1.csv
│   ├── blank_control_run2.csv
│   ├── blank_control_run3.csv
│   ├── K-Feldspar_0.1pct_run1.csv
│   ├── K-Feldspar_0.1pct_run2.csv
│   ├── K-Feldspar_0.1pct_run3.csv
│   ├── K-Feldspar_1pct_run1.csv
│   ├── K-Feldspar_1pct_run2.csv
│   ├── K-Feldspar_1pct_run3.csv
│   ├── OPC_0.1pct_run1.csv
│   ├── OPC_0.1pct_run2.csv
│   ├── OPC_0.1pct_run3.csv
│   ├── OPC_1pct_run1.csv
│   ├── OPC_1pct_run2.csv
│   ├── OPC_1pct_run3.csv
│   ├── anhydrite_0.1pct.csv
│   ├── anhydrite_1pct.csv
│   ├── gypsum_0.1pct.csv
│   ├── gypsum_1pct.csv
│
└──── analysis.py/
    └── droplet_freezing_analysis.py
```
---

## Methodology Summary

Experiments were carried out using the **μL‑NIPI droplet‑freezing assay**, recording the freezing temperature of multiple microdroplets. Raw droplet freezing assay data were analysed using Python-based workflows within the Spyder IDE (WinPython64 environment). Pre-existing preprocessing scripts (Barr, 2023) developed for EF600 droplet freezing assay datasets for academic research purposes were adapted to identify individual ice nucleation events from LabView-generated recordings.
The resulting datasets were exported as structured CSV files containing:

* date and time data,
* plate and set-point temperatures,
* Stirling voltage measurements associated with freezing events.

The following key calculation was implemented in Python:
```python
f_ice(T) = n_ice(T) / n_total              # Fraction of frozen droplets
```
where:

* n_ice(T) represents the number of droplets frozen at temperature T,
* n_total represents the total number of droplets analysed. 


The code performs:
- Data cleaning and outlier handling
- Statistical analysis of freezing temperatures

---

## Technologies Used

- Python
- Spyder IDE
- pandas
- NumPy

---

## How to Run

1. **Download or clone** this repository:  
   ```bash
   git clone https://github.com/nataliewakx-lab/Ice-nucleation-analysis.git
   cd Ice-nucleation-analysis

### 2. Install required packages

```bash
pip install pandas numpy
```

### 3. Run the analysis script

```bash
python analysis.py
```

Running this script imports the droplet freezing assay datasets, performs preprocessing and fraction-frozen calculations.

---

## Expected Outputs

The outputs include:

* processed freezing event data,
* calculated fraction-frozen values,
* cleaned datasets suitable for further statistical analysis,
* exported CSV files for interpretation and comparison between experimental samples and controls.

---

## Dataset Information and Citation

All datasets were collected using the μL‑NIPI at the University of Leeds, School of Earth and Environment. If referencing this repository or methodology, please cite the associated undergraduate dissertation project: 

Kiprono, N. W. (2026). **Evaluating the Ice‑Nucleation Efficiency of Cement Factory Aerosols and Their Potential Effect on Mixed‑Phase Clouds**.

Python script was written by Sarah Burr (2023) for academic research purposes. As part of the above research project I have permission to use it and include it. 




