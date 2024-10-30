# 1 Inicio
# 1.1 Importar las librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1.2 Abrir los archivos CSV
df_cash = pd.read_csv('extract - cash request - data analyst.csv')
df_fees = pd.read_csv('extract - fees - data analyst - .csv')

# 1.3 Mostrar las primeras filas de los DataFrames
print("\n\033[1m\033[95mPARTE 1: Primeras filas\033[0m")
print("Cash head:")
print(df_cash.head())
print("Fees head:")
print(df_fees.head())
print(df_fees.columns)

# 2. Información de los DataFrames
# 2.1 Mostrar información de los tipos de datos
print("\n\033[1m\033[95mPARTE 2: Descripción estadística\033[0m")
df_cash.info()
df_fees.info()

# 2.2 Mostrar descripción estadística
print("Descripción estadística de Cash:")
print(df_cash.describe())
print("Descripción estadística de Fees:")
print(df_fees.describe())

# 3. Limpiar fechas para agrupar por meses
# 3.1 Definir las columnas de fechas para Cash y Fees
print("\n\033[1m\033[95mPARTE 3: Agrupar por meses\033[0m")
date_columns_cash = [
    'created_at', 'updated_at', 'moderated_at', 
    'reimbursement_date', 'cash_request_received_date', 
    'money_back_date', 'send_at', 'reco_creation', 
    'reco_last_update'
]
date_columns_fees = ['created_at', 'updated_at', 'paid_at', 'from_date', 'to_date']

# 3.2 Convertir y normalizar las fechas con pd.to_datetime
for col in date_columns_cash:
    df_cash[col] = pd.to_datetime(df_cash[col], errors='coerce').dt.normalize()
for col in date_columns_fees:
    df_fees[col] = pd.to_datetime(df_fees[col], errors='coerce').dt.normalize()

# 4. Tipos de datos de Cash Requests
print("\n\033[1m\033[95mPARTE 4: Tipos de datos cash request\033[0m")
print("PARTE 4: Tipos de datos cash request:")
print("\nTipos de datos de Cash Requests:")
print(df_cash[date_columns_cash].dtypes)
print("\nTipos de datos de Fees:")
print(df_fees[date_columns_fees].dtypes)

# 5.1 Ordenar por 'created_at' en ambos DataFrames
df_cash_sorted = df_cash.sort_values(by='created_at', ascending=True)
df_fees_sorted = df_fees.sort_values(by='created_at', ascending=True)

# 5.2 Mostrar los primeros resultados después de ordenar
print("\n\033[1m\033[95mPARTE 5: Resultados después de ordenar\033[0m")
print("Cash sorted by created_at:")
print(df_cash_sorted.head())
print("Fees sorted by created_at:")
print(df_fees_sorted.head())

# 6
print("\n\033[1m\033[95mPARTE 6: Sustituir user_id vacíos por deleted_account_id\033[0m")
# 6.1 Llenar valores nulos de 'user_id' con 'deleted_account_id'
df_cash['user_id'] = df_cash['user_id'].fillna(df_cash['deleted_account_id'])

# 6.2 Eliminar filas con user_id aún nulos
df_cash = df_cash[~df_cash['user_id'].isna()]

# 6.3 Agrupar por user_id y obtener la primera fecha de created_at
cohorts = df_cash.groupby('user_id')['created_at'].min().reset_index()
cohorts.rename(columns={'created_at': 'first_created_at'}, inplace=True)

# 6.4 Crear una nueva columna con el formato de mes y año
cohorts['cohort'] = cohorts['first_created_at'].dt.to_period('M').astype(str)

# 6.5 Unir los cohorts al DataFrame original
df_cash = df_cash.merge(cohorts[['user_id', 'cohort']], on='user_id', how='left')

# 6.6 Mostrar los primeros resultados para verificar
print("PARTE 6:")
print(df_cash[['user_id', 'created_at', 'cohort']].head())

# 7. Ordenar el DataFrame df_cash por la columna created_at
df_cash_sorted = df_cash.sort_values(by='created_at', ascending=True)

# 7.1 Mostrar los primeros resultados después de ordenar
print("\n\033[1m\033[95mPARTE 7: Ordenar\033[0m")
print("DataFrame ordenado por created_at:")
print(df_cash_sorted[['user_id', 'created_at', 'cohort', 'deleted_account_id']])

# 8. Gráfico - Distribución de cohorts
print("\n\033[1m\033[95mPARTE 8: Distribución de cohorts\033[0m")
cohort_counts = df_cash.groupby('cohort')['user_id'].nunique()

# 8.1 Visualización de la distribución de usuarios por cohort
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=cohort_counts.index.astype(str), y=cohort_counts.values, palette='Set2')
plt.title('Distribución de usuarios por cohort')
plt.xlabel('Cohort (mes y año)')
plt.ylabel('Número de usuarios únicos')
plt.xticks(rotation=45)

# 8.2 Añadir la cantidad total arriba de cada columna
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=12)
plt.show()

# 9.1 Distribución de los estados actuales
print("\n\033[1m\033[95mPARTE 9: Distribución de estados\033[0m")
status_distribution = df_cash['status'].value_counts()
print("\nDistribución de los estados de las solicitudes de caja:")
print(status_distribution)

# 9.2 Visualización de la distribución de los estados
plt.figure(figsize=(10, 6))
ax = sns.countplot(x='status', data=df_cash, palette='Set2', hue='status', legend=False)  # Asignar hue
plt.title('Distribución de los Estados de las Solicitudes de Caja')
plt.xlabel('Estado de la Solicitud')
plt.ylabel('Número de Solicitudes')
plt.xticks(rotation=45)

# 9.3 Añadir la cantidad total arriba de cada barra
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='bottom', fontsize=12)
plt.show()

# 10 Frecuencia media por cohort
print("\n\033[1m\033[95mPARTE 10: Frecuencia media por cohorte\033[0m")
df_cash['created_at'] = pd.to_datetime(df_cash['created_at'])
df_cash['cohort'] = pd.to_datetime(df_cash['cohort'], format='%Y-%m')

# 10.1 Filtrar usuarios que han hecho más de una solicitud, excluyendo 'rejected'
user_counts = df_cash['user_id'].value_counts()
multiple_requests_users = user_counts[user_counts > 1].index
df_cash_filtered = df_cash[(df_cash['status'] != 'rejected') & (df_cash['user_id'].isin(user_counts[user_counts > 1].index))]

# 10.2 Calcular la frecuencia por usuario como la diferencia entre solicitudes
df_cash_filtered = df_cash_filtered.sort_values(by=['user_id', 'created_at'])
df_cash_filtered['days_between'] = df_cash_filtered.groupby('user_id')['created_at'].diff().dt.days.dropna()

# 10.3 Calcular el número de usuarios que solo han hecho una solicitud por cohort
single_request_users = user_counts[user_counts == 1].index
df_cash_single_request = df_cash[df_cash['user_id'].isin(single_request_users) & (df_cash['status'] != 'rejected')]
single_request_count = df_cash_single_request.groupby('cohort')['user_id'].nunique().reset_index(name='single_request_count')

# 10.4 Visualizar el diagrama de cajas por cohort, añadiendo valores clave
plt.figure(figsize=(12, 8))
box_plot = sns.boxplot(x='cohort', y='days_between', data=df_cash_filtered, palette='Set2')

# Calcular y añadir valores clave como cuartiles, mediana, media, máximo y mínimo
stats = df_cash_filtered.groupby('cohort')['days_between'].describe()
for i, cohort in enumerate(stats.index):
    median = stats.loc[cohort, '50%']
    q1 = stats.loc[cohort, '25%']
    q3 = stats.loc[cohort, '75%']
    mean = stats.loc[cohort, 'mean']
    minimum = stats.loc[cohort, 'min']
    maximum = stats.loc[cohort, 'max']
    
    # Desplazar la etiqueta
    box_plot.annotate(f'Med: {median:.1f}\nMedia: {mean:.1f}\nQ1: {q1:.1f}\nQ3: {q3:.1f}\nMin: {minimum:.1f}\nMax: {maximum:.1f}', 
                      xy=(i, median), 
                      xytext=(i + 0.1, median + 2),
                      arrowprops=dict(arrowstyle='->', lw=1.5))

plt.title('Distribución de Días Entre Solicitudes por Cohorte')
plt.xlabel('Cohorte (Mes y Año)')
plt.ylabel('Días Entre Solicitudes')
plt.xticks(rotation=45)
plt.show()


# 11. Analizar los ingresos generados por cohorte
print("\n\033[1m\033[95mPARTE 11: Analizar ingresos generados por cohorte\033[0m")

df_combinados = df_fees.merge(df_cash[['id', 'cohort']], left_on='cash_request_id', right_on='id', how='left')
df_combinados.head()
df_aprobados = df_combinados[(df_combinados['status'] == 'accepted')]
ingresos_generados = df_aprobados[["total_amount", "cohort"]].groupby("cohort").sum()
ingresos_generados
plt.figure(figsize=(10, 6))

# Corregimos el warning asignando 'cohort' a 'hue' y ocultando la leyenda
graf_ing = sns.barplot(x='cohort', y='total_amount', hue='cohort', data=ingresos_generados, palette='Set2', legend=False)

# Título y etiquetas
plt.title('Ingresos generados por cohorte')
plt.xlabel('Cohorte (mes y año)')
plt.ylabel('Ingresos totales')
plt.xticks(rotation=45)

# Añadimos las etiquetas con la cantidad total encima de cada barra
for p in graf_ing.patches:
    graf_ing.annotate(f'{int(p.get_height())}',  # Mostramos la cantidad sin decimales
                      (p.get_x() + p.get_width() / 2., p.get_height()),  # Posición de la etiqueta
                      ha='center', va='bottom', fontsize=12)  # Alineación y tamaño de fuente

# Mostrar el gráfico
plt.show()

# 12. Distribución de estado por cohorte
print("\n\033[1m\033[95mPARTE 12: Distribución de estado por cohorte\033[0m")
cohort_status_counts = df_cash.pivot_table(index='cohort', columns='status', aggfunc='size', fill_value=0)
cohort_status_counts.plot(kind='bar', stacked=True, figsize=(10, 6))

# Configuramos el título y las etiquetas
plt.title('Distribución de estados por cohorte')
plt.xlabel('Cohorte')
plt.ylabel('Número de registros')
plt.xticks(rotation=45)

# Mostramos el gráfico
plt.legend(title='Estado')
plt.tight_layout()  # Ajusta el layout
plt.show()

# 13. Tasas de incidentes por cohorte en %
print("\n\033[1m\033[95mPARTE 13: Tasas de incidentes por cohorte en %\033[0m")
# Agregamos una fila con los totales para cada cohorte
cohort_status_counts.loc['Total'] = cohort_status_counts.sum()
# Mostramos el DataFrame con los totales
display(cohort_status_counts)

# Filtrar solo los incidentes de pago (todos los estados excepto los mencionados)
incident_status = ['rejected', 'failed', 'canceled', 'error',  'direct_debit_rejected', 'direct_debit_sent', 'transaction_declined']
incident_df = df_cash[df_cash['status'].isin(incident_status)]
# Contar el número de incidentes por cohorte
incident_counts = incident_df.groupby('cohort')['status'].count().reset_index(name='incidents_count')
# Obtener el total de solicitudes por cohorte
total_requests = df_cash.groupby('cohort')['status'].count().reset_index(name='total_count')
# Combinar ambas tablas para calcular la tasa de incidentes
cohort_incident_rate = incident_counts.merge(total_requests, on='cohort')
cohort_incident_rate['incident_rate'] = (cohort_incident_rate['incidents_count'] / cohort_incident_rate['total_count']) * 100
# Mostrar la tasa de incidentes por cohorte
print("Tasa de incidentes por cohorte (%):")
display(cohort_incident_rate[['cohort', 'incident_rate']])
# Visualización de la tasa de incidentes por cohorte
plt.figure(figsize=(10, 6))
sns.barplot(x='cohort', y='incident_rate', data=cohort_incident_rate, palette='Set2')
plt.xticks(rotation=45)
plt.title('Tasa de incidentes por cohorte (%)')
plt.xlabel('Cohorte (Mes y Año)')
plt.ylabel('Tasa de incidentes (%)')
plt.show()

# 14. Porcentaje de incidentes por cohorte y tipo de estado
print("\n\033[1m\033[95mPARTE 14: Porcentaje de incidentes por cohorte y tipo de estado\033[0m")
incident_status2 = ['rejected', 'failed', 'canceled', 'error', 'direct_debit_rejected', 'direct_debit_sent', 'transaction_declined']
incident_df = df_cash[df_cash['status'].isin(incident_status2)]
# Contar el número de incidentes por cohorte y tipo de estado
incident_counts2 = incident_df.groupby(['cohort', 'status']).size().reset_index(name='incidents_count')
# Obtener el total de incidentes por cohorte para calcular el porcentaje
total_incidents_per_cohort = incident_counts2.groupby('cohort')['incidents_count'].sum().reset_index(name='total_incidents')
# Combinar las tablas para calcular el porcentaje
incident_counts2 = incident_counts2.merge(total_incidents_per_cohort, on='cohort')
incident_counts2['percentage'] = (incident_counts2['incidents_count'] / incident_counts2['total_incidents']) * 100

# Visualización de los incidentes como porcentajes por cohorte y tipo de estado
plt.figure(figsize=(12, 8))
bar_plot = sns.barplot(data=incident_counts2, x='cohort', y='percentage', hue='status', palette='Set2')
plt.xticks(rotation=45)
plt.title('Porcentaje de incidentes por cohorte y tipo de estado')
plt.xlabel('Cohorte (Mes y Año)')
plt.ylabel('Porcentaje de incidentes (%)')
plt.legend(title='Tipo de incidente')
# Agregar los valores de porcentaje encima de las barras
for p in bar_plot.patches:
    bar_plot.annotate(f'{p.get_height():.1f}%',
                      (p.get_x() + p.get_width() / 2., p.get_height()),
                      ha='center', va='bottom',
                      fontsize=10, color='black',
                      xytext=(0, 5),  # Desplazamiento vertical
                      textcoords='offset points')
plt.tight_layout()
plt.show()

# 15. Porcentaje de incidentes por cohorte y tipo de estado apilado
print("\n\033[1m\033[95mPARTE 15: Porcentaje de incidentes por cohorte y tipo de estado apilado\033[0m")
incident_status2 = ['rejected', 'failed', 'canceled', 'error', 'direct_debit_rejected', 'direct_debit_sent', 'transaction_declined']
incident_df = df_cash[df_cash['status'].isin(incident_status2)]
# Contar el número de incidentes por cohorte y tipo de estado
incident_counts2 = incident_df.groupby(['cohort', 'status']).size().reset_index(name='incidents_count')
# Obtener el total de incidentes por cohorte para calcular el porcentaje
total_incidents_per_cohort = incident_counts2.groupby('cohort')['incidents_count'].sum().reset_index(name='total_incidents')
# Combinar las tablas para calcular el porcentaje
incident_counts2 = incident_counts2.merge(total_incidents_per_cohort, on='cohort')
incident_counts2['percentage'] = (incident_counts2['incidents_count'] / incident_counts2['total_incidents']) * 100
# Visualización de los incidentes como porcentajes por cohorte y tipo de estado (gráfico apilado)
plt.figure(figsize=(14, 8))
# Usamos pivot_table para reestructurar el DataFrame
incident_pivot = incident_counts2.pivot_table(index='cohort', columns='status', values='percentage', fill_value=0)
# Graficar como un gráfico de barras apiladas
incident_pivot.plot(kind='bar', stacked=True, ax=plt.gca(), colormap='Set2')
plt.xticks(rotation=45)
plt.title('Porcentaje de incidentes por cohorte y tipo de estado (Gráfico Apilado)')
plt.xlabel('Cohorte (Mes y Año)')
plt.ylabel('Porcentaje de incidentes (%)')
plt.legend(title='Tipo de incidente')
plt.tight_layout()
plt.show()

# 16. Desglose de incidencias por tipo y cantidad
print("\n\033[1m\033[95mPARTE 16: Desglose de incidencias por tipo y cantidad\033[0m")

incident_pivot = incident_counts2.pivot_table(index='cohort', columns='status', values='incidents_count', fill_value=0)

# Agrupar por cohorte y obtener la cantidad total de incidentes
cohort_incidents = incident_counts2.groupby('cohort').agg(
    total_incidents=('incidents_count', 'sum')
).reset_index()

# Crear una figura y un eje
fig, ax1 = plt.subplots(figsize=(14, 8))

# Graficar las barras apiladas para la cantidad de incidencias por tipo de incidente usando una paleta más atractiva
incident_pivot.plot(kind='bar', stacked=True, ax=ax1, colormap='Paired')

# Establecer el título y etiquetas del eje y para el gráfico de barras
ax1.set_xlabel('Cohorte (Mes y Año)', fontsize=12)
ax1.set_ylabel('Cantidad de Incidencias por Tipo', fontsize=12)
plt.xticks(rotation=45)

# Añadir los porcentajes dentro de las barras, desplazándolos a la derecha y en negro
for i in range(len(incident_pivot)):
    total = cohort_incidents['total_incidents'].iloc[i]  # Total de incidencias por cohorte
    bottom = 0  # Inicializamos la posición inferior para apilar
    for j, val in enumerate(incident_pivot.iloc[i]):
        if val > 0:
            percentage = (val / total) * 100
            ax1.text(i + 0.3, bottom + val / 2, f'{percentage:.1f}%', ha='left', va='center', color='black', fontsize=10)  # Cambiar a color negro
            bottom += val  # Actualizamos la posición inferior para la siguiente parte de la barra

# Crear un segundo eje y para la cantidad total de incidencias
ax2 = ax1.twinx()

# Graficar una línea para la cantidad total de incidencias por cohorte
sns.lineplot(x='cohort', y='total_incidents', data=cohort_incidents, ax=ax2, color='red', marker='o')

# Establecer etiquetas para el segundo eje y (cantidad total de incidencias)
ax2.set_ylabel('Cantidad Total de Incidencias', fontsize=12, color='red')
ax2.tick_params('y', colors='red')

# Añadir los valores totales por encima de las barras y almacenar las coordenadas para la línea
y_values = []
for i, total in enumerate(cohort_incidents['total_incidents']):
    ax2.text(i, total + 5, f'{int(total)}', ha='center', color='red', fontsize=12)
    y_values.append(total)  # Almacenar los valores para la línea

# Graficar la línea que conecta los totales
ax2.plot(cohort_incidents.index, y_values, color='red', linestyle='--', linewidth=1.5)

# Asegurar que ambos ejes compartan la misma escala
ax2.set_ylim(ax1.get_ylim())

# Título del gráfico
plt.title('Cantidad Total de Incidencias (Línea) y Porcentaje por Tipo de Incidencia (Barras Apiladas) por Cohorte', fontsize=16)

# Ajustar el diseño
plt.tight_layout()

# Mostrar el gráfico
plt.show()
