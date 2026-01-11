# Inventory Management Project

A Python-based Inventory Management System with data analysis and visualization using **Streamlit**.
This project helps track inventory, manage orders, and visualize sales data through an interactive dashboard.

---

## Features

* Inventory tracking and management
* Order and user management modules
* Sales data analysis
* Interactive Streamlit dashboard
* Clean modular Python structure

---

## Tech Stack

* Python 3
* Streamlit
* Pandas
* Matplotlib
* SQLAlchemy

---

## Project Structure

```
Inventory_Management_Project/
│
├── data/
│   └── amazon_sale_report.csv
│
├── models/
│   ├── order.py
│   ├── order_manager.py
│   └── user_manager.py
│
├── visualizations.py
├── main.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/afk-rohan/Inventory_Management_Project.git
cd Inventory_Management_Project
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

---

## Author

**Rohan Sharma**
B.Tech CSE Student

---

## License

This project is for educational purposes.
