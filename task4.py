import pandas as pd  

full_data = pd.read_csv("full_data.csv")  


full_data["timestamp"] = pd.to_datetime(full_data["timestamp"])  


cond1 = (full_data["quantity"] > 100) & (full_data["price"] < 10)  


full_data["hour"] = full_data["timestamp"].dt.floor("H")  
count_hour = full_data.groupby(["customer_id", "hour"])["transaction_id"].transform("count")  
cond2 = count_hour > 3  


suspicious = full_data[cond1 | cond2]  
print("suspicious transactions:") 
print(suspicious[["transaction_id", "customer_id", "quantity", "price"]].head())  

full_data.loc[cond1, "reason"] = "quantity>100 and price<10" 
full_data.loc[cond2, "reason"] = "more than 3 in 1 hour" 
print("reasons added") 

full_data["date"] = full_data["timestamp"].dt.date  
daily = full_data.groupby("date")["revenue"].sum().reset_index()  
daily["rolling_7day"] = daily["revenue"].rolling(7, min_periods=1).mean()  
print("7 day moving average:")  
print(daily.head(10))  

full_data["signup_date"] = pd.to_datetime(full_data["signup_date"])  

first_txn = full_data.groupby("customer_id")["timestamp"].min().reset_index()  
first_txn.columns = ["customer_id", "first_txn"]  
cust_signup = full_data[["customer_id", "signup_date"]].drop_duplicates()  
cust_signup = pd.merge(cust_signup, first_txn, on="customer_id", how="left")  
cust_signup["days_since_signup"] = (cust_signup["first_txn"] - cust_signup["signup_date"]).dt.days 
print("days since signup added")  

full_data = full_data.sort_values(["customer_id", "timestamp"]) 
full_data["gap"] = full_data.groupby("customer_id")["timestamp"].diff().dt.days  
freq = full_data.groupby("customer_id")["gap"].mean().reset_index() 
freq.columns = ["customer_id", "purchase_frequency"] 
print("purchase frequency added")  

div = full_data.groupby("customer_id")["category"].nunique().reset_index() 
div.columns = ["customer_id", "category_diversity"]  
print("category diversity added") 

pref = full_data.groupby("customer_id")["payment_method"].agg(lambda x: x.mode()[0]).reset_index() 
pref.columns = ["customer_id", "preferred_payment"]  
print("preferred payment added")

features = pd.merge(cust_signup, freq, on="customer_id", how="left")  
features = pd.merge(features, div, on="customer_id", how="left") 
features = pd.merge(features, pref, on="customer_id", how="left")  
print("final features sample:") 
print(features.head()) 
