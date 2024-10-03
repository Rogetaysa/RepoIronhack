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
print("\n\033[1m\033[95mPARTE 1: Primeres files\033[0m")
print("Cash head:")
print(df_cash.head())
print("Fees head:")
print(df_fees.head())
print(df_fees.columns)
# 2. Informació dels DataFrames
# 2.1 Mostrar informació dels tipus de dades
print("\n\033[1m\033[95mPARTE 2: Descripció estadística\033[0m")
df_cash.info()
df_fees.info()
# 2.2 Mostrar descripció estadística
print("Descripció estadística de Cash:")
print(df_cash.describe())
print("Descripció estadística de Fees:")
print(df_fees.describe())
# 3. Netejar dates per agrupar per mesos
# 3.1 Definir les columnes de dates per Cash i Fees
print("\n\033[1m\033[95mPARTE 3: Agrupar per mesos\033[0m")
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
print("\n\033[1m\033[95mPARTE 4: Tipus de dades cash request\033[0m")
print("PARTE 4: Tipus de dades cash request:")
print("\nTipus de dades de Cash Requests:")
print(df_cash[date_columns_cash].dtypes)
print("\nTipus de dades de Fees:")
print(df_fees[date_columns_fees].dtypes)
# 5.1 Ordenar per 'created_at' en ambdós DataFrames
df_cash_sorted = df_cash.sort_values(by='created_at', ascending=True)
df_fees_sorted = df_fees.sort_values(by='created_at', ascending=True)
# 5.2 Mostrar els primers resultats després de ordenar
print("\n\033[1m\033[95mPARTE 5: Resultats després de ordenar\033[0m")
print("Cash sorted by created_at:")
print(df_cash_sorted.head())
print("Fees sorted by created_at:")
print(df_fees_sorted.head())
# 6
print("\n\033[1m\033[95mPARTE 6: Sustituir user_id vacíos por deleted_account_id\033[0m")
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
print("\n\033[1m\033[95mPARTE 7: Ordenar\033[0m")
print("DataFrame ordenat per created_at:")
print(df_cash_sorted[['user_id', 'created_at', 'cohort', 'deleted_account_id']])



# 8. Gràfic - Distribució de cohorts
print("\n\033[1m\033[95mPARTE 8: Distribució de cohorts\033[0m")
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

# 9.1 Distribució dels estats actuals
print("\n\033[1m\033[95mPARTE 9: Distribució de estats\033[0m")
status_distribution = df_cash['status'].value_counts()
print("\nDistribució dels estats de les sol·licituds de caixa:")
print(status_distribution)

# 9.2 Visualització de la distribució dels estats
plt.figure(figsize=(10, 6))
ax = sns.countplot(x='status', data=df_cash, palette='Set2', hue='status', legend=False)  # Asignar hue
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



# 10 Freqüència mitjana per cohort
print("\n\033[1m\033[95mPARTE 10: Freqüència mitjana per cohorte\033[0m")
df_cash['created_at'] = pd.to_datetime(df_cash['created_at'])
df_cash['cohort'] = pd.to_datetime(df_cash['cohort'], format='%Y-%m')
# 10.1 Filtrar usuaris que han fet més d'una sol·licitud, excloent 'rejected'
user_counts = df_cash['user_id'].value_counts()
multiple_requests_users = user_counts[user_counts > 1].index
df_cash_filtered = df_cash[(df_cash['status'] != 'rejected') & (df_cash['user_id'].isin(user_counts[user_counts > 1].index))]
# 10.2: Calcular la freqüència per usuari com a la diferència entre sol·licituds
df_cash_filtered = df_cash_filtered.sort_values(by=['user_id', 'created_at'])
df_cash_filtered['days_between'] = df_cash_filtered.groupby('user_id')['created_at'].diff().dt.days.dropna()
# 10.3: Calcular el nombre d'usuaris que només han fet una sol·licitud per cohort
single_request_users = user_counts[user_counts == 1].index
df_cash_single_request = df_cash[df_cash['user_id'].isin(single_request_users) & (df_cash['status'] != 'rejected')]
single_request_count = df_cash_single_request.groupby('cohort')['user_id'].nunique().reset_index(name='single_request_count')
# 10.4: Visualitzar el diagrama de caixes per cohort, afegint valors clau
plt.figure(figsize=(12, 8))
box_plot = sns.boxplot(x='cohort', y='days_between', data=df_cash_filtered, palette='Set2')
# Calcular i afegir valors clau com quartils, mediana, mitjana, màxim i mínim
stats = df_cash_filtered.groupby('cohort')['days_between'].describe()
for i, cohort in enumerate(stats.index):
    median = stats.loc[cohort, '50%']
    q1 = stats.loc[cohort, '25%']
    q3 = stats.loc[cohort, '75%']
    mean = stats.loc[cohort, 'mean']
    minimum = stats.loc[cohort, 'min']
    maximum = stats.loc[cohort, 'max']
    # Desplazar los textos a la derecha
    plt.text(i + 0.3, median, f'{median:.1f}', ha='center', va='bottom', color='black', fontsize=10, fontweight='bold')
    plt.text(i + 0.3, q1, f'{q1:.1f}', ha='center', va='top', color='blue', fontsize=9)
    plt.text(i + 0.3, q3, f'{q3:.1f}', ha='center', va='bottom', color='blue', fontsize=9)
    plt.text(i + 0.3, mean, f'{mean:.1f}', ha='center', va='bottom', color='red', fontsize=9)
    plt.text(i + 0.3, minimum, f'{minimum:.1f}', ha='center', va='top', color='green', fontsize=9)
    plt.text(i + 0.3, maximum, f'{maximum:.1f}', ha='center', va='bottom', color='purple', fontsize=9)
# 10.6 Ajustaments visuals
plt.xticks(rotation=45)
plt.title('Distribució de la freqüència de sol·licituds per cohort (usuaris amb més d\'una sol·licitud)')
plt.xlabel('Cohort (Mes i Any)')
plt.ylabel('Dies entre sol·licituds')
# Agregar leyenda para los colores
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', label='Mitjana', markerfacecolor='red', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Mediana', markerfacecolor='black', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Q1', markerfacecolor='blue', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Q3', markerfacecolor='blue', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Mínim', markerfacecolor='green', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Màxim', markerfacecolor='purple', markersize=10)
]
plt.legend(handles=legend_elements, loc='upper right', fontsize=9, title='Referències de Color')
# Ajustar el layout para los textos desplazados
plt.subplots_adjust(left=0.1, bottom=0.2)
# 10.9 Mostrar el diagrama
plt.show()
# Crear una nova figura per la taula de eliminats en format horizontal
plt.figure(figsize=(12, 4))
# Crear la taula horizontal separada
table = plt.table(cellText=[single_request_count['single_request_count'].values],
                  colLabels=single_request_count['cohort'].dt.strftime('%Y-%m'),
                  loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)
# Ocultar ejes ya que solo mostramos la tabla
plt.axis('off')
plt.title('Quantitat d\'usuaris eliminats que solo han hecho una solicitud')
# Mostrar la nova taula
plt.show()


# 11. Analitzar els ingressos generats per cohort
print("\n\033[1m\033[95mPARTE 11: Analizar ingresos generados por cohorte\033[0m")

df_combinados = df_fees.merge(df_cash[['id', 'cohort']], left_on='cash_request_id', right_on='id', how='left')
df_combinados.head()
df_aprobados = df_combinados[(df_combinados['status'] == 'accepted')]
Ingresos_generados = df_aprobados[["total_amount", "cohort"]].groupby("cohort").sum()
Ingresos_generados
plt.figure(figsize=(10, 6))

# Corregimos el warning asignando 'cohort' a 'hue' y ocultando la leyenda
graf_ing = sns.barplot(x='cohort', y='total_amount', hue='cohort', data=Ingresos_generados, palette='Set2', legend=False)

# Título y etiquetas
plt.title('Ingresos generados por cohorte')
plt.xlabel('Cohort (mes y año)')
plt.ylabel('Ingresos totales')
plt.xticks(rotation=45)

# Añadimos las etiquetas con la cantidad total encima de cada barra
for p in graf_ing.patches:
    graf_ing.annotate(f'{int(p.get_height())}',  # Mostramos la cantidad sin decimales
                (p.get_x() + p.get_width() / 2., p.get_height()),  # Posición de la etiqueta
                ha='center', va='bottom', fontsize=12)  # Alineación y tamaño de fuente

# Mostrar el gráfico
plt.show()



# 12. Distribucion de estado por cohorte
print("\n\033[1m\033[95mPARTE 12: Flor Distribucion de estado por cohorte\033[0m")
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


#13------- Cristian test
#13.1
print("\n\033[1m\033[95mPARTE 13: Cristian, Tasas incidentes por cohorte en %\033[0m")
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

#15
print("\n\033[1m\033[95mPARTE 15: Flor Porcentaje de incidentes por cohorte y tipo de estado apilado\033[0m")
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



#16 Desgloce de incidencias por tipo y cantidad# Crear una tabla pivote para obtener la cantidad de incidencias por cohorte y tipo de incidencia
print("\n\033[1m\033[95mPARTE 16: Desgloce de incidencias por tipo y cantidad\033[0m")

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