import pandas as pd

customers = pd.read_csv("Customers.csv")
products = pd.read_csv("Products.csv")
transactions = pd.read_csv("Transactions.csv")

print("Customers data:", customers.head())
print("Products data:", products.head())
print("Transactions data:", transactions.head())


print("Customers shape:", customers.shape)
print("Products shape:", products.shape)
print("Transactions shape:", transactions.shape)

print("Customers types:", customers.dtypes)
print("Products types:", products.dtypes)
print("Transactions types:", transactions.dtypes)

print("Missing in Customers:", customers.isnull().sum())
print("Missing in Products:", products.isnull().sum())
print("Missing in Transactions:", transactions.isnull().sum())

dup = transactions["transaction_id"].duplicated().sum()
print("Duplicate transaction IDs:", dup)

transactions["timestamp"] = pd.to_datetime(transactions["timestamp"])

transactions["hour"] = transactions["timestamp"].dt.hour
transactions["day"] = transactions["timestamp"].dt.day_name()
transactions["month"] = transactions["timestamp"].dt.month_name()

print("Earliest date:", transactions["timestamp"].min(), "Latest date:", transactions["timestamp"].max())
print("Updated Transactions data:", transactions.head())
