![logo_ironhack_blue 7](https://user-images.githubusercontent.com/23629340/40541063-a07a0a8a-601a-11e8-91b5-2f13e4e6b441.png)

# Prueba Técnica de Análisis de Producto (IronHack Delivery)

***El siguiente párrafo es habitual en entrevistas técnicas de trabajo.***

*Ser práctico es uno de los requisitos clave para este rol. Debes completar esta prueba en un máximo de 3 días desde el día en que la recibas. Cuanto más rápido la entregues, mejor.*

## Lo que valoramos:

- Un estilo de codificación limpio
- Soluciones eficientes a los problemas planteados
- Legibilidad y escalabilidad de SQL
- Uso idiomático de Python
- Uso apropiado de las funciones integradas y bibliotecas estándar de Python

### 1. KPIs (25 puntos)

En tu opinión, ¿cuáles son los tres principales KPIs para IronHack Delivery? Clasificados por orden de importancia decreciente. Explica tu elección y trata de hacer una estimación fundamentada de su valor. Proporciona una explicación paso a paso de tu estimación. ¿Cómo los mejorarías? Nota: Ignora los KPIs financieros puros que aplican a todos los negocios.

### 2. SQL (25 puntos)

Tienes la tabla `customer_courier_chat_messages` que almacena datos sobre mensajes individuales intercambiados entre clientes y repartidores a través del chat en la aplicación. Un ejemplo de la tabla es el siguiente:

| Tipo de app del remitente | ID del cliente | De ID | Para ID | Chat iniciado por | Mensaje | ID del pedido | Etapa del pedido | ID del repartidor | Hora de envío del mensaje |
| ------------------------- | -------------- | ----- | ------ | ----------------- | ------- | ------------- | ---------------- | ----------------- | ------------------------ |
| Cliente iOS               | 17071099       | 17071099 | 16293039 | FALSO | 59528555 | RECOGIENDO | 16293039 | 2019-08-19 8:01:47 |
| Repartidor iOS            | 17071099       | 16293039 | 17071099 | FALSO | 59528555 | LLEGANDO | 16293039 | 2019-08-19 8:01:04 |
| Cliente iOS               | 17071099       | 17071099 | 16293039 | FALSO | 59528555 | RECOGIENDO | 16293039 | 2019-08-19 8:00:04 |
| Repartidor Android        | 12874122       | 18325287 | 12874122 | VERDADERO | 59528038 | ENTREGA_EN_DIRECCIÓN | 18325287 | 2019-08-19 7:59:33 |

También tienes acceso a la tabla `orders` donde tienes un campo `order_id` y `city_code`.

Tu tarea es construir una consulta que cree una tabla (`customer_courier_conversations`) que agregue los mensajes individuales en conversaciones. Ten en cuenta que una conversación es única por pedido. Los campos requeridos son los siguientes:

- ID del pedido
- Código de la ciudad
- Marca de tiempo del primer mensaje del repartidor
- Marca de tiempo del primer mensaje del cliente
- Número de mensajes del repartidor
- Número de mensajes del cliente
- El primer remitente del mensaje (repartidor o cliente)
- Marca de tiempo del primer mensaje en la conversación
- Tiempo (en segundos) transcurrido hasta la primera respuesta
- Marca de tiempo del último mensaje enviado
- La etapa del pedido cuando se envió el último mensaje

¡Haz que tu consulta sea escalable y legible!

### 3. Experimento (25 puntos)

Nos gustaría medir el impacto de aumentar la tarifa de entrega de pedidos en una ciudad dada (sin considerar el valor de los productos), de €1.9 a €2.1, en los KPIs de la empresa.

Se te pide diseñar el experimento desde la etapa conceptual, planificar el análisis empírico y presentar las recomendaciones según los resultados del experimento.

Explica en detalle cómo abordarías esta tarea, enfocándote en lo siguiente:

- ¿Qué tipo de prueba requeriría esto?
- ¿Probarías esto solo en nuevos usuarios o en todos los usuarios activos? ¿Por qué?
- ¿Qué suposiciones harías y cómo probarías si estas suposiciones son correctas?
- ¿Qué enfoque usarías para determinar la duración del experimento?
- ¿Qué KPIs/métricas elegirías para evaluar el éxito de la prueba?
- ¿Qué pasos tomarías para analizar los resultados de la prueba?
- ¿Cuáles serían tus recomendaciones según los resultados de la prueba?

### 4. Análisis Exploratorio de Datos (Ejercicio de Programación Estadística) (25 puntos)

Te han dado un conjunto de datos sobre pedidos provenientes de socios falsos en la aplicación. Los socios falsos son las tiendas que no están integradas directamente con IronHack Delivery, por lo que nuestro equipo de contenido gestiona su catálogo de productos y precios por ellos. Los pedidos de socios falsos se cobran al cliente al momento de la entrega y en muchos casos hay una discrepancia entre el monto total en el checkout de la app (`products_total`) y lo que el repartidor paga en la tienda (`purchase_total_price`), causando muchos problemas. Cuando el `products_total` es menor que el `purchase_total_price`, los llamamos pedidos subautorizados, de lo contrario, es un pedido correctamente autorizado. Queremos pasar del modelo de cobro a la entrega a un modelo de autorización y captura, pero primero necesitamos entender la fluctuación de precios de los pedidos anteriores para conocer el riesgo de hacerlo.

#### Descripción del conjunto de datos:

- `order_id`
- `activation_time_local`: hora local en que se activó el pedido
- `country_code`
- `store_address`
- `final_status`
- `payment_status`
- `products`: número de productos en el pedido
- `products_total`: monto total en el checkout (€)
- `purchase_total_price`: monto que el repartidor pagó en la tienda (€)

Tu tarea es realizar un proceso de Análisis Exploratorio de Datos (EDA) (R/Python) con estos datos para responder las siguientes preguntas:

1. ¿Qué porcentaje de pedidos están subautorizados?
2. ¿Qué porcentaje de pedidos se autorizarían correctamente con una autorización incremental (+20%) sobre el monto en el checkout?
3. ¿Hay diferencias cuando se dividen por país?
4. Para el resto de pedidos que quedarían fuera de la autorización incremental, ¿qué valores serían necesarios para capturar el monto restante?
5. ¿Qué tiendas son las más problemáticas en términos de pedidos y valor monetario?
6. Para los pedidos subautorizados, ¿hay una correlación entre la diferencia en los precios y la cancelación del pedido? En otras palabras: ¿Es más probable que se cancele un pedido a medida que aumenta la diferencia de precio?