## Automated Data Quality & Validation System
### CadetX Virtual Work Experience — Junior BI Analyst Track

## 📌 Project Overview
An end-to-end automated data quality engine that profiles raw datasets, detects hidden data quality issues, and generates structured reports **before** any cleaning or ML happens. This repository tracks all 4 modules of the CadetX project:

- **Module 1 — Advanced Data Profiling & Metadata Intelligence** ✅ *(completed)*
- Module 2 — Automated Data Cleaning & Transformation *(in progress)*
- Module 3 — AI-Powered Data Validation *(upcoming)*
- Module 4 — End-to-End Pipeline, Docker & Automation *(upcoming)*

## 📊 Dataset
**Bank Marketing Dataset (UCI Machine Learning Repository)**
*   **Rows:** 11,162
*   **Columns:** 17
*   **Domain:** Finance / Marketing (term-deposit campaign data)
*   **Target variable:** `deposit` (yes/no)

## 🛠️ Tools & Technologies
Python · Pandas · NumPy · Matplotlib · Google Colab · GitHub

## 🔍 Module 1 — Key Features Implemented
1. **Metadata Extraction Engine** — infers logical data types, detects mixed-type columns and their type composition, classifies semantic meaning (email / phone / date / ID patterns).
2. **Profiling Engine** — missing-value matrix, dtype consistency, unique value & cardinality analysis, ID-like column detection, full numeric statistics (mean, std, quartiles, skew, IQR outliers).
3. **Profiling Visualisations** — outlier distribution (boxplot) and correlation heatmap, generated backend-side as PNG.
4. **Rule Engine** — flags suspicious columns using threshold rules (>50% missingness, mixed types, ID-like cardinality, heavy outliers >5% of rows).
5. **PII Detection** — automatically flags potential Personally Identifiable Information (detected: `age` → dob, `contact` → phone).

## 🚀 Module 1 — Key Findings
*   **5 suspicious columns flagged:** `balance` (1,055 outliers), `duration` (636), `campaign` (601), `pdays` (2,750), `previous` (1,258) via IQR rule.
*   **Negative balances:** `balance` minimum is **-6,847** — impossible for a bank account, indicating data errors.
*   **Sentinel value trap:** `pdays = -1` means "never contacted before" — it is a **category disguised as a number**, polluting 25%+ of rows as fake outliers.
*   **"Unknown" categories:** `education` (497), `contact` (2,346), `poutcome` (8,326 = 75% of data).
*   **The twist:** the dataset shows **0% missing values** — yet hides severe quality issues. Surface-level cleanliness ≠ clean data.

## 📂 Repository Contents
| File | Description |
|---|---|
| `Module1_Data_Profiling_Engine.ipynb` | Profiling engine code (Google Colab notebook) |
| `profiling_report.json` | Full structured profiling report (per-column stats + rules) |
| `outlier_distribution.png` | Boxplot of numeric columns — outlier analysis |
| `correlation_heatmap.png` | Feature correlation matrix |

## ▶️ How to Run
1. Open `Module1_Data_Profiling_Engine.ipynb` in Google Colab.
2. Upload the Bank Marketing CSV when prompted (Cell 1).
3. Run all cells — the engine auto-detects the file separator, profiles every column, and writes `profiling_report.json` + visualisations to the `results/` folder.

## 👤 Author
**Mehak Jilani** — BBA Student | Aspiring Data Analyst
CadetX UK Virtual Work Experience (Batch 2026-A)
linkedin.com/in/mehak-jilani
