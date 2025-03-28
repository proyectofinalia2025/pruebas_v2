# -*- coding: utf-8 -*-
"""protecto_final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ulPwAgIYGWxCMGYDqS6O_VibWCgb-6C3

#IMPORTACIÓN DE LAS BIBLIOTECAS
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import drive
import matplotlib.ticker as mtick
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

"""#CARGA DE DATOS"""

drive.mount('/content/drive')

file_path = "/content/drive/MyDrive/base proyecto final.xlsx"
df = pd.read_excel(file_path)
df

df['GRADUADOS'].plot(kind='box', title='Distribución de Graduados')

plt.figure(figsize=(10, 6))
plt.hist(df['GRADUADOS'], bins=100, color='skyblue', edgecolor='black')
plt.title('Distribución de Graduados')
plt.xlabel('Graduados')
plt.ylabel('Frecuencia')
plt.show()

df['GRADUADOS'].value_counts().sort_index()

df[df['NIVEL DE FORMACIÓN']=='Doctorado'].shape

"""# EXPLORAR DATASET

"""

df.info()

df.describe()

df.head()

"""# LIMPIEZA DE DATOS"""

df['ÁREA DE CONOCIMIENTO'].value_counts()

df.replace("Sin información", np.nan, inplace=True)

df.isnull().sum()

columna = "ÁREA DE CONOCIMIENTO"
porcentaje_nulos = df[columna].isnull().mean() * 100
print(f"El {porcentaje_nulos:.2f}% de los datos en la columna '{columna}' son nulos.")
#Por ser un porcentaje bajo, decidimos eliminar las filas nulas

df.dropna(subset=["ÁREA DE CONOCIMIENTO"], inplace=True)

print(df["ÁREA DE CONOCIMIENTO"].isnull().sum())

df.shape

df.size

# Borrado de columnas
df2 = df.drop(['ID SECTOR IES', 'ID NIVEL DE FORMACIÓN', 'ID ÁREA'], axis=1)

df2.columns

df2.shape

df2.size

"""df2.head()"""

df2_grouped_año_graduados = df2.groupby("AÑO DE GRADO")["GRADUADOS"].sum().reset_index()
df2_grouped_año_graduados

df2_grouped_ingreso_graduados = df.groupby("INGRESO")["GRADUADOS"].sum().reset_index()
df2_grouped_ingreso_graduados

"""# **ANALISIS UNIVARIADO**

## **Frecuencia de las categorías**

#### Área de Conocimiento
"""

plt.figure(figsize=(15, 3))

# Graficar la suma de GRADUADOS por cada área de conocimiento
ax = sns.barplot(data=df2, x='ÁREA DE CONOCIMIENTO', y='GRADUADOS', palette='Paired', estimator=sum,)

# Formatear el eje Y para mostrar los valores en millones
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))

plt.xticks(rotation=80)
plt.title('Distribución de Graduados por Área de Conocimiento')
plt.ylabel('Graduados (millones)')
plt.show()

"""#### Nivel de Formación"""

plt.figure(figsize=(8, 6))

# Usar barplot para sumar los valores de GRADUADOS por cada nivel de formación
ax = sns.barplot(data=df2, x='NIVEL DE FORMACIÓN', y='GRADUADOS', palette='Set2', estimator=sum)

# Formatear el eje Y para mostrar los valores en millones
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))

plt.xticks(rotation=75)
plt.title('Distribución de Graduados por Nivel de Formación')
plt.ylabel('Graduados (millones)')
plt.show()

"""#### Sexo"""

# Calcular la sumatoria de GRADUADOS por SEXO
sexo_counts = df2.groupby('SEXO')['GRADUADOS'].sum()
print(sexo_counts)

# Calcular la sumatoria de GRADUADOS por ÁREA DE CONOCIMIENTO
conocimiento_counts = df2.groupby('ÁREA DE CONOCIMIENTO')['GRADUADOS'].sum()
print(conocimiento_counts)

# Calcular la sumatoria de GRADUADOS por SEXO
sexo_counts = df2.groupby('SEXO')['GRADUADOS'].sum()

# Definir función para mostrar el porcentaje y el valor absoluto
def porcentaje_y_absoluto(pct, total_vals):
    total = sum(total_vals)
    abs_val = int(round(pct * total / 100.0))  # Valor absoluto redondeado
    return f"{pct:.1f}%\n({abs_val:,})"

plt.figure(figsize=(7, 7))

# Crear gráfico de pastel con valores absolutos y porcentajes
plt.pie(sexo_counts, labels=sexo_counts.index, startangle=90,
        colors=['#ff9999','#66b3ff'],
        autopct=lambda pct: porcentaje_y_absoluto(pct, sexo_counts),
        wedgeprops={'edgecolor': 'black'})

# Agregar el título con la suma total de graduados
suma_total = sexo_counts.sum()
plt.title(f'Distribución de Graduados por Sexo\nTotal Graduados: {suma_total:,}', fontsize=14, color='blue')

# Asegurar que la gráfica sea circular
plt.axis('equal')

# Mostrar la gráfica
plt.show()

"""#### Ingreso (salarios minimos)"""

# Calcular la sumatoria de GRADUADOS por INGRESO
ingreso_counts = df2.groupby('INGRESO')['GRADUADOS'].sum()
print(ingreso_counts)

plt.figure(figsize=(8, 6))

# Agrupar por INGRESO y sumar GRADUADOS
ingreso_counts = df2.groupby('INGRESO')['GRADUADOS'].sum().reset_index()

# Ordenar el dataframe por INGRESO de menor a mayor
ingreso_counts = ingreso_counts.sort_values(by='INGRESO')

# Crear el gráfico de barras con la sumatoria de GRADUADOS
ax = sns.barplot(data=ingreso_counts, x='INGRESO', y='GRADUADOS', palette='Set2')

# Formatear el eje Y para mostrar valores en millones
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))

plt.xticks(rotation=75)
plt.title('Distribución de Graduados según Ingreso en Salarios Mínimos')
plt.ylabel('Graduados (millones)')
plt.xlabel('Ingreso (Salarios Mínimos)')
plt.show()

"""#### Graduados"""

suma = df2["GRADUADOS"].sum()
print(suma)

# Calcular la sumatoria de GRADUADOS por INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)
institucion_counts = df2.groupby('INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)')['GRADUADOS'].sum()
print(institucion_counts)

"""#### Intitución Educativa"""

plt.figure(figsize=(12, 6))

# Agrupar por IES y sumar GRADUADOS
institucion_counts = df2.groupby('INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)')['GRADUADOS'].sum()

# Seleccionar el Top 20 de instituciones con más graduados
top_20_instituciones = institucion_counts.sort_values(ascending=False).head(20)

# Crear gráfico de barras con la sumatoria de GRADUADOS en el Top 20 de IES
ax = sns.barplot(x=top_20_instituciones.values, y=top_20_instituciones.index, palette='viridis')

# Formatear el eje X para mostrar valores en miles
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x/1e3:.1f}K'))

plt.title('Top 20 Instituciones de Educación Superior con Más Graduados')
plt.xlabel('Graduados (miles)')
plt.ylabel('Institución')
plt.show()

"""# ANALISIS BIVARIADO"""

plt.figure(figsize=(8, 6))

# Crear boxplot de graduados por sexo
ax = sns.boxplot(data=df2, x='SEXO', y='GRADUADOS', palette='coolwarm')

# Calcular la sumatoria de graduados por sexo
sexo_counts = df2.groupby('SEXO')['GRADUADOS'].sum()

# Agregar etiquetas con la sumatoria encima del gráfico
for i, sexo in enumerate(sexo_counts.index):
    ax.text(i, sexo_counts[sexo], f'{sexo_counts[sexo]:,}', ha='center', va='bottom', fontsize=12, color='black')

plt.title('Graduados por Sexo')
plt.ylabel('Número de Graduados')
plt.xlabel('Sexo')
plt.show()

plt.figure(figsize=(14, 7))

# Crear boxplot de graduados por área de conocimiento
ax = sns.boxplot(data=df2, x='ÁREA DE CONOCIMIENTO', y='GRADUADOS', palette='Spectral')

# Calcular la sumatoria de graduados por área de conocimiento
area_counts = df2.groupby('ÁREA DE CONOCIMIENTO')['GRADUADOS'].sum()

# Agregar etiquetas con la sumatoria en miles encima del gráfico
for i, area in enumerate(area_counts.index):
    ax.text(i, area_counts[area], f'{area_counts[area] / 1e3:.1f}K',
            ha='center', va='bottom', fontsize=10, color='black', rotation=90)

# Ajustar el eje Y para mostrar valores en miles
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x/1e3:.1f}K'))

plt.xticks(rotation=90)
plt.title('Graduados por Área de Conocimiento')
plt.ylabel('Número de Graduados (miles)')
plt.xlabel('Área de Conocimiento')
plt.show()

# Calcular la sumatoria de graduados por Nivel de Formación y Sexo
formacion_counts = df2.groupby(['NIVEL DE FORMACIÓN', 'SEXO'])['GRADUADOS'].sum().reset_index()

# Determinar si mostrar en miles (K) o millones (M)
max_value = formacion_counts['GRADUADOS'].max()
scale_factor = 1e6 if max_value >= 1e6 else 1e3
unit = "M" if max_value >= 1e6 else "K"

# Crear el gráfico
g = sns.catplot(data=formacion_counts, x='NIVEL DE FORMACIÓN', y='GRADUADOS', hue='SEXO', kind='bar', palette='Set2', height=6, aspect=2)

# Obtener el eje
ax = g.ax

# Agregar etiquetas con la sumatoria en miles o millones sobre cada barra
for p in ax.patches:
    ax.annotate(f'{p.get_height()/scale_factor:.1f}{unit}',
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=10, color='black')

# Ajustar el eje Y para mostrar valores en miles o millones
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x/scale_factor:.1f}{unit}'))

plt.xticks(rotation=90)
plt.title('Distribución de Nivel de Formación por Sexo')
plt.ylabel(f'Número de Graduados ({unit})')
plt.xlabel('Nivel de Formación')
plt.show()

# Calcular la sumatoria de graduados por Ingreso y Sexo
ingreso_counts = df2.groupby(['INGRESO', 'SEXO'])['GRADUADOS'].sum().reset_index()

# Determinar si mostrar en miles (K) o millones (M)
max_value = ingreso_counts['GRADUADOS'].max()
scale_factor = 1e6 if max_value >= 1e6 else 1e3
unit = "M" if max_value >= 1e6 else "K"

# Crear el gráfico
g = sns.catplot(data=ingreso_counts, x='INGRESO', y='GRADUADOS', hue='SEXO', kind='bar', palette='Set2', height=6, aspect=2)

# Obtener el eje
ax = g.ax

# Agregar etiquetas con la sumatoria en miles o millones sobre cada barra
for p in ax.patches:
    ax.annotate(f'{p.get_height()/scale_factor:.1f}{unit}',
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=10, color='black')

# Ajustar el eje Y para mostrar valores en miles o millones
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x/scale_factor:.1f}{unit}'))

plt.xticks(rotation=90)
plt.title('Distribución de Ingresos por Sexo')
plt.ylabel(f'Número de Graduados ({unit})')
plt.xlabel('Ingreso')
plt.show()

# Calcular la sumatoria de graduados por Nivel de Formación y Sexo
formacion_counts = df2.groupby(['NIVEL DE FORMACIÓN', 'SEXO'])['GRADUADOS'].sum().reset_index()

# Determinar si mostrar en miles (K) o millones (M)
max_value = formacion_counts['GRADUADOS'].max()
scale_factor = 1e6 if max_value >= 1e6 else 1e3
unit = "M" if max_value >= 1e6 else "K"

# Crear el gráfico
g = sns.catplot(data=formacion_counts, x='NIVEL DE FORMACIÓN', y='GRADUADOS', hue='SEXO', kind='bar', palette='Set2', height=6, aspect=2)

# Obtener el eje
ax = g.ax

# Agregar etiquetas con la sumatoria en miles o millones sobre cada barra
for p in ax.patches:
    ax.annotate(f'{p.get_height()/scale_factor:.1f}{unit}',
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=10, color='black')

# Ajustar el eje Y para mostrar valores en miles o millones
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x/scale_factor:.1f}{unit}'))

plt.xticks(rotation=90)
plt.title('Distribución de Nivel de Formación por Sexo')
plt.ylabel(f'Número de Graduados ({unit})')
plt.xlabel('Nivel de Formación')
plt.show()

# Calcular la sumatoria de graduados por Ingreso y Sexo
ingreso_counts = df2.groupby(['INGRESO', 'SEXO'])['GRADUADOS'].sum().reset_index()

# Determinar si mostrar en miles (K) o millones (M)
max_value = ingreso_counts['GRADUADOS'].max()
scale_factor = 1e6 if max_value >= 1e6 else 1e3
unit = "M" if max_value >= 1e6 else "K"

# Crear el gráfico
g = sns.catplot(data=ingreso_counts, kind='bar', x='GRADUADOS', y='INGRESO', hue='SEXO', palette='Set2', height=6, aspect=2, orient='h')

# Obtener el eje
ax = g.ax

# Agregar etiquetas con la sumatoria en miles o millones sobre cada barra
for p in ax.patches:
    ax.annotate(f'{p.get_width()/scale_factor:.1f}{unit}',
                (p.get_width(), p.get_y() + p.get_height() / 2),
                ha='left', va='center', fontsize=10, color='black')

# Ajustar el eje X para mostrar valores en miles o millones
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x/scale_factor:.1f}{unit}'))

plt.title('Distribución de Graduados por Ingreso y Sexo')
plt.xlabel(f'Número de Graduados ({unit})')
plt.ylabel('Ingreso')
plt.show()

"""INGRESOS POR ÁREA DEL CONOCIMIENTO"""

# Agrupar por Área de Conocimiento e Ingreso, sumando los graduados
df_grouped = df2.groupby(["ÁREA DE CONOCIMIENTO", "INGRESO"])["GRADUADOS"].sum().reset_index()

plt.figure(figsize=(14, 7))

# Crear gráfico de burbujas
sns.scatterplot(data=df_grouped,
                x="ÁREA DE CONOCIMIENTO",
                y="INGRESO",
                size="GRADUADOS",
                hue="ÁREA DE CONOCIMIENTO",
                sizes=(20, 1000),  # Escalar tamaño de burbujas
                palette="coolwarm",
                edgecolor="black", alpha=0.7)

# Rotar etiquetas y mejorar visualización
plt.xticks(rotation=90, ha="right")
plt.title("Relación de Ingresos por Área de Conocimiento considerando Graduados")
plt.xlabel("Área de Conocimiento")
plt.ylabel("Ingreso")
plt.legend(title="Área de Conocimiento", bbox_to_anchor=(1, 1), loc="upper left")

plt.grid(True, linestyle="--", alpha=0.5)
plt.show()

# Agrupar y sumar graduados por año
df2_grouped = df2.groupby("AÑO DE GRADO")["GRADUADOS"].sum().reset_index()

# Variables para graficar
X = df2_grouped["AÑO DE GRADO"]
Y = df2_grouped["GRADUADOS"]

# Determinar si mostrar valores en miles o millones
scale_factor = 1e6 if Y.max() >= 1e6 else 1e3
unit = "M" if Y.max() >= 1e6 else "K"

# Graficar la línea
plt.figure(figsize=(10, 5))
plt.plot(X, Y / scale_factor, color='g', marker='o', linestyle='-', linewidth=2, markersize=6)

# Mejorar la visualización
plt.grid(True, linestyle='--', alpha=0.7)
plt.title("Evolución de Graduados por Año", fontsize=14, fontweight='bold')
plt.xlabel("Año de Grado", fontsize=12)
plt.ylabel(f"Número de Graduados ({unit})", fontsize=12)

# Formatear el eje Y en miles o millones
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.1f}{unit}'))

plt.show()

"""# **VISTAS MULTIPLES**"""

# Asegurar que GRADUADOS es numérico
df2['GRADUADOS'] = pd.to_numeric(df2['GRADUADOS'], errors='coerce').fillna(0)

# Agrupar por AÑO DE GRADO y ÁREA DE CONOCIMIENTO para sumar graduados
df2_grouped = df2.groupby(["AÑO DE GRADO", "ÁREA DE CONOCIMIENTO"])["GRADUADOS"].sum().reset_index()

# Determinar si mostrar valores en miles o millones
scale_factor = 1e6 if df2_grouped["GRADUADOS"].max() >= 1e6 else 1e3
unit = "M" if df2_grouped["GRADUADOS"].max() >= 1e6 else "K"

# Crear la gráfica de dispersión
plt.figure(figsize=(10,6))
sns.scatterplot(
    data=df2_grouped,
    x="AÑO DE GRADO",
    y=df2_grouped["GRADUADOS"] / scale_factor,  # Convertir a miles o millones
    hue="ÁREA DE CONOCIMIENTO",
    palette="tab10",
    alpha=0.7,
    s=100  # Tamaño de los puntos
)

# Mejoras visuales
plt.title("Graduados por Año y Área de Conocimiento", fontsize=14, fontweight='bold')
plt.xlabel("Año de Grado", fontsize=12)
plt.ylabel(f"Número de Graduados ({unit})", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

# Formatear el eje Y
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.1f}{unit}'))

plt.show()

g = sns.FacetGrid(df2, col="SEXO", hue="ÁREA DE CONOCIMIENTO", height=5, aspect=1.2)
g.map(sns.scatterplot, "AÑO DE GRADO", "GRADUADOS", alpha=0.6)
g.add_legend()
plt.show()

# Asegurar que GRADUADOS es numérico
df2['GRADUADOS'] = pd.to_numeric(df2['GRADUADOS'], errors='coerce').fillna(0)

# Agrupar por AÑO DE GRADO, SEXO y ÁREA DE CONOCIMIENTO para sumar los graduados
df2_grouped = df2.groupby(["AÑO DE GRADO", "SEXO", "ÁREA DE CONOCIMIENTO"])["GRADUADOS"].sum().reset_index()

# Crear el FacetGrid con datos agrupados
g = sns.FacetGrid(df2_grouped, col="SEXO", hue="ÁREA DE CONOCIMIENTO", height=5, aspect=1.2)
g.map(sns.scatterplot, "AÑO DE GRADO", "GRADUADOS", alpha=0.6, s=100)  # s=100 para mayor visibilidad

# Agregar la leyenda
g.add_legend()

# Mejorar etiquetas
g.set_axis_labels("Año de Grado", "Número de Graduados")
g.fig.suptitle("Graduados por Año, Sexo y Área de Conocimiento", fontsize=14, fontweight='bold')

plt.show()

# Asegurar que GRADUADOS es numérico
df2['GRADUADOS'] = pd.to_numeric(df2['GRADUADOS'], errors='coerce').fillna(0)

# Agrupar por AÑO DE GRADO y NIVEL DE FORMACIÓN sumando los graduados
df2_grouped = df2.groupby(["AÑO DE GRADO", "NIVEL DE FORMACIÓN"])["GRADUADOS"].sum().reset_index()

# Determinar la escala adecuada (miles o millones)
max_value = df2_grouped["GRADUADOS"].max()
if max_value >= 1e6:
    scale_factor = 1e6
    unit = "M"
elif max_value >= 1e3:
    scale_factor = 1e3
    unit = "K"
else:
    scale_factor = 1
    unit = ""

# Ajustar los valores al formato elegido
df2_grouped["GRADUADOS"] /= scale_factor

# Crear el gráfico de líneas con la suma de graduados ajustada
plt.figure(figsize=(10, 5))
sns.lineplot(data=df2_grouped, x="AÑO DE GRADO", y="GRADUADOS", hue="NIVEL DE FORMACIÓN", marker="o")

# Formatear el eje Y
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:.1f}{unit}"))

# Mejorar título y etiquetas
plt.title("Evolución de los niveles de formación a lo largo del tiempo", fontsize=14, fontweight='bold')
plt.xlabel("Año de Grado")
plt.ylabel(f"Número de Graduados ({unit})")
plt.grid(True)

plt.show()

# Asegurar que GRADUADOS es numérico
df2['GRADUADOS'] = pd.to_numeric(df2['GRADUADOS'], errors='coerce').fillna(0)

# Agrupar por AÑO DE GRADO y NIVEL DE FORMACIÓN sumando GRADUADOS
df2_grouped = df2.groupby(["AÑO DE GRADO", "NIVEL DE FORMACIÓN"])["GRADUADOS"].sum().reset_index()

# Determinar la escala adecuada (miles o millones)
max_value = df2_grouped["GRADUADOS"].max()
if max_value >= 1e6:
    scale_factor = 1e6
    unit = "M"
elif max_value >= 1e3:
    scale_factor = 1e3
    unit = "K"
else:
    scale_factor = 1
    unit = ""

# Ajustar los valores al formato elegido
df2_grouped["GRADUADOS"] /= scale_factor

# Crear el gráfico de líneas con la suma de graduados ajustada
plt.figure(figsize=(10, 5))
sns.lineplot(data=df2_grouped, x="AÑO DE GRADO", y="GRADUADOS", hue="NIVEL DE FORMACIÓN", marker="o")

# Formatear el eje Y
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:.1f}{unit}"))

# Mejorar título y etiquetas
plt.title("Número de graduados por nivel de formación a lo largo del tiempo", fontsize=14, fontweight='bold')
plt.xlabel("Año de Grado")
plt.ylabel(f"Número de Graduados ({unit})")
plt.grid(True)

plt.show()

# Asegurar que GRADUADOS es numérico
df2['GRADUADOS'] = pd.to_numeric(df2['GRADUADOS'], errors='coerce').fillna(0)

# Agrupar por Año de Grado, Ingreso y Área de Conocimiento sumando Graduados
df2_grouped = df2.groupby(["AÑO DE GRADO", "INGRESO", "ÁREA DE CONOCIMIENTO"])["GRADUADOS"].sum().reset_index()

# Normalizar el tamaño de los puntos (escala adaptable)
df2_grouped["size"] = (df2_grouped["GRADUADOS"] / df2_grouped["GRADUADOS"].max()) * 300  # Ajuste de tamaño relativo

# Crear el scatter plot con tamaño proporcional a Graduados
sns.set_style("white")
g = sns.relplot(
    data=df2_grouped,
    x="AÑO DE GRADO",
    y="INGRESO",
    hue="ÁREA DE CONOCIMIENTO",
    size="GRADUADOS",
    sizes=(10, 300),  # Tamaño mínimo y máximo de los puntos
    kind="scatter",
    aspect=1.5,
    height=6,
    palette="tab10"
)

# Ajustar la leyenda
g._legend.set_bbox_to_anchor((1, 1))
g._legend.set_title("Área de Conocimiento")
g._legend.get_frame().set_alpha(0.9)

# Mejorar visualización del eje X
g.ax.set_xticklabels(g.ax.get_xticklabels(), rotation=45)

# Agregar grid para mejor lectura
plt.grid(True, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)

plt.title("Distribución de Ingresos por Año y Área de Conocimiento (Tamaño = Graduados)", fontsize=14, fontweight='bold')
plt.show()

# Asegurar que GRADUADOS es numérico
df2['GRADUADOS'] = pd.to_numeric(df2['GRADUADOS'], errors='coerce').fillna(0)

# Obtener las 3 áreas de conocimiento con más graduados
top_3_areas = df2.groupby("ÁREA DE CONOCIMIENTO")["GRADUADOS"].sum().nlargest(3)

# Mostrar resultado de manera clara
print("\n🔹 **Top 3 Áreas de Conocimiento con Más Graduados** 🔹\n")
for area, total in top_3_areas.items():
    print(f"📌 {area}: {total:,.0f} graduados")

# Asegurar que GRADUADOS es numérico
df["GRADUADOS"] = pd.to_numeric(df["GRADUADOS"], errors="coerce").fillna(0)

# Filtrar las áreas de conocimiento relevantes
df_filtrado = df[df["ÁREA DE CONOCIMIENTO"].isin([
    "Economía, administración, contaduría y afines",
    "Ingeniería, arquitectura, urbanismo y afines",
    "Ciencias de la educación"
])]

# Agrupar y sumar GRADUADOS para asegurar que los valores sean correctos
df_filtrado = df_filtrado.groupby(
    ["AÑO DE GRADO", "INGRESO", "SEXO", "SECTOR IES", "ÁREA DE CONOCIMIENTO"]
)["GRADUADOS"].sum().reset_index()

# Crear el gráfico
g = sns.relplot(
    data=df_filtrado,
    x="AÑO DE GRADO",
    y="INGRESO",
    hue="SEXO",
    size="GRADUADOS",
    style="SECTOR IES",
    col="ÁREA DE CONOCIMIENTO",
    col_wrap=3,
    height=5,
    aspect=1.5
)

# Ordenar la variable 'INGRESO' si es categórica
df["INGRESO"] = pd.Categorical(df["INGRESO"], ordered=True)

# Crear la gráfica usando countplot en lugar de displot
g = sns.catplot(
    data=df,
    x="INGRESO",
    col="SEXO",
    kind="count",  # Usamos countplot porque 'INGRESO' es categórico
    height=5,
    aspect=1.5,
    color="blue"
)

# Ajustar etiquetas del eje X
for ax in g.axes.flat:
    ax.set_xticklabels(ax.get_xticklabels(), rotation=60, ha="right")

plt.show()

# Asegurar que "AÑO DE GRADO" sea numérico
df["AÑO DE GRADO"] = pd.to_numeric(df["AÑO DE GRADO"], errors="coerce")

# Crear la gráfica KDE
g = sns.displot(
    data=df,
    x="AÑO DE GRADO",
    kind="kde",
    rug=True,  # Muestra marcas en el eje X
    col="SECTOR IES",
    height=5,
    aspect=1.5
)

# Ajustar etiquetas y mejorar la visualización
for ax in g.axes.flat:
    ax.set_xlim(df["AÑO DE GRADO"].min(), df["AÑO DE GRADO"].max())  # Asegurar escala correcta
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

plt.show()

# Crear la serie con la suma de graduados por ingreso
ingreso_counts = df2.groupby("INGRESO")["GRADUADOS"].sum()

# Definir función para mostrar el porcentaje y la cantidad real
def porcentaje_y_absoluto(pct, total_vals):
    total = sum(total_vals)
    abs_val = int(round(pct * total / 100.0))  # Valor absoluto redondeado
    return f"{pct:.1f}%\n({abs_val:,})"

# Crear el gráfico de torta
plt.figure(figsize=(10, 8))
colors = ['skyblue', 'lightcoral', 'lightgreen', "cyan", "blueviolet", "magenta", "orange"]

plt.pie(
    ingreso_counts,
    labels=ingreso_counts.index,
    autopct=lambda pct: porcentaje_y_absoluto(pct, ingreso_counts),
    startangle=90,
    colors=colors,
    wedgeprops={'edgecolor': 'black'}
)

# Añadir el título con la suma total
suma_total = ingreso_counts.sum()
plt.title(f'Distribución de Ingresos\nTotal Graduados: {suma_total:,}', fontsize=14, color='blue')

# Asegurar que la torta sea circular
plt.axis('equal')

# Mostrar la gráfica
plt.show()

"""**COLUMNAS CONVERTIDOS A CODIGO NUMERICO**"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Crea una instancia de LabelEncoder
label_encoder = LabelEncoder()

# Listar las columnas categóricas
categorical_columns = [
    'INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)', 'SECTOR IES',
    'PROGRAMA ACADÉMICO', 'NIVEL ACADÉMICO', 'NIVEL DE FORMACIÓN',
    'ÁREA DE CONOCIMIENTO', 'SEXO', 'INGRESO'
]

# Aplica el LabelEncoder a cada columna categórica
for col in categorical_columns:
    df2[col] = label_encoder.fit_transform(df2[col].astype(str))

# Verifica los cambios
print(df2.head())

df2['INGRESO'].unique()

from sklearn.preprocessing import KBinsDiscretizer

# Definir el discretizador para 4 categorías
kbins = KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='uniform')

# Transformar la columna 'INGRESO' y sobrescribirla con los nuevos valores
df2['INGRESO'] = kbins.fit_transform(df2[['INGRESO']]).astype(int)

# Ver distribución después del agrupamiento
print(df2['INGRESO'].value_counts()) 

"""**MODELO: ARBOL DE DECISIONES**"""

from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTEENN
from sklearn.ensemble import RandomForestClassifier  # Importamos el Random Forest
import xgboost as xgb  # Importamos XGBoost
import lightgbm as lgb
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import EarlyStopping
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.tree import plot_tree
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTETomek

from imblearn.over_sampling import RandomOverSampler
import pandas as pd

# Asumir que df2 es tu DataFrame
X = df2.drop('INGRESO', axis=1)  # Eliminar la columna de la variable objetivo
y = df2['INGRESO']  # Columna objetivo

# Crear un modelo de RandomOverSampler
ros = RandomOverSampler(random_state=42)

# Ajustar el resampling
X_resampled, y_resampled = ros.fit_resample(X, y)

# Verifica el balanceo
print(y_resampled.value_counts())

#oversampling

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Crear el modelo de árbol de decisión
arbol = DecisionTreeClassifier(criterion='entropy', max_depth=5, random_state=42)

# Entrenar el modelo
arbol.fit(X_train, y_train)

# Hacer predicciones
y_pred = arbol.predict(X_test)

# Evaluar el modelo
accuracy = accuracy_score(y_test, y_pred)
print(f'Precisión del modelo: {accuracy:.2f}')
print(classification_report(y_test, y_pred))

# Visualizar el árbol de decisión
plt.figure(figsize=(20,10))
plot_tree(arbol, feature_names=X_resampled.columns, class_names=[str(c) for c in y_resampled.unique()], filled=True)
plt.show()

#subsampling

# Aplicar submuestreo (undersampling)
rus = RandomUnderSampler(random_state=42)
X_resampled, y_resampled = rus.fit_resample(X, y)

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Crear el modelo de árbol de decisión
arbol = DecisionTreeClassifier(criterion='entropy', max_depth=5, random_state=42)

# Entrenar el modelo
arbol.fit(X_train, y_train)

# Hacer predicciones
y_pred = arbol.predict(X_test)

# Evaluar el modelo
accuracy = accuracy_score(y_test, y_pred)
print(f'Precisión del modelo: {accuracy:.2f}')
print(classification_report(y_test, y_pred))

# Visualizar el árbol de decisión
plt.figure(figsize=(20,10))
plot_tree(arbol, feature_names=X_resampled.columns, class_names=[str(c) for c in y_resampled.unique()], filled=True)
plt.show()

#combinacion

# Aplicar combinación de sobremuestreo (SMOTE) y submuestreo (Tomek Links)
smt = SMOTETomek(random_state=42)
X_resampled, y_resampled = smt.fit_resample(X, y)

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Crear el modelo de árbol de decisión
arbol = DecisionTreeClassifier(criterion='entropy', max_depth=5, random_state=42)

# Entrenar el modelo
arbol.fit(X_train, y_train)

# Hacer predicciones
y_pred = arbol.predict(X_test)

# Evaluar el modelo
accuracy = accuracy_score(y_test, y_pred)
print(f'Precisión del modelo: {accuracy:.2f}')
print(classification_report(y_test, y_pred))

# Visualizar el árbol de decisión
plt.figure(figsize=(20,10))
plot_tree(arbol, feature_names=X_resampled.columns, class_names=[str(c) for c in y_resampled.unique()], filled=True)
plt.show()

#random forest

from imblearn.combine import SMOTETomek
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Aplicar SMOTE + Tomek Links para balanceo mejorado
smt = SMOTETomek(random_state=42)
X_resampled, y_resampled = smt.fit_resample(X, y)

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Crear el modelo Random Forest optimizado
random_forest = RandomForestClassifier(
    n_estimators=500,  # Más árboles para mejorar estabilidad
    criterion='entropy',
    max_depth=None,  # Sin límite de profundidad
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1  # Usa todos los núcleos del procesador
)

# Entrenar el modelo
random_forest.fit(X_train, y_train)

# Hacer predicciones
y_pred = random_forest.predict(X_test)

# Evaluar el modelo
accuracy = accuracy_score(y_test, y_pred)
print(f'Precisión del modelo: {accuracy:.2f}')
print(classification_report(y_test, y_pred))

from xgboost import XGBClassifier
from imblearn.combine import SMOTETomek
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Aplicar SMOTE + Tomek Links para balanceo
smt = SMOTETomek(random_state=42)
X_resampled, y_resampled = smt.fit_resample(X, y)

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Crear el modelo XGBoost optimizado
xgb_model = XGBClassifier(
    n_estimators=1000,  # Más árboles
    max_depth=10,  # Profundidad optimizada
    learning_rate=0.05,  # Tasa de aprendizaje ajustada
    subsample=0.8,  # Submuestreo para evitar sobreajuste
    colsample_bytree=0.8,  # Evita que un árbol use todas las variables
    eval_metric='mlogloss',
    use_label_encoder=False,
    random_state=42
)

# Entrenar el modelo
xgb_model.fit(X_train, y_train)

# Hacer predicciones
y_pred = xgb_model.predict(X_test)

# Evaluar el modelo
accuracy = accuracy_score(y_test, y_pred)
print(f'Precisión del modelo: {accuracy:.2f}')
print(classification_report(y_test, y_pred))