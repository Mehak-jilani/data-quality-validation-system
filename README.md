## Automated Data Quality & Validation System
### CadetX Work Experience — Data Analyst

## 📌 Project Overview
An end-to-end automated data quality engine that profiles raw datasets, detects hidden data quality issues, and generates structured reports **before** any cleaning or ML happens. This repository tracks all 4 modules of the CadetX project:

- **Module 1 — Advanced Data Profiling & Metadata Intelligence** ✅ *(completed)*
- **Module 2 — Automated Data Cleaning & Transformation** ✅ *(completed)*
- **Module 3 — AI-Powered Data Validation** ✅ *(completed)*
- **Module 4 — End-to-End Pipeline, Docker & Automation** ✅ *(completed)*

## 📊 Dataset
**Bank Marketing Dataset (UCI Machine Learning Repository)**
*   **Rows:** 11,162
*   **Columns:** 17
*   **Domain:** Finance / Marketing (term-deposit campaign data)
*   **Target variable:** `deposit` (yes/no)

## 🛠️ Tools & Technologies
Python · Pandas · NumPy · Matplotlib · scikit-learn · PyYAML · Pytest · Docker · Google Colab · GitHub

## 🔍 Module 1 — Data Profiling ✅
1. **Metadata Extraction Engine** — infers logical data types, detects mixed-type columns and their type composition, classifies semantic meaning (email / phone / date / ID patterns).
2. **Profiling Engine** — missing-value matrix, dtype consistency, unique value & cardinality analysis, ID-like column detection, full numeric statistics (mean, std, quartiles, skew, IQR outliers).
3. **Profiling Visualisations** — outlier distribution (boxplot) and correlation heatmap, generated backend-side as PNG.
4. **Rule Engine** — flags suspicious columns using threshold rules (>50% missingness, mixed types, ID-like cardinality, heavy outliers >5% of rows).
5. **PII Detection** — automatically flags potential Personally Identifiable Information (detected: `age` → dob, `contact` → phone).

**Key findings:**
*   **5 suspicious columns flagged:** `balance` (1,055 outliers), `duration` (636), `campaign` (601), `pdays` (2,750), `previous` (1,258) via IQR rule.
*   **Negative balances:** `balance` minimum is **-6,847** — impossible for a bank account, indicating data errors.
*   **Sentinel value trap:** `pdays = -1` means "never contacted before" — a **category disguised as a number**, polluting 25%+ of rows as fake outliers.
*   **"Unknown" categories:** `education` (497), `contact` (2,346), `poutcome` (8,326 = 75% of data).
*   **The twist:** the dataset shows **0% missing values** — yet hides severe quality issues. Surface-level cleanliness ≠ clean data.

## 🧹 Module 2 — Data Cleaning ✅

| Action | What it does | Rows affected |
|---|---|---|
| **Sentinel fix** | `pdays = -1` ("never contacted") → real missing value | 8,324 |
| **Invalid value fix** | Negative `balance` (impossible) → missing | 688 |
| **Outlier capping** | IQR winsorization on 5 flagged columns | 3,504 |
| **KNN imputation** | Missing values filled via KNNImputer (5 neighbours) | 9,012 |
| **Fuzzy duplicate detection** | Composite profile matching (age+job+marital+balance) | 960 groups / 1,560 rows |
| **Scaling + encoding** | StandardScaler (7 numeric) + one-hot (9 categorical) → ML-ready | 11,162 × 43 cols |

**Quality Score: 91.84 → 95.16 (+3.32)** · sentinel 8,324→0 · negatives 688→0 · outliers 6,471→171 (–97%)

*Outputs:* `cleaned_data.csv` + `cleaning_log.json` (audit trail) · `ml_ready_data.csv` (ML-ready)

## 🤖 Module 3 — AI-Powered Validation ✅

| Layer | What it does | Result |
|---|---|---|
| **Rule-based engine** | 8 business rules with severity levels (age 18–100, balance ≥ 0, valid categories, day 1–31, target yes/no) | **8/8 PASSED — 0 violations** (confirms Module 2 cleaning worked) |
| **AI anomaly detection** | Isolation Forest (scikit-learn) flags records that pass all rules but are statistically unusual | **224 anomalies (2.01%)** — e.g. 82-yr customer with 844-min call |

**Dataset Health Score: 97.99 / 100**

*Output:* `validation_report.json` (rules result + anomaly summary + health score)

## ⚙️ Module 4 — Production Pipeline ✅

**One command runs everything:**

    python pipeline.py --input bank.csv --config config.yaml

| Component | Purpose |
|---|---|
| `pipeline.py` | End-to-end CLI: profile → clean → validate, with structured logging |
| `config.yaml` | YAML-driven settings — thresholds/rules without touching code |
| `test_pipeline.py` | Pytest suite — **6/6 tests passed** (caught a real bug pre-release) |
| `Dockerfile` + `requirements.txt` | Containerized, reproducible environment |
| `docker_demo.png` | Pipeline executed inside Docker (GitHub Codespaces) |

*Pipeline output: Dataset Health Score **97.99/100***

## 🏗️ System Architecture
```mermaid
graph TD
    raw["Raw CSV Data (11,162 rows)"] --> profiler["MODULE 1: PROFILER"]
    profiler --> cleaner["MODULE 2: CLEANER"]
    cleaner --> validator["MODULE 3: VALIDATOR"]
    validator --> pipeline["MODULE 4: PIPELINE"]
    
    config["config.yaml"] -.-> pipeline
    docker["Docker Deployment"] -.-> pipeline

    style raw fill:#f9f9f9,stroke:#333,stroke-width:2px
    style profiler fill:#d1e7dd,stroke:#0f5132,stroke-width:2px
    style cleaner fill:#cfe2ff,stroke:#084298,stroke-width:2px
    style validator fill:#f8d7da,stroke:#842029,stroke-width:2px
    style pipeline fill:#fef3c7,stroke:#92400e,stroke-width:2px
    style config fill:#e2e3e5,stroke:#383d41,stroke-width:1px
    style docker fill:#e2e3e5,stroke:#383d41,stroke-width:1px


## 📂 Repository Contents
| File | Description |
| --- | --- |
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
| `architecture_diagram.png` / `.mmd` | System architecture (rendered PNG + Mermaid source) |
| `Module4_Pipeline.ipynb` | Module 4 notebook (config, pipeline run, pytest, Dockerfile) |
| `pipeline.py` | End-to-end CLI pipeline script |
| `config.yaml` | Pipeline configuration (thresholds, rules, settings) |
| `test_pipeline.py` | Pytest suite — 6/6 tests passed |
| `Dockerfile` | Container definition for the pipeline |
| `requirements.txt` | Python dependencies |
| `docker_demo.png` | Docker container run output (GitHub Codespaces) |
| `final_presentation.pdf` | 5-slide project demo deck |

▶️ How to Run
Notebooks (Colab): Open module notebook → upload required CSV (Modules 1–2:  bank.csv ; Module 3:  cleaned_data.csv ) → run all cells. Pipeline:  python pipeline.py --input bank.csv --config config.yaml  · Tests:  pytest -q  · Docker:  docker build -t dq-pipeline . && docker run --rm dq-pipeline

## 👤 Author

**Mehak Jilani** — Data Analyst (Volunteer), CadetX UK Work Experience

[🔗 LinkedIn Profile](https://www.linkedin.com/in/mehak-jilani)
