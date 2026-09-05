# -*- coding: utf-8 -*-
"""analisis_preliminar_de_datos.py

Ejecutar desde la carpeta raíz del proyecto (TP_1) con el comando:
python3 -m scr.analisis_preliminar_de_datos

"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('./data/house-prices-tp.csv')
print("\nInfo dataset original:\n")
df.info()
print("\n")
print("#"*70)
print("Primeras 10 filas de df:")
print("#"*70)
print(df.head(10))

print("#"*90)
print("Describe de df:")
print("#"*90)
print(df.describe().T)

#Verificamos si hay registros duplicados
duplicados = df.duplicated().sum()
print("#"*70)
print(f"Cantidad de registros duplicados: {duplicados}")

nulos_por_columna = df.isna().sum()
print("#"*70)
print("Cantidad de nulos por columna:")
print("#"*70)
print(nulos_por_columna)


nulos_por_fila = df.isna().sum(axis=1)
print("#"*70)
print("Cantidad de nulos por fila:")
print("#"*70)
print(nulos_por_fila.value_counts().sort_index())

# Filtra las filas que acumulan más de 5 NaN
filas_mas_5_nulos = df[df.isna().sum(axis=1) > 5]
print(" ")
print("#"*70)
print (f"Filas con más de 5 nulos: {len(filas_mas_5_nulos)}")
print("#"*70)
print(filas_mas_5_nulos)

#Removemos las filas con más de 5 nulos
df_filtrado = df.drop(filas_mas_5_nulos.index).reset_index(drop=True)

print("#"*70)
print("Información de df_filtrado (luego de remover filas con > 5 NaNs):")
print("#"*70)
df_filtrado.info()

print("#"*70)
print("Listado de registros MEDV sin precios (Target):")
print("#"*70)
print(df_filtrado[df_filtrado['MEDV'].isnull()])
#Removemos registros sin precios. Son pocos (4)
df_filtrado = df_filtrado.dropna(subset=['MEDV']).reset_index(drop=True)

print("#"*70)
print("info() de df_filtrado (se remueven registros MEDV=NaN)")
print("#"*70)
print(df_filtrado.info())
print("#"*70)
print("Describe de df_filtrado:")
print("#"*70)
print(df_filtrado.describe().T)

# Visualización de la distribución de la variable objetivo (MEDV)
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.histplot(df["MEDV"].dropna(), kde=True, ax=axes[0])
axes[0].set_title("Distribución de MEDV")
sns.boxplot(x=df["MEDV"].dropna(), ax=axes[1])
axes[1].set_title("Boxplot de MEDV")
plt.tight_layout()
plt.savefig('./outputs/distribucion_medv_pre_imputacion.png', dpi=200)
plt.show()

# Histograma de cada variable numérica
plt.figure(figsize=(18, 12))
df.hist(bins=20, edgecolor='black')
plt.tight_layout()
plt.savefig('./outputs/histogramas_variables_pre_imputacion.png', dpi=200)
plt.show()


#A los valores faltanes se les imputa el valor de sus medianas
df_filtrado = df_filtrado.fillna(df_filtrado.median())
print("#"*70)
print("info() de df_filtrado imputando medianas")
print("#"*70)
print(df_filtrado.info())
print("#"*70)
print("Describe de df_filtrado imputando medianas")
print("#"*70)
print(df_filtrado.describe().T)
print("#"*70)


# Visualización de la distribución de la variable objetivo (MEDV)
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.histplot(df["MEDV"].dropna(), kde=True, ax=axes[0])
axes[0].set_title("Distribución de MEDV")
sns.boxplot(x=df["MEDV"].dropna(), ax=axes[1])
axes[1].set_title("Boxplot de MEDV")
plt.tight_layout()
plt.savefig('./outputs/distribucion_medv_post_imputacion.png', dpi=200)
plt.show()

# Histograma de cada variable numérica
plt.figure(figsize=(18, 12))
df.hist(bins=20, edgecolor='black')
plt.tight_layout()
plt.savefig('./outputs/histogramas_variables_post_imputacion.png', dpi=200)
plt.show()

# Scatterplot entre variables numéricas
scatter_cols = df.columns
pd.plotting.scatter_matrix(df[scatter_cols], figsize=(18, 18), alpha=0.7, diagonal='hist')
plt.tight_layout()
#plt.savefig('./outputs/scatterplot_variables.png', dpi=200)
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
#plt.savefig('./outputs/heatmap_variables.png', dpi=200)
plt.show()

# Boxplot de cada variable para observar cuartiles y outliers
plt.figure(figsize=(18, 12))
df.boxplot(rot=45, patch_artist=True)
plt.title('Boxplot de cada variable')
plt.tight_layout()
plt.savefig('./outputs/boxplot_variables.png', dpi=200)
plt.show()