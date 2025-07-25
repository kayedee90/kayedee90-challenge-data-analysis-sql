# **Belgium Business Insights – SQL Data Analysis**

## **Description**

This project is part of the **BeCode AI & Data Analytics training**.
It focuses on analyzing a **real-world database of Belgian companies** using **SQL** to extract meaningful business insights.

The database contains information on:

* **Companies** (juridical form, status, type, start date)
* **Addresses** (zip code, municipality, province)
* **Activities** (NACE codes)
* **Establishments and branches**
* **Contacts**

The goal is to **tell a story about business trends in Belgium** by answering strategic questions using SQL queries and presenting the findings in a short **slide deck**.

---

## **Key Insights Delivered**

Some of the main questions answered:

1. **Which industries dominate the Belgian market at which time?**
2. **How is the geographical distribution of companies changing over time?**
3. **What are the fastest-growing provinces?**
4. **How has Belgium’s economy shifted from industrial to service sectors since 1960?**
5. **What role does Brussels play compared to other regions?**
6. **Which sectors dominate each decade?**
7. **What is the Compound Annual Growth Rate (CAGR) by province?**
8. **Projection of top provinces for 2040 based on historical growth.**

---

## **Installation**

**Requirements:**

* Python 3.10+
* PostgreSQL (or your DB engine)
* Libraries:

  ```bash
  pip install pandas plotly kaleido
  ```

Clone the repository:

```bash
git clone https://github.com/kayedee90/challenge-data-analysis-sql.git
cd challenge-data-analysis-sql
```

---

## **Usage**

1. **Run SQL queries** in your PostgreSQL client (e.g., DBeaver).
2. **Generate charts**:

   ```bash
   python belgium_industry_charts.py
   ```
3. **View interactive dashboard**:
   Open `exports/dashboard.html` in a browser.
4. **Export PNG charts** for presentation (auto-generated in `exports/`).

---

## ** Visual Examples**

* **Log-scale growth chart**
* **Regional share evolution**
* **CAGR comparison**
* **Interactive Belgium map by province**
* **Pie charts: 1960 vs 2020 regional share**

---

## **Contributors**

* **Kenny Dif** – Data Analyst

---

## **Timeline**

* Project Duration: **2 days**
* Deadline: **25/07/2025 – 16:30**

---

## **Personal Notes**

This project was an opportunity to:

* Apply **SQL for advanced analytics** on a large dataset.
* Build **visual storytelling** around business trends.
* Combine **raw data → insights → presentation** within strict time constraints.

---
