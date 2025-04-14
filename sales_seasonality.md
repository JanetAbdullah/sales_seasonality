# Sales Seasonality SQL (Synthetic Data)

This project demonstrates a complete workflow for generating, querying, and analyzing synthetic sales data using SQLite + SQL + Python. It simulates daily sales for 2 years and analyzes seasonal trends across months, products, and regions.

## Project Objectives
- Simulate realistic sales transactions across time
- Perform SQL-based seasonal trend analysis
- Visualize results with professional Python plots
- Extract insights by product, region, and time period

## Tools Used
- Python 3.x
- SQLite (in-memory)
- pandas
- matplotlib
- seaborn
- numpy

## How to Run
```bash
pip install pandas matplotlib seaborn numpy
python sales_seasonality_sql.py
```

## File Structure
```
sales_seasonality_sql/
├── sales_seasonality_sql.py   # Full Python + SQL analysis pipeline
├── README.md                  # Project overview and usage instructions
```

## Key Features and Analysis

### 1. Synthetic Data Generation
- 2 full years of daily sales (2022–2023)
- Random products, quantities, regions, and prices
- Stored in an in-memory SQLite table

### 2. Monthly Sales Analysis
- Total revenue per month using SQL aggregation
- Visualized as line plot (seasonality curve)

### 3. Product-Wise Trends
- Monthly sales grouped by product
- Visualized using stacked bar charts

### 4. Region-Wise Trends
- Heatmap of region × month total sales
- Useful for detecting regional performance patterns

### 5. Quarterly Growth Tracking
- Sales per quarter for both years
- Trend line comparing growth over time

### 6. Final Insights Extracted
- Best month (by revenue)
- Region with highest total sales

## Example Visuals
- Monthly trend line plot
- Stacked bar chart (product × month)
- Region/month heatmap
- Quarterly sales growth line chart

## Use Case
Perfect for showcasing:
- SQL skills
- Synthetic data generation
- Trend extraction and storytelling
- Integrated use of SQL + Python for data science

## Author
Janet Abdullah  
GitHub: [https://github.com/JanetAbdullah]  
Feel free to fork, run, and adapt for your own portfolio!
