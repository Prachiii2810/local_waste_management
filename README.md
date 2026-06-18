# 🌱 Local Food Wastage Management System

A centralized platform and analytics dashboard built to bridge the gap between food surpluses and communities in need. This project analyzes operational datasets, executes deep analytical SQL queries, and surfaces metrics via an interactive **Streamlit** dashboard to optimize donation efficiency and minimize local food waste.

---

## 📌 Project Overview & Objective

Every day, vast amounts of edible food are discarded by restaurants, grocery stores, and supermarkets due to coordination bottlenecks. Concurrently, thousands of individuals and local NGOs struggle to access meals.

**The Solution:** This centralized system connects **Food Providers** with **Receivers (NGOs/Shelters)**. 
* Providers post available food listings.
* Receivers claim active listings dynamically.
* Transactions, statuses, and timeline parameters are monitored and stored for systemic insight reporting.

---

## 📂 Project Architecture & Repository Structure

```text
├── 📁 data/
│   ├── providers.csv          # Profiles of contributing vendors (Restaurants, Groceries)
│   ├── receivers.csv          # Profiles of distribution channels (NGOs, Shelters)
│   ├── food_listings.csv      # Log entries of generated food surpluses
│   └── claims.csv             # Operational logs tracking claimed donations
├── app.py                     # Main interactive Streamlit Dashboard web app 
├── queries.sql                # Production-ready file containing 15+ complex analytical SQL queries
└── requirements.txt           # Deployment configurations for packages and libraries
