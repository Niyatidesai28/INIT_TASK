import pandas as pd

full_data = pd.read_csv("full_data.csv")  

customer_revenue = full_data.groupby("customer_id")["revenue"].sum().reset_index()
print("total revenue per customer:", customer_revenue.head())

customer_txn = full_data.groupby("customer_id")["transaction_id"].count().reset_index()
customer_txn.columns = ["customer_id", "num_transactions"]
print("number of transactions per customer:", customer_txn.head())

avg_txn_value = full_data.groupby("customer_id")["revenue"].mean().reset_index()
avg_txn_value.columns = ["customer_id", "avg_transaction_value"]
print("average transaction value per customer:", avg_txn_value.head())

cust_summary = pd.merge(customer_revenue, customer_txn, on="customer_id")
cust_summary = pd.merge(cust_summary, avg_txn_value, on="customer_id")
print("merged customer summary:", cust_summary.head())

full_data["timestamp"] = pd.to_datetime(full_data["timestamp"])
full_data["month"] = full_data["timestamp"].dt.to_period("M")
month_revenue = full_data.groupby("month")["revenue"].sum().reset_index()
print("total revenue per month:", month_revenue.head())

month_customers = full_data.groupby("month")["customer_id"].nunique().reset_index()
month_customers.columns = ["month", "unique_customers"]
print("unique customers per month:", month_customers.head())

avg_order_value = full_data.groupby("month")["revenue"].mean().reset_index()
avg_order_value.columns = ["month", "avg_order_value"]
print("average order value per month:", avg_order_value.head())

month_stats = pd.merge(month_revenue, month_customers, on="month")
month_stats = pd.merge(month_stats, avg_order_value, on="month")
print("monthly stats:", month_stats.head())
