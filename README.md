# Supply Chain Delivery Performance Analysis

## Project Overview

This project analyzes supply chain delivery performance to evaluate the operational and financial impact of late deliveries.

The objective of this analysis is to determine whether delivery delays are region-specific or systemic, quantify revenue exposure caused by delays, and provide actionable business recommendations.

The analysis was conducted using SQL for data preparation and Power BI for data modeling and visualization.

---

## Business Objectives
- Measure overall Late Delivery Rate
- Quantify revenue exposure caused by delayed orders
- Analyze delay severity levels (Low, Moderate, High Risk)
- Evaluate shipping mode performance
- Identify whether delays are regional or systemic

---

## Dataset Description
- Dataset Size: 100K+ delivery records
- Key Fields:
  - Order Date
  - Ship Date
  - Delivery Status
  - Shipping Mode
  - Region
  - Sales / Revenue
  - Delivery Duration

The dataset was cleaned and prepared before visualization and KPI modeling.

---

## Key Metrics (KPIs)
- **Late Delivery Rate (%)**
- **Lost Revenue (Revenue from Late Orders)**
- **Average Delay Days**
- **Delay Severity Distribution**
- **Shipping Mode Performance Comparison**

---

## Key Insights
1. Late delivery rate (~57%) was consistent across regions, indicating systemic operational inefficiencies rather than region-specific issues.
2. Moderate and High-risk delays contributed disproportionately to revenue exposure.
3. Faster shipping modes reduced delay duration but did not significantly lower the overall late delivery rate.
4. Revenue risk is driven more by delay severity than by geographical distribution.

---

## Business Recommendations
- Implement severity-based monitoring instead of region-based prioritization.
- Optimize operational workflows causing systemic delays.
- Introduce proactive delay risk tracking dashboard.
- Focus improvement initiatives on moderate and high-risk delivery categories.

---

## Tools & Technologies Used
- SQL (Data Cleaning & Preparation)
- Power BI (Dashboard & Data Modeling)
- DAX (KPI Calculation)
- Data Modeling (Star Schema approach)

---

## Dashboard Preview
<img width="1425" height="739" alt="image" src="https://github.com/user-attachments/assets/7c38ea38-e0f0-4cfa-b5fe-e46b16ad465a" />


---

## Project Structure
Supply-Chain-Delivery-Analysis/
│
├── README.md
├── data/
│ └── sample_dataset.csv
├── sql/
│ └── data_cleaning_queries.sql
├── powerbi/
│ └── dashboard_screenshot.png
└── documentation/
└── project_summary.pdf

---

## Project Outcome
This project demonstrates end-to-end analytical capability:
- Business problem framing
- Data preparation
- KPI modeling
- Insight generation
- Executive-level recommendation delivery

## Data Source
The dataset used in this project was obtained from Kaggle (public dataset) for educational and portfolio purposes.
All analysis and modeling were independently conducted.
