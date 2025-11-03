import pandas as pd
import time  

# load data
full_data = pd.read_csv("full_data.csv") 


start = time.time()  
result = []  

for i, row in full_data.iterrows():  
    if row["age"] > 25 and row["country"] == "USA":  
        result.append(row["customer_id"])  
end = time.time() 
print("slow loop time:", end - start, "seconds")

start = time.time()  
fast_result = full_data.loc[(full_data["age"] > 25) & (full_data["country"] == "USA"), "customer_id"] 
end = time.time() 
print("fast vectorized time:", end - start, "seconds")  

print("vectorization is much faster!")



def customer_lifetime_value(transactions_df, customer_id, discount_rate=0.1):
    """
    simple function to calculate CLV (customer lifetime value)
    CLV = sum of (revenue * (1 - discount_rate)^month)
    """
    cust_data = transactions_df[transactions_df["customer_id"] == customer_id]

    cust_data["timestamp"] = pd.to_datetime(cust_data["timestamp"])

    cust_data = cust_data.sort_values("timestamp")

    cust_data["month_index"] = range(len(cust_data))

    cust_data["discount_factor"] = (1 - discount_rate) ** cust_data["month_index"]

    clv_value = (cust_data["revenue"] * cust_data["discount_factor"]).sum()

    return clv_value  

one_cust = full_data["customer_id"].iloc[0]  
clv = customer_lifetime_value(full_data, one_cust)  
print("CLV for customer", one_cust, "=", clv)  
