# Dissertation Experiment

This repository contains the full pipeline for my dissertation experiment, covering dataset preparation, feature selection, and machine learning model evaluation.

---

## Overview

The experiment involves:
1. Preprocessing and cleaning a dataset
2. Applying feature selection techniques to identify the most informative features
3. Training and comparing two machine learning models — **Random Forest (RF)** and **Decision Tree (DT)**
4. Validating results and visualising model performance

---

## Repository Structure

### Python Scripts

| File | Description |
|------|-------------|
| `Dataset_DF.py` | Loads and converts raw data into CSV format for processing |
| `Condensed_permissions.py` | Handles dataset de-duplication and permission condensing |
| `Numerical_Datatable_FS.py` | Prepares numerical datatable for feature selection |
| `feature_selection.py` | Runs feature selection and outputs importance scores |
| `feature_selection_Graph.py` | Generates visualisations of feature selection results |
| `dataset_Valid.py` | Validates the dataset and produces final evaluation graphs |
| `machine_learning_table.py` | Trains RF and DT models and generates comparison tables |

### Results & Output Files

| File | Description |
|------|-------------|
| `Feature_Selection_scores.txt` | Scores from the feature selection phase |
| `Machine_Learning_scores.txt` | Accuracy/performance scores for the ML models |
| `Peak_performance_Feature_selection.txt` | Summary of peak performance across feature selection runs |
| `RF_vs_DT_Full_Features.csv` | Full feature comparison between Random Forest and Decision Tree |
| `feature_selection_comparison.png` | Visual comparison of feature selection results |

### Data

| File | Description |
|------|-------------|
| `datasets.zip` | Compressed archive containing the raw and processed datasets (CSV format) |

---

## How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aoishic25/Dissertation_Experiment.git
   cd Dissertation_Experiment
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   > If no `requirements.txt` exists, the core libraries used are: `pandas`, `numpy`, `scikit-learn`, `beautifulsoup4`, `requests`, `matplotlib`

3. **Prepare the dataset**
   ```bash
   python Dataset_DF.py
   python Condensed_permissions.py
   python dataset_Valid.py
   ```

4. **Run feature selection**
   ```bash
   python Numerical_Datatable_FS.py
   python feature_selection.py
   python feature_selection_Graph.py
   ```

5. **Train and evaluate models**
   ```bash
   python machine_learning_table.py
   ```

---

## Results

Scores and model comparisons are stored in the `.txt` and `.csv` result files. Key outputs include:

- Feature importance rankings
- RF vs DT accuracy comparison across full feature sets
- Peak performance summary across all experimental runs

---

## Author

**Aoishic25** — Dissertation project repository
