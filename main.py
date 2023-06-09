# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xvCA1B-HE6-Kdk05TAE07Q991D0L7Ltf

Importing the required libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns

"""Data Collecting and Analysis"""

#loading the csv file as a pandas dataframe
cust_data = pd.read_csv('Online Retail.csv')


#first 5 rows in the dataframe
cust_data.head()

#finding the nummber of rows and columns
cust_data.shape

#getting info about the dataset
cust_data.info
features=['Quantity','UnitPrice']

#chcecking for missing values
cust_data=cust_data.dropna(subset=features)
#data = cust_data[features]
# data.head()

#cust_data_without_nulls1 = cust_data.dropna(subset=['Description','CustomerID'],how='any')
#cust_data_without_nulls.isnull().sum()
# data = ((data-data.min())/(data.max()-data.min()))*9+1
# data.describe()

#cust_data_without_nulls.shape
# data.head()

cust_data.duplicated().sum()

df_pure=cust_data.drop_duplicates()
# df_pure.shape
# df_pure.head()
data = df_pure[features]
data.head()

data = ((data-data.min())/(data.max()-data.min()))*9+1
data.describe()


# df_pure = df_pure.drop('CustomerID',axis=1)
# df_pure.head()

#df_pure.columns
#df_pure.head()
# print(df_pure['Quantity'].min())

"""Choosing the Quantity and Unitprice for KMeans clusternig and storing it in another dataframe"""

X = data.iloc[:,[1,0]].values
print(X)
# print(type(data))

"""Choosing the number of clusters

WCSS = Within Cluster Sum Of Squares
"""

#finding WCSS values for different number of clusters
WCSS=[]

for i in range(1,11):
  kmeans = KMeans(n_clusters=i,n_init=10,init='k-means++',random_state=32)
  kmeans.fit(X)

  WCSS.append(kmeans.inertia_)

#plotting an elbow graph
sns.set()
plt.plot(range(1,11),WCSS)
plt.title('The Elbow Point Graph')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS Value')
plt.show()

"""Optimum Number Of Clusters = 5

Trainning The K-Means Clustering Model
"""

kmeans = KMeans(n_clusters=6,n_init=50,init='k-means++',random_state=32)
#return a label for each data point based on the cluster
Y=kmeans.fit_predict(X)
print(Y)

"""Visualizing all the clusters"""

#plotting all the clusters and their centroids

plt.figure(figsize=(10,10))
plt.scatter(X[Y==0,0],X[Y==0,1],s=50,c='green',label='Cluster 1')
plt.scatter(X[Y==1,0],X[Y==1,1],s=50,c='red',label='Cluster 2')
plt.scatter(X[Y==2,0],X[Y==2,1],s=50,c='blue',label='Cluster 3')
plt.scatter(X[Y==3,0],X[Y==3,1],s=50,c='yellow',label='Cluster 4')
plt.scatter(X[Y==4,0],X[Y==4,1],s=50,c='pink',label='Cluster 5')
plt.scatter(X[Y==5,0],X[Y==5,1],s=50,c='orange',label='Cluster 6')

#Plot the centroids
plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1],s=20,c='black',label='Centroid')
plt.title('Stock Categories')
plt.xlabel('Stock Price')
plt.ylabel('Quantity')
plt.legend()
plt.show()

#now taking input from the user
new_stock_price = float(input("Enter the new stock price "))
new_stock_qty = int(input("Enter the new stock quantity "))
# us_dt = user_data.split()
# N_X = []
# N_X.append(new_stock_price)
# N_X.append(new_stock_qty)
data_prev=df_pure[features]
stock_prices = data_prev['UnitPrice']
quantities = data_prev['Quantity']
min_price = stock_prices.min()

max_price = stock_prices.max()
# print(max_price)
min_qty = quantities.min()
max_qty = quantities.max()

scaled_price = ((new_stock_price - min_price) / (max_price - min_price)) * 9 + 1
scaled_qty = ((new_stock_qty - min_qty) / (max_qty - min_qty)) * 9 + 1
# print(scaled_price)

new_data = [[scaled_price, scaled_qty]]
new_data_cluster = kmeans.predict(new_data)

plt.figure(figsize=(10,10))
plt.scatter(X[Y==0,0],X[Y==0,1],s=50,c='green',label='Cluster 0')
plt.scatter(X[Y==1,0],X[Y==1,1],s=50,c='red',label='Cluster 1')
plt.scatter(X[Y==2,0],X[Y==2,1],s=50,c='blue',label='Cluster 2')
plt.scatter(X[Y==3,0],X[Y==3,1],s=50,c='yellow',label='Cluster 3')
plt.scatter(X[Y==4,0],X[Y==4,1],s=50,c='pink',label='Cluster 4')
plt.scatter(X[Y==5,0],X[Y==5,1],s=50,c='orange',label='Cluster 5')

# Plot the new data point
plt.scatter(scaled_price, scaled_qty, s=50, c='violet', label='New Data Point (Cluster {})'.format(new_data_cluster[0]))

# Plot the centroids
plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1],s=20,c='black',label='Centroid')

plt.title('Stock Categories')
plt.xlabel('Stock Price')
plt.ylabel('Quantity')
plt.legend()
plt.show()

2