# 🗽 Spatio-Temporal Crime Patterns and Event-Driven Fluctuations in NYC

**Authors:**  
- Jan Tietz — [jtietz3060@floridapoly.edu](mailto:jtietz3060@floridapoly.edu)  
- Niklas Grau — [ngrau3035@floridapoly.edu](mailto:ngrau3035@floridapoly.edu)  
- Manuel Rodriguez — [mrodriguezberdud318@floridapoly.edu](mailto:mrodriguezberdud318@floridapoly.edu)  

---

## 📘 Abstract

Urban crime patterns in major metropolitan areas are influenced by complex interactions between population density, mobility, and public events.  
This project investigates **spatio-temporal crime dynamics** in **New York City (NYC)** during **2024**, focusing on how major public events — holidays, parades, and sporting competitions — affect crime **distribution** and **composition**.

Using **NYPD Arrest Data** and **NYC Permitted Event Data**, we apply:

- **DBSCAN** → baseline spatial clustering  
- **ST-DBSCAN** → spatio-temporal event analysis  
- **H-DBSCAN** → hierarchical density detection  

Our findings show:
- A **36.7% reduction** in total arrests during major events  
- Strongest decreases on **Thanksgiving (-61.6%)** and **New Year’s Eve (-43.0%)**  
- A proportional **increase in assaults (+13.27pp)** and **decrease in drug-related arrests (-8.13pp)**  
- **Event-driven spatial expansion** of crime during the NYC Marathon  

These results indicate that public events reshape the spatial and temporal distribution of urban crime.

---

## 🧩 Research Objectives

1. Introduce an **event-aware framework** for analyzing urban crime beyond long-term averages.  
2. Develop **spatio-temporal clustering methods** that reveal event-specific crime dynamics.  
3. Provide **data-driven insights** to improve public safety, event planning, and traveler decision-making.

---

## 📊 Datasets

### 1. NYPD Arrest Data (2024)
- Source: [NYC Open Data Portal](https://data.cityofnewyork.us/Public-Safety/NYPD-Arrests-Data-Historic-/8h9b-rp9u/about_data)  
- Contains incident-level details (date, location, offense type, borough, etc.).  
- Filtered to five key categories:
  - Robbery  
  - Assault and Related Offenses  
  - Dangerous Drugs  
  - Criminal Trespass  
  - Petit Larceny  

### 2. NYC Permitted Events Information (2024)
- Source: [NYC Permitted Events Dataset](https://data.cityofnewyork.us/City-Government/NYC-Permitted-Event-Information-Historical/bkfu-528j/about_data)  
- Includes location, date, and duration of all authorized public events.  
- Focused events:
  - Halloween  
  - Thanksgiving  
  - Independence Day  
  - New Year’s Eve  
  - NYC Marathon  

---

## ⚙️ Methodology Overview

| Method | Purpose | Description |
|--------|----------|-------------|
| **DBSCAN** | Baseline Hotspot Detection | Identifies persistent spatial clusters using density-based spatial clustering. |
| **ST-DBSCAN** | Spatio-Temporal Event Analysis | Adds time as a dimension to detect temporary, event-specific clusters. |
| **H-DBSCAN** | Hierarchical Analysis | Automatically identifies clusters across multiple density thresholds. |

### Tools & Libraries
- `pandas`, `numpy` — Data processing  
- `scikit-learn`, `st-dbscan` — Clustering algorithms  
- `matplotlib`, `contextily`, `geopandas` — Visualization  
- `OpenStreetMap` — Base maps for cluster overlays  

---

## 🧠 Key Results

| Event | Arrest Change | Notes |
|--------|----------------|-------|
| Halloween | -30.6% | Decrease in total arrests, increase in assaults |
| Thanksgiving | -61.6% | Strongest decline, high assault ratio |
| Independence Day | -26.6% | Moderate decrease, rise in petty theft |
| New Year’s Eve | -43.0% | Decline in drug-related arrests |
| NYC Marathon | -14.2% | Expanded spatial risk areas along marathon route |

**Average total arrest change:** −36.7%  
**Assaults:** +13.27 percentage points  
**Drug arrests:** −8.13 percentage points  

---

## 🗺️ Case Study: NYC Marathon

Using **ST-DBSCAN**, we compared November 3, 2024 (Marathon Day) to November 10 (Control Day).  
Results showed:
- **8 clusters** on Marathon Day vs. **5 on Control Day**  
- **Morning–afternoon temporal concentration (8 AM–2 PM)**  
- **Clusters followed the marathon route**, indicating spatial spread of crowd-related crime activity  

---

## 🔍 Conclusions

- **Persistent crime hotspots** exist year-round in dense commercial and transit zones.  
- **Major events** temporarily **reduce overall arrests** but **shift crime composition**.  
- **Spatio-temporal analysis** reveals dynamic patterns missed by static clustering methods.  

### Future Work
- Integrate weather and crowd density data  
- Extend analysis to **multi-year** comparisons  
- Develop an **interactive web dashboard** for real-time event safety predictions  

---

## 🧾 Citation

If you use this project, please cite:

> Tietz, J., Grau, N., & Rodriguez, M. (2025). *Spatio-Temporal Crime Patterns and Event-Driven Fluctuations in NYC.* Florida Polytechnic University.  

---

## 📚 References

1. Uittenbogaard, A. C., & Ceccato, V. (2012). *Space–Time Clusters of Crime in Stockholm, Sweden.* Review of European Studies, 4(1), 148–161.  
2. Delgado, M., & Sánchez-Delgado, A. (2019). *Seasonality in Property Crime: Entropy Measures and Predictability in Barcelona.* Applied Sciences, 9(24).  
3. Kumar, J. S. et al. (2024). *Predictive Analytics in Law Enforcement: Unveiling Patterns in NYPD Crime through Machine Learning and Data Mining.* ReBICTE.  
4. Birant, D., & Kut, A. (2007). *ST-DBSCAN: An Algorithm for Clustering Spatial–Temporal Data.* Data & Knowledge Engineering, 60(1), 208–221.  
5. NYC Open Data Portal. (2024). *NYPD Arrests Data (Historic)* and *NYC Permitted Event Information – Historical.*  

---

## 💻 Repository Structure

