
"""
Synthetic Sales Seasonality Analyzer (Extended)
------------------------------------------------
This project generates a synthetic daily sales database using SQLite and performs
multi-dimensional seasonal trend analysis using SQL queries and Python visualizations.
"""

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
import seaborn as sns

# Create in-memory SQLite database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create sales table
cursor.execute("""
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    product TEXT,
    region TEXT,
    quantity INTEGER,
    unit_price REAL
)
""")

# Generate synthetic daily sales data
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')
products = ['Laptop', 'Phone', 'Tablet', 'Monitor']
regions = ['North', 'South', 'East', 'West']

sales_data = []
for date in date_range:
    for _ in range(random.randint(2, 5)):
        product = random.choice(products)
        region = random.choice(regions)
        quantity = int(np.random.poisson(lam=10))
        base_price = {'Laptop': 1200, 'Phone': 800, 'Tablet': 500, 'Monitor': 300}[product]
        price = base_price * (0.95 + 0.1 * np.random.rand())
        sales_data.append((date.strftime('%Y-%m-%d'), product, region, quantity, round(price, 2)))

cursor.executemany("INSERT INTO sales (date, product, region, quantity, unit_price) VALUES (?, ?, ?, ?, ?)", sales_data)
conn.commit()

# --- Analysis 1: Total Monthly Sales ---
query_monthly = """
SELECT 
    strftime('%m', date) AS month,
    SUM(quantity * unit_price) AS total_sales
FROM sales
GROUP BY month
ORDER BY month
"""
monthly_sales = pd.read_sql_query(query_monthly, conn)
monthly_sales['month'] = monthly_sales['month'].astype(int)

plt.figure(figsize=(10, 6))
plt.plot(monthly_sales['month'], monthly_sales['total_sales'], marker='o', color='navy')
plt.title('Monthly Sales Seasonality (Synthetic)')
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.xticks(ticks=range(1,13))
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Analysis 2: Sales by Product per Month ---
query_product = """
SELECT 
    strftime('%m', date) AS month,
    product,
    SUM(quantity * unit_price) AS total_sales
FROM sales
GROUP BY month, product
ORDER BY month, product
"""
product_sales = pd.read_sql_query(query_product, conn)
product_sales['month'] = product_sales['month'].astype(int)

pivot_product = product_sales.pivot(index='month', columns='product', values='total_sales')
pivot_product = pivot_product.sort_index()

pivot_product.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='tab20')
plt.title('Monthly Sales by Product')
plt.xlabel('Month')
plt.ylabel('Sales ($)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# --- Analysis 3: Heatmap by Region and Month ---
query_region = """
SELECT 
    strftime('%m', date) AS month,
    region,
    SUM(quantity * unit_price) AS total_sales
FROM sales
GROUP BY month, region
"""
region_sales = pd.read_sql_query(query_region, conn)
region_sales['month'] = region_sales['month'].astype(int)
pivot_region = region_sales.pivot(index='region', columns='month', values='total_sales')

plt.figure(figsize=(10, 6))
sns.heatmap(pivot_region, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Sales Heatmap: Region × Month")
plt.xlabel("Month")
plt.ylabel("Region")
plt.tight_layout()
plt.show()

# --- Analysis 4: Quarterly Growth Rate ---
query_quarter = """
SELECT 
    strftime('%Y', date) AS year,
    (CAST((strftime('%m', date)-1)/3 AS INTEGER)+1) AS quarter,
    SUM(quantity * unit_price) AS total_sales
FROM sales
GROUP BY year, quarter
ORDER BY year, quarter
"""
quarter_sales = pd.read_sql_query(query_quarter, conn)
quarter_sales['quarter_label'] = quarter_sales['year'] + ' Q' + quarter_sales['quarter'].astype(str)

plt.figure(figsize=(10, 6))
plt.plot(quarter_sales['quarter_label'], quarter_sales['total_sales'], marker='o', color='darkgreen')
plt.title('Quarterly Total Sales Growth')
plt.xlabel('Quarter')
plt.ylabel('Sales ($)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Summary: Best Month and Best Region ---
best_month = monthly_sales.loc[monthly_sales['total_sales'].idxmax(), 'month']
best_region = region_sales.groupby('region')['total_sales'].sum().idxmax()

print(f"\nINSIGHTS:")
print(f"- Best month for total sales: {best_month}")
print(f"- Region with highest total sales: {best_region}")

# Close database connection
conn.close()
