
# 1. Importar les llibreries necessàries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# 2. Obrir els fitxers CSV
df_cash = pd.read_csv('extract - cash request - data analyst.csv')
df_fees = pd.read_csv('extract - fees - data analyst - .csv')
# 3. Mostrar les primeres files dels DataFrames
# print("Cash head:")
# print(df_cash.head())
# print("Fees head:")
# print(df_fees.head())
# 4. Informació dels DataFrames
# 4.1 Mostrar informació dels tipus de dades
# df_cash.info()
# df_fees.info()
# 4.2 Mostrar descripció estadística
# print("Descripció estadística de Cash:")
# print(df_cash.describe())
# print("Descripció estadística de Fees:")
# print(df_fees.describe())
# 5. Netejar dates per agrupar per mesos
# 5.1 Definir les columnes de dates per Cash i Fees
date_columns_cash = [
    'created_at', 'updated_at', 'moderated_at',
    'reimbursement_date', 'cash_request_received_date',
    'money_back_date', 'send_at', 'reco_creation',
    'reco_last_update'
]
date_columns_fees = ['created_at', 'updated_at', 'paid_at', 'from_date', 'to_date']
# 5.2 Convertir les dates amb pd.to_datetime per Cash
for i in date_columns_cash:
    df_cash[i] = pd.to_datetime(df_cash[i], errors='coerce')
# 5.3 Convertir les dates amb pd.to_datetime per Fees
for k in date_columns_fees:
    df_fees[k] = pd.to_datetime(df_fees[k], errors='coerce')
# 6. Normalitzar les dates (eliminar hora) per Cash
for i in date_columns_cash:
    df_cash[i] = df_cash[i].dt.normalize()
# 7. Normalitzar les dates (eliminar hora) per Fees
for k in date_columns_fees:
    df_fees[k] = df_fees[k].dt.normalize()
# 8. Mostrar les dates modificades
# print("Cash head amb dates canviades:")
# print(df_cash.head())
# print("Fees head amb dates canviades:")
# print(df_fees.head())
# 9. Tipus de dades de Cash Requests
# 9.1 Mostrar tipus de dades de les dates de Cash
# print("\nTipus de dades de Cash Requests:")
# print(df_cash[date_columns_cash].dtypes)
# 9.2 Mostrar tipus de dades de les dates de Fees
# print("\nTipus de dades de Fees:")
# print(df_fees[date_columns_fees].dtypes)
# 10. Ordenar per 'created_at' en ambdós DataFrames
# 10.1 Ordenar df_cash
df_cash_sorted = df_cash.sort_values(by='created_at', ascending=True)
# 10.2 Ordenar df_fees
df_fees_sorted = df_fees.sort_values(by='created_at', ascending=True)
# 11. Mostrar els primers resultats després de ordenar
# print("Cash sorted by created_at:")
# print(df_cash_sorted.head())
# print("Fees sorted by created_at:")
# print(df_fees_sorted.head())
# 12. Omplir valors nuls de 'user_id' amb 'deleted_account_id'
df_cash['user_id'] = df_cash['user_id'].fillna(df_cash['deleted_account_id'])
# 13. Agrupar per user_id i obtenir la primera data de created_at
# 13.1 Agrupació per 'user_id'

cohorts = df_cash.groupby('user_id')['created_at'].min().reset_index()

# 13.2 Renombrar la columna per fer-la més descriptiva
cohorts.rename(columns={'created_at': 'first_created_at'}, inplace=True)

# 14. Crear una nova columna amb el format de mes i any
# 14.1 Convertir la primera data a període de mes
cohorts['cohort'] = cohorts['first_created_at'].dt.to_period('M').astype(str)
# 15. Unir els cohortes al DataFrame original
df_cash = df_cash.merge(cohorts[['user_id', 'cohort']], on='user_id', how='left')
# 16. Mostrar els primers resultats per verificar
# print(df_cash[['user_id', 'created_at', 'cohort']].head())
# 17. Ordenar el DataFrame df_cash per la columna created_at
df_cash_sorted = df_cash.sort_values(by='created_at', ascending=True)
# 18. Mostrar els primers resultats després d'ordenar
# print("DataFrame ordenat per created_at:")
# display(df_cash_sorted[['user_id', 'created_at', 'cohort', 'deleted_account_id']])
# 19. Grafico - Distribució de cohorts
# 19.1 Calcular la distribució de cohorts
cohort_counts = df_cash.groupby('cohort')['user_id'].nunique()
# 19.2 Visualització de la distribució d'usuaris per cohort (mes i any)

# print(cohorts['first_created_at'].head())
print ("df cash de muestra")
display (df_cash)

print ("df fees de muestra")
display (df_fees)


print("Grafico de distribución de usuarios por cohorte")
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=cohort_counts.index.astype(str), y=cohort_counts.values, palette='Set2')
plt.title('Distribució d\'usuaris per cohort')
plt.xlabel('Cohort (mes i any)')
plt.ylabel('Nombre d\'usuaris únics')
plt.xticks(rotation=45)
# 19.3 Afegeix la quantitat total a dalt de cada columna
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=12)
# 19.4 Mostrar el gràfic
plt.show()
# 20. Mostrar el total de la distribució de cohorts
total_cohort_users = cohort_counts.sum()
# print("Total cohort users:")
# print(total_cohort_users)
# 21. Distribució dels estats actuals
# 21.1 Calcular la distribució dels estats
status_distribution = df_cash['status'].value_counts()
# print("\nDistribució dels estats de les sol·licituds de caixa:")
# display(status_distribution)
# 21.2 Visualització de la distribució dels estats
plt.figure(figsize=(10, 6))
ax = sns.countplot(x='status', data=df_cash, palette='Set2')
plt.title('Distribució dels Estats de les Sol·licituds de Caixa')
plt.xlabel('Estat de la Sol·licitud')
plt.ylabel('Nombre de Sol·licituds')
plt.xticks(rotation=45)
# 21.3 Afegeix la quantitat total a dalt de cada barra
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=12)
# 21.4 Mostrar el gràfic
plt.show()



print ("#----------------------------------FRECUENCIA SEGUN USUARIO")


# 1. Agrupar por 'user_id' y calcular la primera y última fecha de 'created_at'
date_info = df_cash.groupby('user_id')['created_at'].agg(['min', 'max', 'count']).reset_index()

# 2. Calcular la diferencia en días
date_info['date_difference'] = (date_info['max'] - date_info['min']).dt.days

# 3. Calcular la frecuencia
date_info['frecuencia'] = date_info['date_difference'] // date_info['count']

# 4. Unir esta información al DataFrame original
df_cash = df_cash.merge(date_info[['user_id', 'frecuencia']], on='user_id', how='left')

# Mostrar los primeros resultados para verificar
print("DataFrame con la nueva columna de frecuencia:")
display(df_cash[['user_id', 'created_at', 'frecuencia']])
#----------------------------------FRECUENCIA SEGUN USUARIO

print ("#-----------------------------------Frecuencia segun cohorte")


# Asegúrate de que el DataFrame ya tiene las columnas 'cohort' y 'frecuencia'

# 1. Agrupar por cohorte y calcular la media de la frecuencia
cohort_frequencies = df_cash.groupby('cohort')['frecuencia'].mean().reset_index()

# 2. Visualizar la frecuencia promedio por cohorte
plt.figure(figsize=(10, 6))
sns.barplot(x='cohort', y='frecuencia', data=cohort_frequencies)
plt.xticks(rotation=45)
plt.title('Frecuencia promedio de uso de adelantos de efectivo por cohorte')
plt.xlabel('Cohorte (Mes y Año)')
plt.ylabel('Frecuencia promedio (días)')
plt.show()
#-----------------------------------Frecuencia segun cohorte

# 6. Analizar cómo evoluciona la frecuencia a lo largo del tiempo para cada cohorte (usuarios con más de una solicitud)
df_cash_filtered = df_cash_filtered.assign(
    created_at_month=df_cash_filtered['created_at'].dt.to_period('M').astype(str)
)

# Primero, agrupar también por el mes de la solicitud para ver la evolución de la frecuencia
df_cash_filtered['created_at_month'] = df_cash_filtered['created_at'].dt.to_period('M').astype(str)

# Agrupar por cohorte y el mes de la solicitud, para ver la evolución de la frecuencia
cohort_monthly_frequencies_filtered = df_cash_filtered.groupby(['cohort', 'created_at_month'])['frecuencia'].mean().reset_index()





# 7. Visualizar la evolución de la frecuencia de uso a lo largo del tiempo por cohorte (solo usuarios con más de una solicitud)
plt.figure(figsize=(12, 8))
sns.lineplot(x='created_at_month', y='frecuencia', hue='cohort', data=cohort_monthly_frequencies_filtered, marker='o')
plt.xticks(rotation=45)
plt.title('Evolución de la frecuencia de uso a lo largo del tiempo por cohorte (Usuarios con más de una solicitud)')
plt.xlabel('Mes de Solicitud (Mes y Año)')
plt.ylabel('Frecuencia promedio (días)')
Text(0, 0.5, 'Frecuencia promedio (días)')

print ("#------------------------ingresos según cohorte")

# Configuración del gráfico
plt.figure(figsize=(10, 6))

# Crear la gráfica de barras (descomentar esta línea para definir graf_ing)
graf_ing = sns.barplot(x='cohort', y='total_amount', data=Ingresos_generados.reset_index(), palette='Set2')

# Título y etiquetas
plt.title('Ingresos generados por cohorte')
plt.xlabel('Cohorte (mes y año)')
plt.ylabel('Ingresos totales')
plt.xticks(rotation=45)

# Añadir etiquetas con la cantidad total encima de cada barra
for p in graf_ing.patches:
    graf_ing.annotate(f'{int(p.get_height())}',  # Muestra la cantidad sin decimales
                      (p.get_x() + p.get_width() / 2., p.get_height()),  # Posición de la etiqueta
                      ha='center', va='bottom', fontsize=12)  # Alineación y tamaño de fuente

# Mostrar el gráfico
plt.show()
#------------------------ingresos según cohorte

# 3. Analizar cómo evoluciona la frecuencia a lo largo del tiempo para cada cohorte

# Primero, necesitamos agrupar también por la fecha en la que se hizo cada solicitud para cada cohorte
df_cash['created_at_month'] = df_cash['created_at'].dt.to_period('M').astype(str)

# Agrupar por cohorte y el mes en que se hizo la solicitud, para ver la evolución de la frecuencia
cohort_monthly_frequencies = df_cash.groupby(['cohort', 'created_at_month'])['frecuencia'].mean().reset_index()

# 4. Visualizar la evolución de la frecuencia de uso a lo largo del tiempo para cada cohorte
plt.figure(figsize=(12, 8))
sns.lineplot(x='created_at_month', y='frecuencia', hue='cohort', data=cohort_monthly_frequencies, marker='o')
plt.xticks(rotation=45)
plt.title('Evolución de la frecuencia de uso a lo largo del tiempo por cohorte')
plt.xlabel('Mes de Solicitud (Mes y Año)')
plt.ylabel('Frecuencia promedio (días)')
plt.legend(title='Cohorte', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 1. Contar cuántas veces ha hecho una solicitud cada 'user_id'
user_counts = df_cash.groupby('user_id')['created_at'].count().reset_index()

# 2. Filtrar los usuarios que han realizado más de una solicitud
user_counts = user_counts[user_counts['created_at'] > 1]

# 3. Unir de nuevo esta información con el DataFrame original para excluir a los usuarios con una sola compra
df_cash_filtered = df_cash[df_cash['user_id'].isin(user_counts['user_id'])]

# 4. Agrupar por cohorte y calcular la media de la frecuencia para los usuarios que hicieron más de una solicitud
cohort_frequencies_filtered = df_cash_filtered.groupby('cohort')['frecuencia'].mean().reset_index()

# 5. Visualizar la frecuencia promedio por cohorte (solo para usuarios con más de una solicitud)
plt.figure(figsize=(10, 6))
sns.barplot(x='cohort', y='frecuencia', data=cohort_frequencies_filtered)
plt.xticks(rotation=45)
plt.title('Frecuencia promedio de uso de adelantos de efectivo por cohorte (Usuarios con más de una solicitud)')
plt.xlabel('Cohorte (Mes y Año)')
plt.ylabel('Frecuencia promedio (días)')
plt.show()

print ("#-------------------tasa de insidencias")




cohort_status_counts = df_cash.pivot_table(index='cohort', columns='status', aggfunc='size', fill_value=0)
# Agregamos una fila con los totales para cada cohorte
cohort_status_counts.loc['Total'] = cohort_status_counts.sum()
# Mostramos el DataFrame con los totales
display(cohort_status_counts)

# Filtrar solo los incidentes de pago (todos los status excepto los mencionados)
incident_status = ['rejected', 'failed', 'canceled', 'error',  'direct_debit_rejected', 'direct_debit_sent', 'transaction_declined'
]  # Ejemplo de posibles estados de incidentes
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
#-------------------tasa de insidencias

#14 ------------------Flor test
print("\n\033[1m\033[95mPARTE 14: Flor Porcentaje de incidentes por cohorte y tipo de estado\033[0m")
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

# Visualización de los incidentes como porcentajes por cohorte y tipo de estado (gráfico apilado)
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
print("Porcentaje de incidentes por cohorte y tipo de estado")
display (incident_pivot)

# Graficar como un gráfico de barras apiladas
incident_pivot.plot(kind='bar', stacked=True, ax=plt.gca(), colormap='Set2')
plt.xticks(rotation=45)
plt.title('Porcentaje de incidentes por cohorte y tipo de estado (Gráfico Apilado)')
plt.xlabel('Cohorte (Mes y Año)')
plt.ylabel('Porcentaje de incidentes (%)')
plt.legend(title='Tipo de incidente')
plt.tight_layout()
plt.show()

# Parte 16: Desgloce de incidencias por tipo y cantidad
print("\n\033[1m\033[95mPARTE 16: Desgloce de incidencias por tipo y cantidad\033[0m")

# Crear una tabla pivote para obtener la cantidad de incidencias por cohorte y tipo de incidencia
incident_pivot = incident_counts2.pivot_table(index='cohort', columns='status', values='incidents_count', fill_value=0)

# Agrupar por cohorte y obtener la cantidad total de incidentes
cohort_incidents = incident_counts2.groupby('cohort').agg(total_incidents=('incidents_count', 'sum')).reset_index()

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
