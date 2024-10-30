# 1 Inicio
# 1.1 Importar les llibreries necessàries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1.2 Obrir els fitxers CSV
df_cash = pd.read_csv('extract - cash request - data analyst.csv')
df_fees = pd.read_csv('extract - fees - data analyst - .csv')

# 1.3. Mostrar les primeres files dels DataFrames
print("PARTE 1: Primeres files")
print("Cash head:")
print(df_cash.head())
print("Fees head:")
print(df_fees.head())
print(df_fees.columns)

# 2. Informació dels DataFrames
# 2.1 Mostrar informació dels tipus de dades
print("PARTE 2: Descripció estadística")
df_cash.info()
df_fees.info()

# 2.2 Mostrar descripció estadística
print("Descripció estadística de Cash:")
print(df_cash.describe())
print("Descripció estadística de Fees:")
print(df_fees.describe())

# 3. Netejar dates per agrupar per mesos
# 3.1 Definir les columnes de dates per Cash i Fees
print("PARTE 3: Agrupar per mesos")
date_columns_cash = [
    'created_at', 'updated_at', 'moderated_at', 
    'reimbursement_date', 'cash_request_received_date', 
    'money_back_date', 'send_at', 'reco_creation', 
    'reco_last_update'
]
date_columns_fees = ['created_at', 'updated_at', 'paid_at', 'from_date', 'to_date']

# 3.2 Convertir i normalitzar les dates amb pd.to_datetime
for col in date_columns_cash:
    df_cash[col] = pd.to_datetime(df_cash[col], errors='coerce').dt.normalize()

for col in date_columns_fees:
    df_fees[col] = pd.to_datetime(df_fees[col], errors='coerce').dt.normalize()

# 4. Tipus de dades de Cash Requests
print("PARTE 4: Tipus de dades cash request:")
print("\nTipus de dades de Cash Requests:")
print(df_cash[date_columns_cash].dtypes)

print("\nTipus de dades de Fees:")
print(df_fees[date_columns_fees].dtypes)

# 5.1 Ordenar per 'created_at' en ambdós DataFrames
df_cash_sorted = df_cash.sort_values(by='created_at', ascending=True)
df_fees_sorted = df_fees.sort_values(by='created_at', ascending=True)

# 5.2 Mostrar els primers resultats després de ordenar
print("PARTE 5: Resultats després de ordenar")
print("Cash sorted by created_at:")
print(df_cash_sorted.head())
print("Fees sorted by created_at:")
print(df_fees_sorted.head())

# 6
print("PARTE 6: Sustituir user_id vacíos por deleted_account_id")
# 6.1 Omplir valors nuls de 'user_id' amb 'deleted_account_id'
df_cash['user_id'] = df_cash['user_id'].fillna(df_cash['deleted_account_id'])

# 6.2 Eliminar files amb user_id encara nuls
df_cash = df_cash[~df_cash['user_id'].isna()]

# 6.3 Agrupar per user_id i obtenir la primera data de created_at
cohorts = df_cash.groupby('user_id')['created_at'].min().reset_index()
cohorts.rename(columns={'created_at': 'first_created_at'}, inplace=True)

# 6.4 Crear una nova columna amb el format de mes i any
cohorts['cohort'] = cohorts['first_created_at'].dt.to_period('M').astype(str)

# 6.5 Unir els cohorts al DataFrame original
df_cash = df_cash.merge(cohorts[['user_id', 'cohort']], on='user_id', how='left')

# 6.6 Mostrar els primers resultats per verificar
print("PARTE 6:")
print(df_cash[['user_id', 'created_at', 'cohort']].head())

# 7. Ordenar el DataFrame df_cash per la columna created_at
df_cash_sorted = df_cash.sort_values(by='created_at', ascending=True)

# 7.1 Mostrar els primers resultats després d'ordenar
print("PARTE 7: Ordenar tot")
print("DataFrame ordenat per created_at:")
print(df_cash_sorted[['user_id', 'created_at', 'cohort', 'deleted_account_id']])

# 8. Gràfic - Distribució de cohorts
print("PARTE 8: Distribució de cohorts")

cohort_counts = df_cash.groupby('cohort')['user_id'].nunique()

# 8.1 Visualització de la distribució d'usuaris per cohort
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=cohort_counts.index.astype(str), y=cohort_counts.values, palette='Set2')
plt.title('Distribució d\'usuaris per cohort')
plt.xlabel('Cohort (mes i any)')
plt.ylabel('Nombre d\'usuaris únics')
plt.xticks(rotation=45)

# 8.2 Afegeix la quantitat total a dalt de cada columna
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=12)
plt.show()

# 8.3 Mostrar el total de la distribució de cohorts
total_cohort_users = cohort_counts.sum()
print("Total cohort users:")
print(total_cohort_users)

# 9.1 Distribució dels estats actuals
print("PARTE 9: Distribució de estats")

status_distribution = df_cash['status'].value_counts()
print("\nDistribució dels estats de les sol·licituds de caixa:")
print(status_distribution)

# 9.2 Visualització de la distribució dels estats
plt.figure(figsize=(10, 6))
ax = sns.countplot(x='status', data=df_cash, palette='Set2')
plt.title('Distribució dels Estats de les Sol·licituds de Caixa')
plt.xlabel('Estat de la Sol·licitud')
plt.ylabel('Nombre de Sol·licituds')
plt.xticks(rotation=45)

# 9.3 Afegeix la quantitat total a dalt de cada barra
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='bottom', fontsize=12)
plt.show()

# 10.1 Filtrar usuaris que han fet més d'una sol·licitud
print("PARTE 10: Filtrar usuaris que han fet més d'una sol·licitud i freqüència mitjana per cohorte")

user_counts = df_cash['user_id'].value_counts()
multiple_requests_users = user_counts[user_counts > 1].index
df_cash_filtered = df_cash[df_cash['user_id'].isin(multiple_requests_users)]

# 10.2: Calcular la freqüència per usuari com a la diferència entre sol·licituds
df_cash_filtered = df_cash_filtered.sort_values(by=['user_id', 'created_at'])
df_cash_filtered['days_between'] = df_cash_filtered.groupby('user_id')['created_at'].diff().dt.days.dropna()

# 10.3: Agrupar per cohort i calcular la mitjana de la freqüència
cohort_frequencies_filtered = df_cash_filtered.groupby('cohort')['days_between'].mean().reset_index()

# 10.4: Visualitzar la freqüència mitjana per cohort
plt.figure(figsize=(10, 6))
sns.barplot(x='cohort', y='days_between', data=cohort_frequencies_filtered)
plt.xticks(rotation=45)
plt.title('Freqüència mitjana de sol·licituds per cohort (usuaris amb més d\'una sol·licitud)')
plt.xlabel('Cohort (Mes i Any)')
plt.ylabel('Mitjana de dies entre sol·licituds')

# 10.5 Afegeix la quantitat total a dalt de cada barra
for p in plt.gca().patches:
    plt.annotate(f'{p.get_height():,.1f}', 
                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='bottom', fontsize=12)
plt.show()

# 11. Analitzar els ingressos generats per cohort
print("PARTE 11: Ingressos generats per cohort.")

if 'total_amount' in df_fees.columns and 'amount' in df_cash.columns:
    # Calcular els ingressos
    df_fees['revenue'] = df_cash.groupby('user_id')['amount'].sum().reindex(df_fees['user_id']).reset_index(drop=True) - df_fees['total_amount']

    # Agrupar per cohort i calcular els ingressos totals
    cohort_revenue = df_cash.groupby('cohort')['amount'].sum() - df_fees.groupby('cohort')['total_amount'].sum()

    # Visualitzar els ingressos totals per cohort
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=cohort_revenue.index.astype(str), y=cohort_revenue.values)
    plt.title('Ingressos generats per cohort')
    plt.xlabel('Cohort (Mes i Any)')
    plt.ylabel('Ingressos totals')
    plt.xticks(rotation=45)

    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='bottom', fontsize=12)
    plt.show()

else:
    print("Les columnes 'total_amount' i 'amount' no estan disponibles per calcular els ingressos.")

print("FIN DEL CÒDIC")



# 12. Agrupar per cohort per sumar les taxes pagades
print("PARTE 12:  agrupar cohorte para sumar tasas pagadas. Me peta, lo escondo")

#12.2 cohort fees
#cohort_fees = df_fees.groupby(df_fees['paid_at'].dt.to_period('M'))['fee_amount'].sum().reset_index()

cohort_fees = df_fees.groupby(df_fees['paid_at'].dt.to_period('M'))['total_amount'].sum().reset_index()

# 12.2 Visualitzar les taxes totals per cohort
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='paid_at', y='total_amount', data=cohort_fees, palette='Set1')
plt.xticks(rotation=45)
plt.title('Taxes totals per cohort')
plt.xlabel('Cohort (Mes i Any)')
plt.ylabel('Taxes totals')

# 12.3 Afegeix la quantitat total a dalt de cada barra
for p in ax.patches:
    ax.annotate(f'{p.get_height():,.2f}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='bottom', fontsize=12)

plt.show()



#13------- Cristian test
#13.1
print("PARTE 13: Cristian, Tasas incidentes por cohorte en %")
cohort_status_counts = df_cash.pivot_table(index='cohort', columns='status', aggfunc='size', fill_value=0)
# Agregamos una fila con los totales para cada cohorte
cohort_status_counts.loc['Total'] = cohort_status_counts.sum()
# Mostramos el DataFrame con los totales
display(cohort_status_counts)


#13.2
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


#14 ------------------Flor test
print("PARTE 14: Flor Porcentaje de incidentes por cohorte y tipo de estado")
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


#14
print("PARTE 15: Flor Porcentaje de incidentes por cohorte y tipo de estado apilado")

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