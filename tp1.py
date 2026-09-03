import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt




df = pd.read_csv('/home/g/Documents/TUIA/AA1/TP_AA1_Acosta_Hauret_Rinaldi/house-prices-tp.csv')

df.info()

print(df.describe())
print(df.head(10))

# Histograma de cada variable numérica
plt.figure(figsize=(18, 12))
df.hist(bins=20, edgecolor='black')
plt.tight_layout()
plt.savefig('histogramas_variables.png', dpi=200)
plt.show()

# Scatterplot entre variables numéricas
scatter_cols = df.columns
pd.plotting.scatter_matrix(df[scatter_cols], figsize=(18, 18), alpha=0.7, diagonal='hist')
plt.tight_layout()
plt.savefig('scatterplot_variables.png', dpi=200)
plt.show()

# Heatmap de correlación entre todas las variables
corr = df.corr()
plt.figure(figsize=(16, 12))
plt.imshow(corr, cmap='coolwarm', interpolation='nearest')
plt.colorbar(label='Correlación')
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha='right')
plt.yticks(range(len(corr.columns)), corr.columns)
for i in range(len(corr.columns)):
    for j in range(len(corr.columns)):
        plt.text(j, i, f'{corr.iloc[i, j]:.2f}', ha='center', va='center', color='black' if abs(corr.iloc[i, j]) < 0.7 else 'white')
plt.title('Heatmap de correlación')
plt.tight_layout()
plt.savefig('heatmap_variables.png', dpi=200)
plt.show()

# Boxplot de cada variable para observar cuartiles y outliers
plt.figure(figsize=(18, 12))
df.boxplot(rot=45, patch_artist=True)
plt.title('Boxplot de cada variable')
plt.tight_layout()
plt.savefig('boxplot_variables.png', dpi=200)
plt.show()

# Muestra todas las filas donde al menos una columna sea NaN/null
filas_nulas = df[df.isna().any(axis=1)]

print(filas_nulas)
len(filas_nulas)

# Filtra las filas que acumulan más de 3 NaN
filas_mas_3_nulos = df[df.isna().sum(axis=1) > 3]

print(filas_mas_3_nulos)

# Filtra las filas que acumulan más de 5 NaN
filas_mas_5_nulos = df[df.isna().sum(axis=1) > 5]

print(filas_mas_5_nulos)