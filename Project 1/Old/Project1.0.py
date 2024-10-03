#primer importaem les llibreries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



#obrim els csv
df_cash = pd.read_csv('extract - cash request - data analyst.csv')
df_fees = pd.read_csv('extract - fees - data analyst - .csv')

print("Cash head:")
print(df_cash.head())
print("Fees head:")
print(df_fees.head())

#df.info()
df_cash.info()
df_fees.info()

#df.describe()
df_cash.describe()
df_fees.describe()

# Netejar dates per agrupar per mesos
date_columns_cash = ['created_at', 'updated_at', 'moderated_at', 'reimbursement_date', 'cash_request_received_date', 'money_back_date', 'send_at', 'reco_creation', 'reco_last_update']
date_columns_fees = ['created_at', 'updated_at', 'paid_at', 'from_date', 'to_date']

#Convertir les dates amb pd.to_datetime
for i in date_columns_cash:
    df_cash[i] = pd.to_datetime(df_cash[i], errors='coerce')
# Extraer solo día, mes y año
for i in date_columns_cash:
    df_cash[i] = pd.to_datetime(df_cash[i], errors='coerce')
for i in date_columns_cash:
    df_cash[i] = df_cash[i].dt.normalize()
for k in date_columns_fees:
    df_fees[k] = pd.to_datetime(df_fees[k], errors='coerce')
for k in date_columns_fees:
    df_fees[k] = df_fees[k].dt.normalize()

#for i in date_columns_cash:
#    df_cash[i] = pd.to_datetime(df_cash[i], errors='coerce')

#for j in date_columns_fees:
#    df_fees[j] = pd.to_datetime(df_fees[j], errors='coerce')

#provar
print("Cash head amb dates canviades:")
print(df_cash.head())
print("Fees head amb dates canviades:")
print(df_fees.head())

print("\nTipus de dades de Cash Requests:")
print(df_cash[date_columns_cash].dtypes)
print("\nTipus de dades de Fees:")
print(df_fees[date_columns_fees].dtypes)



