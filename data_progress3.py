#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from datetime import datetime

url_github = 'https://raw.githubusercontent.com/NationalSpark37/Agrupaciones-y-Agregaci-n-Multinivel-de-Datos-fase-2/refs/heads/main/pipol_dataset%20(2).csv'

df = pd.read_csv(url_github)

print("=" * 80)
print("AGRUPACIONES Y AGREGACION MULTINIVEL DE DATOS")
print("=" * 80)

print("\nDataset original:")
print(df.head(10))
print(f"\nForma del dataset: {df.shape[0]} filas, {df.shape[1]} columnas")

df['birthday'] = pd.to_datetime(df['birthday'], format='%d/%m/%Y')
df['edad'] = datetime.now().year - df['birthday'].dt.year

print("\n" + "=" * 80)
print("1. INFORMACION DEL DATASET")
print("=" * 80)
print(df.info())

print("\n" + "=" * 80)
print("2. PAISES Y CIUDADES DISPONIBLES")
print("=" * 80)
print("Paises:", df['country'].unique())
print("\nCiudades por pais:")
for pais in df['country'].unique():
    ciudades = df[df['country'] == pais]['city'].unique()
    print(f"  {pais}: {list(ciudades)}")

print("\n" + "=" * 80)
print("3. AGRUPACION POR PAIS Y CIUDAD (Mexico y Dusty City)")
print("=" * 80)

busqueda_pais = 'Mexico'
busqueda_ciudad = 'Dusty City'

print(f"\nBuscando personas de {busqueda_pais} y {busqueda_ciudad}...")
filtro = (df['country'] == busqueda_pais) & (df['city'] == busqueda_ciudad)
resultado_filtro = df[filtro]

if len(resultado_filtro) > 0:
    print(f"Se encontraron {len(resultado_filtro)} personas:")
    print(resultado_filtro[['name', 'last_name', 'city', 'country', 'edad']])
else:
    print(f"No se encontraron personas en {busqueda_pais}, {busqueda_ciudad}")
    print("\nMostrando grupos de pais y ciudad disponibles:")

    grupos = df.groupby(['country', 'city']).size()
    print(grupos)

print("\n" + "=" * 80)
print("4. AGRUPACION MULTINIVEL: PAIS Y CIUDAD")
print("=" * 80)

grupos_pais_ciudad = df.groupby(['country', 'city']).agg({
    'name': 'count',
    'edad': ['mean', 'min', 'max']
}).round(2)

grupos_pais_ciudad.columns = ['cantidad_personas', 'edad_promedio', 'edad_minima', 'edad_maxima']

print("\nAgrupacion por Pais y Ciudad:")
print(grupos_pais_ciudad)

print("\n" + "=" * 80)
print("5. AGRUPACION MULTINIVEL DETALLADA")
print("=" * 80)

grupos_multinivel = df.groupby(['country', 'city'])

print(f"\nTotal de grupos (pais, ciudad): {grupos_multinivel.ngroups}")

print("\nDetalles de cada grupo:")
for (pais, ciudad), grupo in grupos_multinivel:
    print(f"\n{pais} - {ciudad}:")
    print(f"  Cantidad de personas: {len(grupo)}")
    print(f"  Edad promedio: {grupo['edad'].mean():.2f}")
    print(f"  Edad minima: {grupo['edad'].min()}")
    print(f"  Edad maxima: {grupo['edad'].max()}")
    print(f"  Personas: {', '.join(grupo['name'].values)}")

print("\n" + "=" * 80)
print("6. EDAD PROMEDIO POR PAIS")
print("=" * 80)

edad_por_pais = df.groupby('country').agg({
    'edad': ['mean', 'count', 'min', 'max', 'std']
}).round(2)

edad_por_pais.columns = ['edad_promedio', 'cantidad_personas', 'edad_minima', 'edad_maxima', 'desviacion_estandar']

print("\nEdad promedio por pais:")
print(edad_por_pais)

print("\n" + "=" * 80)
print("7. USANDO get_group()")
print("=" * 80)

grupos_pais_ciudad_obj = df.groupby(['country', 'city'])

paises_disponibles = df['country'].unique()
ciudades_por_pais = df.groupby('country')['city'].unique()

print("Ejemplos de get_group():")

for pais in paises_disponibles[:3]:
    ciudades = ciudades_por_pais[pais]
    if len(ciudades) > 0:
        ciudad = ciudades[0]
        try:
            grupo = grupos_pais_ciudad_obj.get_group((pais, ciudad))
            print(f"\nGrupo: ({pais}, {ciudad})")
            print(f"Cantidad de registros: {len(grupo)}")
            print(f"Nombres: {', '.join(grupo['name'].values)}")
        except KeyError:
            print(f"No existe el grupo ({pais}, {ciudad})")

print("\n" + "=" * 80)
print("8. AGREGACIONES MULTIPLES CON .agg()")
print("=" * 80)

agregaciones = df.groupby('country').agg({
    'edad': ['mean', 'median', 'min', 'max', 'count'],
    'name': 'count'
}).round(2)

agregaciones.columns = ['edad_promedio', 'edad_mediana', 'edad_minima', 'edad_maxima', 'edad_count', 'total_personas']

print("\nAgregaciones multiples por pais:")
print(agregaciones)

print("\n" + "=" * 80)
print("9. RESUMEN FINAL")
print("=" * 80)

total_personas = len(df)
total_paises = df['country'].nunique()
total_ciudades = df['city'].nunique()
edad_promedio_general = df['edad'].mean()

print(f"Total de personas: {total_personas}")
print(f"Total de paises: {total_paises}")
print(f"Total de ciudades: {total_ciudades}")
print(f"Edad promedio general: {edad_promedio_general:.2f}")

print("\nPrograma finalizado correctamente")
print("=" * 80)


# In[ ]:




