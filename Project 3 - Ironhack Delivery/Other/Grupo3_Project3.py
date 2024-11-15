# Pregunta 4
import pandas as pd

capsalera = [
    'order_id', 'activation_time_local', 'country_code', 'store_address', 'final_status', 'payment_status', 'products', 'products_total', 'purchase_total_price'
]
dataold = pd.read_csv('/Users/gabrielrogetdeaysa/Library/CloudStorage/GoogleDrive-rogetaysa@gmail.com/La meva unitat/IronhackGD/RepoIronhack/Project 3 - Ironhack Delivery/project_dataset/python_raw_data/fake_orders_test.csv', header= None, names= capsalera)
dataold.to_csv('/Users/gabrielrogetdeaysa/Library/CloudStorage/GoogleDrive-rogetaysa@gmail.com/La meva unitat/IronhackGD/RepoIronhack/Project 3 - Ironhack Delivery/project_dataset/python_raw_data/fake_orders_test_headers.csv',index=False)
data = pd.read_csv('/Users/gabrielrogetdeaysa/Library/CloudStorage/GoogleDrive-rogetaysa@gmail.com/La meva unitat/IronhackGD/RepoIronhack/Project 3 - Ironhack Delivery/project_dataset/python_raw_data/fake_orders_test_headers.csv')
data['activation_time_local'] = pd.to_datetime(data['activation_time_local'], errors='coerce', format='%d/%m/%Y %H:%M')
print(data.head())

#test

# 1. ¿Qué porcentaje de pedidos están subautorizados?
data['subautorizado'] = data['products_total']<data['purchase_total_price'] 
porcentaje_subautorizado = data['subautorizado'].mean()*100
print(f"P1: % Subautorizados: {porcentaje_subautorizado:.2f}%")

# 2. ¿Qué porcentaje de pedidos se autorizarían correctamente con una autorización incremental (+20%) sobre el monto en el checkout?
data['autorizacion_incremental']= data['products_total']*1.2 >= data['purchase_total_price']
percentatge_autoritzats_incremental = data['autorizacion_incremental'].mean()*100
print(f"P2: % de pedidos autoritzats amb increment de 20%: {percentatge_autoritzats_incremental:.2f}%")

# 3. ¿Hay diferencias cuando se dividen por país?
por_pais = data.groupby('country_code')['subautorizado'].mean()*100
print("3: ")
print(por_pais)

# 4. Para el resto de pedidos que quedarían fuera de la autorización incremental, ¿qué valores serían necesarios para capturar el monto restante?
sin_autorizacion_incremental = data.loc[data['subautorizado']& data['autorizacion_incremental'],'purchase_total_price']-data['products_total']
print("4: ")
print(sin_autorizacion_incremental)

# 5. ¿Qué tiendas son las más problemáticas en términos de pedidos y valor monetario?
problematicas = data.groupby('store_address').agg({'subautorizado':'sum','purchase_total_price':'sum'}).sort_values(by='subautorizado',ascending=False)
print("5: ")
print(problematicas.head())

# 6. Para los pedidos subautorizados, ¿hay una correlación entre la diferencia en los precios y la cancelación del pedido? En otras palabras: ¿Es más probable que se cancele un pedido a medida que aumenta la diferencia de precio?
data['diferencia_preu']=data['purchase_total_price']-data['products_total']
correlacio = data['diferencia_preu'].corr(data['final_status'].apply(lambda x:1 if x == 'CanceledStatus' else 0))
print(f"6: Correlacio {correlacio:.2f}")