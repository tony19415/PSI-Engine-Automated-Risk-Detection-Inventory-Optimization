# PSI-Engine-Automated-Risk-Detection-Inventory-Optimization
End to end analytics engineering pipeline transforming raw transactional data into PSI command center.


![dbt](https://img.shields.io/badge/dbt-1.8-orange?style=flat-square&logo=dbt)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![DuckDB](https://img.shields.io/badge/DuckDB-1.0-yellow?style=flat-square)
![PowerBI](https://img.shields.io/badge/PowerBI-Dashboard-f2c811?style=flat-square&logo=powerbi)

> **An End-to-End Analytics Engineering Portfolio Project**
> *Simulating a modern supply chain control tower to predict stockouts, optimize inventory, and enforce data governance.*

---

## 📖 Executive Summary
Supply chain teams often struggle to balance **Service Levels** (avoiding stockouts) with **Working Capital** (reducing excess inventory) due to fragmented data and reactive processes.

This project implements an **Automated PSI (Purchase-Sales-Inventory) Engine** that transforms raw transactional data into actionable insights. By integrating **dbt** for semantic modeling and automated quality governance, the system provides trustworthy, forward-looking risk detection.

**Key Capabilities:**
* **Automated Risk Alerts:** Detects stockouts 14 days in advance using a dynamic supply-demand run rate model.
* **Governance & Trust:** Implements a CI/CD-style approach to data quality with blocking tests that prevent "impossible" data (e.g., negative inventory) from reaching decision-makers.
* **Scenario Planning:** Simulates supply chain volatility (randomized lead times) to stress-test safety stock levels.
* **Secure Access:** Designed with Row-Level Security (RLS) logic to restrict sensitive cost data by region.

---

## 🏗️ Architecture & Tech Stack

This project follows a **Modern Data Stack** architecture, running locally via DuckDB for high-performance analytics without cloud costs.

| Component | Tool | Description |
| :--- | :--- | :--- |
| **Ingestion & Simulation** | `Python (Pandas)` | Generates mock Supply/PO data to complement Kaggle demand data. |
| **Warehouse** | `DuckDB` | Serverless, fast SQL OLAP engine. |
| **Transformation** | `dbt (data build tool)` | Handles cleaning, testing, and lineage. |
| **Orchestration** | `Bash` | Simple pipeline execution. |
| **Visualization** | `PowerBI` | Final interactive dashboard for planners. |

### Data Lineage
*(Insert screenshot of dbt lineage graph here)*
> *The pipeline traces data from raw CSVs -> Staging (Cleaning) -> Intermediate (PSI Logic) -> Marts (Star Schema).*

---

## 📂 Project Structure

```text
psi-supply-chain-portfolio/
├── dbt_psi/               # The Transformation Layer
│   ├── models/
│   │   ├── staging/       # 1:1 Cleaned views of raw data
│   │   ├── intermediate/  # Complex PSI Logic (Running Totals)
│   │   └── marts/         # Final Star Schema (dim_product, fct_psi)
│   ├── tests/             # Data Quality Checks (Governance)
│   └── dbt_project.yml
├── python_engine/         # The Simulation Layer
│   ├── generate_mock_supply.py  # Script to create POs & Inventory
│   └── forecast_model.py        # (Optional) Demand Forecasting logic
├── data/                  # Local Data Lake
│   ├── raw/               # Landing zone for CSVs
│   └── output/            # Exported data for PowerBI
├── requirements.txt       # Python dependencies
└── README.md              # You are here