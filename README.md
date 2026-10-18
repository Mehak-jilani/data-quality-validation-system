## Automated Data Quality & Validation System
### CadetX Work Experience — Data Analyst

## 📌 Project Overview
An end-to-end automated data quality engine that profiles raw datasets, detects hidden data quality issues, and generates structured reports **before** any cleaning or ML happens. This repository tracks all 4 modules of the CadetX project:

- **Module 1 — Advanced Data Profiling & Metadata Intelligence** ✅ *(completed)*
- **Module 2 — Automated Data Cleaning & Transformation** ✅ *(completed)*
- **Module 3 — AI-Powered Data Validation** ✅ *(completed)*
- Module 4 — End-to-End Pipeline, Docker & Automation *(upcoming)*

## 📊 Dataset
**Bank Marketing Dataset (UCI Machine Learning Repository)**
*   **Rows:** 11,162
*   **Columns:** 17
*   **Domain:** Finance / Marketing (term-deposit campaign data)
*   **Target variable:** `deposit` (yes/no)

## 🛠️ Tools & Technologies
Python · Pandas · NumPy · Matplotlib · scikit-learn · Google Colab · GitHub

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

## 🧹 Module 2 — Data Cleaning ✅

**Cleaning engine results (Bank Marketing dataset, 11,162 rows):**

| Action | What it does | Rows affected |
|---|---|---|
| **Sentinel fix** | `pdays = -1` ("never contacted") → real missing value | 8,324 |
| **Invalid value fix** | Negative `balance` (impossible) → missing | 688 |
| **Outlier capping** | IQR winsorization on 5 flagged columns | 3,504 |
| **KNN imputation** | Missing values filled via KNNImputer (5 neighbours) | 9,012 |
| **Fuzzy duplicate detection** | Composite profile matching (age+job+marital+balance) | 960 groups / 1,560 rows |
| **Scaling + encoding** | StandardScaler (7 numeric) + one-hot (9 categorical) → ML-ready | 11,162 × 43 cols |

**Quality Score: 91.84 → 95.16 (+3.32)** · sentinel 8,324→0 · negatives 688→0 · outliers 6,471→171 (–97%)

*Module 2 outputs:* `cleaned_data.csv` + `cleaning_log.json` (audit trail) · `ml_ready_data.csv` (ML-ready)

## 🤖 Module 3 — AI-Powered Validation ✅

**Two-layer validation on the cleaned dataset:**

| Layer | What it does | Result |
|---|---|---|
| **Rule-based engine** | 8 business rules with severity levels (age 18–100, balance ≥ 0, valid categories, day 1–31, target yes/no) | **8/8 PASSED — 0 violations** (confirms Module 2 cleaning worked) |
| **AI anomaly detection** | Isolation Forest (scikit-learn) flags records that pass all rules but are statistically unusual | **224 anomalies (2.01%)** — e.g. 82-yr customer with 844-min call |

**Dataset Health Score: 97.99 / 100**

*Module 3 output:* `validation_report.json` (rules result + anomaly summary + health score)

## 📂 Repository Contents
| File | Description |
|---|---|
| `Module1_Data_Profiling_Engine.ipynb` | Profiling engine code (Google Colab notebook) |
| `profiling_report.json` | Full structured profiling report (per-column stats + rules) |
| `outlier_distribution.png` | Boxplot of numeric columns — outlier analysis |
| `correlation_heatmap.png` | Feature correlation matrix |
| `Module2_Data_Cleaning.ipynb` | Cleaning engine (sentinel fix, outlier capping, KNN imputation, fuzzy duplicates, scaling/encoding) |
| `cleaned_data.csv` | Cleaned dataset — 11,162 rows (sentinel fixed, outliers capped) |
| `cleaning_log.json` | Audit trail of every cleaning action + before/after quality scores |
| `ml_ready_data.csv` | ML-ready dataset — 11,162 rows × 43 columns (scaled + one-hot encoded) |
| `Module3_Data_Validation.ipynb` | Validation engine (rule checks + Isolation Forest anomaly detection) |
| `validation_report.json` | Validation results — 8/8 rules, 224 anomalies, health 97.99/100 |
| `architecture_diagram.png` / `.mmd` | System architecture (4-module pipeline flow) + Mermaid source |

## ▶️ How to Run
1. Open the Module notebook in Google Colab.
2. Upload the required CSV when prompted (Module 1–2: `bank.csv`; Module 3: `cleaned_data.csv`).
3. Run all cells — each module writes its outputs.

## 👤 Author

**Mehak Jilani** — Data Analyst (Volunteer), CadetX UK Work Experience

[🔗 LinkedIn Profile](https://www.linkedin.com/in/mehak-jilani)
