
# K-Means and Hierarchical Clustering on Sales Data

# 1. Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering

from scipy.cluster.hierarchy import dendrogram, linkage

# 2. Load Dataset
df = pd.read_csv("sales_data.csv")

print("Original Dataset:")
print(df.head())

# 3. Preprocessing
df = df.dropna()
df = df.drop_duplicates()

# Select Features
X = df[["Sales", "Profit"]]

# 4. Standardize Data
scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# 5. Elbow Method
wcss = []

for k in range(1, 11):

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    kmeans.fit(X_scaled)

    wcss.append(kmeans.inertia_)

# Plot Elbow Graph
plt.plot(range(1, 11), wcss, marker="o")

plt.title("Elbow Method")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("WCSS")
plt.grid()
plt.show()

# 6. Apply K-Means Clustering
k = 3

kmeans = KMeans(
    n_clusters=k,
    random_state=42,
    n_init=10
)

df["KMeans_Cluster"] = kmeans.fit_predict(X_scaled)

print("\nK-Means Clustering:")
print(df)

# Visualize K-Means Clusters
plt.figure(figsize=(8, 5))

sns.scatterplot(
    x=X["Sales"],
    y=X["Profit"],
    hue=df["KMeans_Cluster"],
    palette="viridis",
    s=100
)

plt.title("K-Means Clustering")
plt.xlabel("Sales")
plt.ylabel("Profit")
plt.show()

# 7. Hierarchical Clustering
linked = linkage(X_scaled, method="ward")

# Plot Dendrogram
plt.figure(figsize=(10, 5))

dendrogram(linked)

plt.title("Hierarchical Clustering Dendrogram")
plt.xlabel("Data Points")
plt.ylabel("Euclidean Distance")
plt.show()

# 8. Apply Agglomerative Clustering
hc = AgglomerativeClustering(
    n_clusters=k,
    linkage="ward"
)

df["Hierarchical_Cluster"] = hc.fit_predict(X_scaled)

print("\nHierarchical Clustering:")
print(df)

# Visualize Hierarchical Clusters
plt.figure(figsize=(8, 5))

sns.scatterplot(
    x=X["Sales"],
    y=X["Profit"],
    hue=df["Hierarchical_Cluster"],
    palette="viridis",
    s=100
)

plt.title("Hierarchical Clustering")
plt.xlabel("Sales")
plt.ylabel("Profit")
plt.show()

# 9. Display Final Results
print("\nFinal Cluster Results:")
print(df)
