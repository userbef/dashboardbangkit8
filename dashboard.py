import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os

zip_file_path = 'dataset.zip'

if os.path.exists(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall('dataset')  
    df = pd.read_csv('dataset/olist_customers_dataset.csv')
    st.write(df) 
else:
    st.error(f'File {zip_file_path} not found')


# Load the datasets
df = pd.read_csv('dataset/olist_customers_dataset.csv')
df1 = pd.read_csv('dataset/olist_orders_dataset.csv')

# Data preprocessing
df = df.drop(['customer_unique_id', 'customer_zip_code_prefix', 'customer_city'], axis=1)
df1 = df1.drop(['order_status', 'order_approved_at', 'order_delivered_carrier_date', 'order_estimated_delivery_date', 'order_delivered_customer_date'], axis=1)

# Streamlit interface
st.title('Olist E-commerce Data Analysis')

# 1. Registered customers in each state
state_counts = df['customer_state'].value_counts()

st.subheader('Registered Customers per State')
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(state_counts.index, state_counts.values, color='skyblue')
ax.set_title('Registered Customers')
ax.set_xlabel('State')
ax.set_ylabel('Customer Counts')
ax.set_xticks(state_counts.index)
ax.set_xticklabels(state_counts.index, rotation=45)
st.pyplot(fig)

# 2. Number of purchases each year
df1['order_purchase_timestamp'] = pd.to_datetime(df1['order_purchase_timestamp'])
df1['Year'] = df1['order_purchase_timestamp'].dt.year
yearly_orders = df1['Year'].value_counts().sort_index()

st.subheader('Number of Purchases Each Year')
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(yearly_orders.index, yearly_orders.values, color='lightgreen')
ax.set_title('Number of Purchases Each Year')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Purchases')
ax.set_xticks(yearly_orders.index)
st.pyplot(fig)

# 3. Number of purchases per month for each year
df_2016 = df1[df1['order_purchase_timestamp'].dt.year == 2016]
df_2017 = df1[df1['order_purchase_timestamp'].dt.year == 2017]
df_2018 = df1[df1['order_purchase_timestamp'].dt.year == 2018]

df_2016['Month'] = df_2016['order_purchase_timestamp'].dt.month
df_2017['Month'] = df_2017['order_purchase_timestamp'].dt.month
df_2018['Month'] = df_2018['order_purchase_timestamp'].dt.month

monthly_purchases_2016 = df_2016['Month'].value_counts().sort_index()
monthly_purchases_2017 = df_2017['Month'].value_counts().sort_index()
monthly_purchases_2018 = df_2018['Month'].value_counts().sort_index()

st.subheader('Number of Purchases in 2016-2018')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_purchases_2016.index, monthly_purchases_2016.values, marker='o', color='green', linestyle='-', label='2016')
ax.plot(monthly_purchases_2017.index, monthly_purchases_2017.values, marker='o', color='blue', linestyle='-', label='2017')
ax.plot(monthly_purchases_2018.index, monthly_purchases_2018.values, marker='o', color='red', linestyle='-', label='2018')
ax.set_title('Number of Purchases in 2016-2018')
ax.set_xlabel('Month')
ax.set_ylabel('Number of Purchases')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax.grid(True)
ax.legend()
st.pyplot(fig)

# 4. Number of unique customers placing orders per state each year
merged_data = pd.merge(df1, df, on='customer_id')
merged_data['Year'] = merged_data['order_purchase_timestamp'].dt.year
merged_data['Month'] = merged_data['order_purchase_timestamp'].dt.month

state_customers = merged_data.groupby(['Year', 'customer_state'])['customer_id'].nunique().unstack(fill_value=0)

st.subheader('Number of Unique Customers per State in 2016-2018')
fig, ax = plt.subplots(figsize=(10, 6))
for year in state_customers.index:
    ax.plot(state_customers.columns, state_customers.loc[year], marker='o', label=str(year))
ax.set_title('Number of Unique Customers per State in 2016-2018')
ax.set_xlabel('State')
ax.set_ylabel('Number of Unique Customers')
ax.set_xticks(state_customers.columns)
ax.set_xticklabels(state_customers.columns, rotation=45)
ax.grid(True)
ax.legend(title="Year")
st.pyplot(fig)
