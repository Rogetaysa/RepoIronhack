# Pregunta 4
import pandas as pd

capsalera = [
    'order_id', 'activation_time_local', 'country_code', 'store_address', 'final_status', 'payment_status', 'products', 'products_total', 'purchase_total_price'
]
dataold = pd.read_csv('/Users/gabrielrogetdeaysa/Library/CloudStorage/GoogleDrive-rogetaysa@gmail.com/La meva unitat/IronhackGD/RepoIronhack/Project 3 - Ironhack Delivery/project_dataset/python_raw_data/fake_orders_test.csv', header= None, names= capsalera)
dataold.to_csv('/Users/gabrielrogetdeaysa/Library/CloudStorage/GoogleDrive-rogetaysa@gmail.com/La meva unitat/IronhackGD/RepoIronhack/Project 3 - Ironhack Delivery/project_dataset/python_raw_data/fake_orders_test_headers.csv',index=False)
data = pd.read_csv('/Users/gabrielrogetdeaysa/Library/CloudStorage/GoogleDrive-rogetaysa@gmail.com/La meva unitat/IronhackGD/RepoIronhack/Project 3 - Ironhack Delivery/project_dataset/python_raw_data/fake_orders_test_headers.csv')

print(data.head())
#test

# 1. ¿Qué porcentaje de pedidos están subautorizados?
data['subautorizado'] = data['products_total']<data['purchase_total_price'] 
porcentaje_subautorizado = data['subautorizado'].mean()*100
print(f"P1: % Subautorizados: {porcentaje_subautorizado:.2f}%")

# 2. ¿Qué porcentaje de pedidos se autorizarían correctamente con una autorización incremental (+20%) sobre el monto en el checkout?
#  

# 3. ¿Hay diferencias cuando se dividen por país?


# 4. Para el resto de pedidos que quedarían fuera de la autorización incremental, ¿qué valores serían necesarios para capturar el monto restante?
# 

# 5. ¿Qué tiendas son las más problemáticas en términos de pedidos y valor monetario?
# 

# 6. Para los pedidos subautorizados, ¿hay una correlación entre la diferencia en los precios y la cancelación del pedido? En otras palabras: ¿Es más probable que se cancele un pedido a medida que aumenta la diferencia de precio?
# 