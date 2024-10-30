# 1. Importar les llibreries necessàries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Obrir els fitxers CSV
df_cash = pd.read_csv('extract - cash request - data analyst.csv')
df_fees = pd.read_csv('extract - fees - data analyst - .csv')

# 3. Mostrar les primeres files dels DataFrames
print("Cash head:")
print(df_cash.head())
print("Fees head:")
print(df_fees.head())

# 4. Informació dels DataFrames
# 4.1 Mostrar informació dels tipus de dades
df_cash.info()
df_fees.info()

# 4.2 Mostrar descripció estadística
print("Descripció estadística de Cash:")
print(df_cash.describe())
print("Descripció estadística de Fees:")
print(df_fees.describe())

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
print("Cash head amb dates canviades:")
print(df_cash.head())
print("Fees head amb dates canviades:")
print(df_fees.head())

# 9. Tipus de dades de Cash Requests
# 9.1 Mostrar tipus de dades de les dates de Cash
print("\nTipus de dades de Cash Requests:")
print(df_cash[date_columns_cash].dtypes)

# 9.2 Mostrar tipus de dades de les dates de Fees
print("\nTipus de dades de Fees:")
print(df_fees[date_columns_fees].dtypes)

# 10. Ordenar per 'created_at' en ambdós DataFrames
# 10.1 Ordenar df_cash
df_cash_sorted = df_cash.sort_values(by='created_at', ascending=True)

# 10.2 Ordenar df_fees
df_fees_sorted = df_fees.sort_values(by='created_at', ascending=True)

# 11. Mostrar els primers resultats després de ordenar
print("Cash sorted by created_at:")
print(df_cash_sorted.head())
print("Fees sorted by created_at:")
print(df_fees_sorted.head())

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
print(df_cash[['user_id', 'created_at', 'cohort']].head())

# 17. Ordenar el DataFrame df_cash per la columna created_at
df_cash_sorted = df_cash.sort_values(by='created_at', ascending=True)

# 18. Mostrar els primers resultats després d'ordenar
print("DataFrame ordenat per created_at:")
display(df_cash_sorted[['user_id', 'created_at', 'cohort', 'deleted_account_id']])

# 19. Grafico - Distribució de cohorts
# 19.1 Calcular la distribució de cohorts
cohort_counts = df_cash.groupby('cohort')['user_id'].nunique()

# 19.2 Visualització de la distribució d'usuaris per cohort (mes i any)
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
print("Total cohort users:")
print(total_cohort_users)

# 21. Distribució dels estats actuals
# 21.1 Calcular la distribució dels estats
status_distribution = df_cash['status'].value_counts()
print("\nDistribució dels estats de les sol·licituds de caixa:")
display(status_distribution)

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

#-------------------------------------------- Gabi's versión

# 22.1: Crear una base de datos con la diferencia entre fechas de uso por user_id y deleted_account_id
# Ordenar por 'account_id' y 'created_at' para calcular las diferencias correctamente
df_cash_sorted = df_cash.sort_values(by=['user_id', 'created_at'])

# Calcular las diferencias en días entre las fechas de uso
df_cash_sorted['date_difference'] = df_cash_sorted.groupby('user_id')['created_at'].diff().dt.days

# Crear una nueva columna para el account_id que tenga en cuenta ambos tipos de cuentas
df_cash_sorted['account_id'] = df_cash_sorted['user_id'].combine_first(df_cash_sorted['deleted_account_id'])

# Filtrar las columnas necesarias y quitar NaNs
# Asegurarse de incluir los eliminados en el análisis
date_info = df_cash_sorted[['account_id', 'date_difference']].dropna()

# 22.2: Calcular la media de frecuencia para cada account_id
average_frequency = date_info.groupby('account_id')['date_difference'].mean().reset_index()

# Renombrar la columna para mayor claridad
average_frequency.rename(columns={'date_difference': 'average_frequency'}, inplace=True)

# 22.3: Agrupar por 'average_frequency' y contar usuarios que comparten esa frecuencia
user_count_per_frequency = average_frequency.groupby('average_frequency').size().reset_index(name='user_count')

# 22.4: Crear el gráfico de dispersión de frecuencias promedio
plt.figure(figsize=(10, 6))
sns.scatterplot(data=user_count_per_frequency, x='average_frequency', y='user_count', 
                size='user_count', sizes=(50, 500), alpha=0.6, color='purple', legend=None)

plt.title('Frecuencia Promedio de Uso por Account ID')
plt.xlabel('Frecuencia Promedio (días entre interacciones)')
plt.ylabel('Número de Usuarios')

# Mostrar el gráfico
plt.show()

#--------------------------------------------Cristian's version

# 22. Càlcul de la freqüència d'interaccions per user_id
# 22.1. Agrupar per 'user_id' i calcular la primera i última data de 'created_at'
date_info = df_cash.groupby('user_id')['created_at'].agg(['min', 'max', 'count']).reset_index()
# 22.2. Calcular la diferència en dies
date_info['date_difference'] = (date_info['max'] - date_info['min']).dt.days
# 22.3. Calcular la freqüència
date_info['frecuencia'] = date_info['date_difference'] // date_info['count']
# 22.4. Unir aquesta informació al DataFrame original
df_cash = df_cash.merge(date_info[['user_id', 'frecuencia']], on='user_id', how='left')

# 22.5. Gràfic de mapa de calor amb bombolles
plt.figure(figsize=(10, 6))

# Normalitzar les freqüències per obtenir colors
norm_frecuencia = (date_info['frecuencia'] - date_info['frecuencia'].min()) / (date_info['frecuencia'].max() - date_info['frecuencia'].min())
colors = sns.color_palette("coolwarm_r", as_cmap=True)(norm_frecuencia)  # Paleta de colors inversa

# Crear un mapa de calor com a gràfic de dispersió
sns.scatterplot(data=date_info, x='frecuencia', y='count', 
                size='count', sizes=(20, 500),  # Mida de la bombolla basada en el nombre d'usuaris
                alpha=0.6, palette=colors, legend=None, hue=norm_frecuencia)

plt.title('Mapa de Calor de la Freqüència d\'Interaccions per User ID')
plt.xlabel('Freqüència (dies entre interaccions)')
plt.ylabel('Nombre d\'Usuaris')

# Mostrar el gràfic
plt.show()



#-----------------------------------Frecuencia segun cohorte
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
# 6. Analizar cómo evoluciona la frecuencia a lo largo del tiempo para cada cohorte (usuarios con más de una solicitud)
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

#--------------------------------------------



