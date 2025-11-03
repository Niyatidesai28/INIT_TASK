import pandas as pd

# load csv files
customers = pd.read_csv("Customers.csv")
products = pd.read_csv("Products.csv")
transactions = pd.read_csv("Transactions.csv")

customers = customers.fillna(customers.median(numeric_only=True))#Numeric columns → replaced with their median
for col in customers.select_dtypes(include="object"): #Text/object columns → replaced with their most frequent (mode) value
    customers[col] = customers[col].fillna(customers[col].mode()[0])

products = products.fillna(products.median(numeric_only=True))
for col in products.select_dtypes(include="object"):
    products[col] = products[col].fillna(products[col].mode()[0])

transactions = transactions.fillna(transactions.median(numeric_only=True))
for col in transactions.select_dtypes(include="object"):
    transactions[col] = transactions[col].fillna(transactions[col].mode()[0])

print("missing values handled")

transactions["revenue"] = transactions["quantity"] * transactions["price"]
print("added revenue column")

full_data = pd.merge(transactions, customers, on="customer_id", how="left")
full_data = pd.merge(full_data, products, on="product_id", how="left")
print("merged full_data shape:", full_data.shape)

# (price - costprice)/price*100
full_data["profit_margin"] = (full_data["price"] - full_data["cost_price"]) / full_data["price"] * 100
print("added profit margin column")

print("full data sample:", full_data.head())
full_data.to_csv("full_data.csv", index=False) # saving for later
print("full_data.csv saved")