# ⚓ Maritime Crisis Analysis & Route Risk Optimizer

A real-time geographical analysis tool designed to minimize risk for shipping traders by evaluating sea routes, ports, and countries against active global crises. This project leverages data to provide actionable insights, helping logistics managers choose safer paths and avoid costly disruptions caused by geopolitical conflicts, piracy, or severe weather events.

---

## 🎯 Overview

Global maritime trade is increasingly vulnerable to geographical crises. The **Geography Crisis Analysis** tool addresses this by providing a dynamic assessment of sea routes. It aggregates data on current crises to score and visualize risk levels, enabling traders to make informed, real-time decisions about their shipping logistics.

### Key Value Proposition
* **Minimize Risk**: Proactively identify and avoid high-risk zones.
* **Optimize Routes**: Data-driven suggestions for alternative, safer shipping lanes.
* **Real-time Awareness**: Live updates on how emerging crises impact specific ports and nations.

---

## 📊 Key Features

✅ **Real-Time Crisis Mapping**
Visualize active crises (geopolitical unrest, piracy hotspots, natural disasters) directly on maritime maps.

✅ **Route Risk Assessment**
Input standard shipping routes to receive a comprehensive risk score based on current geographical data along the path.

✅ **Port & Country Impact Analysis**
Check the operational status and risk level of specific destination ports and trading partner countries before finalizing shipments.

✅ **Dynamic Rerouting Suggestions**
(Planned Feature) AI-driven recommendations for the safest and most efficient alternative routes when primary paths are compromised.

---

## 📁 Project Structure

```text
geography_crisis_analysis/
│
├── app.py                 # Main dashboard application (Streamlit/Flask)
├── requirement.txt        # Project dependencies
├── data/                  # Geographical and crisis datasets
│   ├── maritime_routes.csv
│   └── active_crises.json
└── README.md              # Project documentation
⚙️ Setup & Installation
Prerequisites
Python 3.9+

[Optional: API keys if using live data sources]

Installation Steps
Clone the repository

Bash

git clone [https://github.com/damodar04/geography_crisis_analysis.git]
cd geography_crisis_analysis
Install dependencies

Bash

pip install -r requirement.txt
Run the Dashboard

Bash

# If using Streamlit:
streamlit run app.py
# If using Flask:
# python app.py
🧠 Future Roadmap
[ ] Integration with live AIS shipping data APIs.

[ ] Machine learning model to predict future crisis hotspots based on historical trends.

[ ] Automated email alerts for traders when their active routes enter high-risk status.

👤 Author
Damodar Bhawsar

🌍 Focus: Data Science & Geopolitical Analysis

🔗 LinkedIn: damodar-bhawsar-

🐙 GitHub: @damodar04
