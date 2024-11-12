-- Pregunta 1
-- 1. Tiempo de espera entre pedido y entrega
-- 2. Porcentaje de pedidos completados (no cancelados)
-- 3. Frecuencia de uso del servicio

-- Pregunta 2
CREATE DATABASE ironhackdelivery;
USE ironhackdelivery;

-- Afegir columna per les dates en format hora:
ALTER TABLE customer_courier_chat_messages
ADD COLUMN time_message_sent DATETIME;

-- Omplir la columna amb dades convertides: OJO S'HA DE TREURE EL SAFE UPDATES
UPDATE customer_courier_chat_messages
SET time_message_sent = STR_TO_DATE(message_sent_time, '%d/%m/%Y %H:%i')
WHERE STR_TO_DATE(message_sent_time, '%d/%m/%Y %H:%i') IS NOT NULL;

-- TORNA A POSAR SAFE UPDATES PER SI LES MOSQUES

DROP TABLE IF EXISTS customer_courier_conversations;
CREATE TABLE customer_courier_conversations AS
WITH conversation_agg AS(
    SELECT 
        ccm.order_id,
        o.city_code,
        -- tiempo_primer_mensaje_repartidor
        MIN(CASE
            WHEN ccm.sender_app_type LIKE 'Courier%' THEN ccm.time_message_sent
        END) AS tiempo_primer_mensaje_repartidor,
        -- tiempo_primer_mensaje_cliente,
        MIN(CASE
            WHEN ccm.sender_app_type LIKE 'Customer%' THEN ccm.time_message_sent
        END) AS tiempo_primer_mensaje_cliente,
        -- num_mensajes_repartidor
        COUNT(CASE
            WHEN ccm.sender_app_type LIKE 'Courier%' THEN 1
        END) AS num_mensajes_repartidor,
        -- num_mensajes_cliente
        COUNT(CASE
            WHEN ccm.sender_app_type LIKE 'Customer%' THEN 1
        END) AS num_mensajes_cliente,
        -- primer_remitente
        CASE
            WHEN MIN(ccm.time_message_sent) = MIN(CASE
                WHEN ccm.sender_app_type LIKE 'Courier%' THEN ccm.time_message_sent
            END) THEN 'Courier'
            ELSE 'Client'
        END AS primer_remitente,
        -- primer_mensaje_conversacion:
        MIN(ccm.time_message_sent) AS primer_mensaje_conversacion,
        -- ultimo_mensaje_conversacion:
        MAX(ccm.time_message_sent) AS ultimo_mensaje_conversacion,
        -- etapa_ultimo_mensaje:
        MAX(ccm.order_stage) AS etapa_ultimo_mensaje
    FROM
        customer_courier_chat_messages ccm
    JOIN orders o ON ccm.order_id = o.order_id
    GROUP BY ccm.order_id, o.city_code
)
SELECT 
    ca.order_id,
    ca.city_code,
    ca.tiempo_primer_mensaje_repartidor,
    ca.tiempo_primer_mensaje_cliente,
    ca.num_mensajes_repartidor,
    ca.num_mensajes_cliente,
    ca.primer_remitente,
	ca.primer_mensaje_conversacion,
    -- ca.tiempo_primera_respuesta:
    COALESCE(TIMESTAMPDIFF(SECOND, ca.primer_mensaje_conversacion, ca.tiempo_primer_mensaje_cliente),0) AS tiempo_primera_respuesta,
	ca.ultimo_mensaje_conversacion,
	ca.etapa_ultimo_mensaje
FROM conversation_agg ca;

SELECT * FROM customer_courier_conversations;

-- Pregunta 3
-- * ¿Qué tipo de prueba requeriría esto?
-- Prueba A/B (Sesion 42 - AB Testing). Un experimento controlado. Donde habría dos grupos:
-- Grupo de control a 1,9€
-- Grupo de tratamiento a 2,1€

-- * ¿Probarías esto solo en nuevos usuarios o en todos los usuarios activos? ¿Por qué?
-- Todos los usuarios ya que aseguras que la muestra sea de usuarios recurrentes y de nuevos

-- * ¿Qué suposiciones harías y cómo probarías si estas suposiciones son correctas?
-- Que ambos grupos (de control y tratamiento) sean iguales (en cuanto a características)
-- Que la sensibilidad al precio no varía por otros factores que no tienen que ver con la prueba
-- Pruebas: Hacer un análisis de equilibro para asegurarnos que las muestras son homogéneas

-- * ¿Qué enfoque usarías para determinar la duración del experimento?
-- El objetivo es tener un nivel de significancia de aprox 95% y un poder estadístico de alrededor de 80%. Por lo que hay que usar una fórmula para calcular el tamaño de la muestra y determinar la duración necesaria para alcanzar estos niveles.
-- Hay que tener en cuenta la tasa de conversión y el efecto esperado por esta subida de tarifa

-- * ¿Qué KPIs/métricas elegirías para evaluar el éxito de la prueba?
-- Principales: Tasa de completación de pedidos, Valor promedio de cada pedido, La retención de usuarios y la satisfacción de los clientes
-- Otros: Abandono de la compra a medias, Cancelación de pedidos

-- * ¿Qué pasos tomarías para analizar los resultados de la prueba?
-- Como método, primero análisis de cuán diferentes sean los grupos. Preubas estadísiticas (como el t-test para comparar los KPis). Y Regresiones para ajustar variables de control y verificar la consistencia de los resultados
-- Para ver los resultados seguramente diagramas de barras, de puntos o incluso de cajas para ver las diferencias entre los dos grupos

-- * ¿Cuáles serían tus recomendaciones según los resultados de la prueba?
-- Ver si el grupo nuevo mejora, o se queda igual haría el cambio a la nueva tarifa para todos
-- Si el grupo nuevo empeora pues mantendría los precios antiguos



-- Pregunta 4
-- 1. ¿Qué porcentaje de pedidos están subautorizados?
-- 

-- 2. ¿Qué porcentaje de pedidos se autorizarían correctamente con una autorización incremental (+20%) sobre el monto en el checkout?
-- 

-- 3. ¿Hay diferencias cuando se dividen por país?
-- 

-- 4. Para el resto de pedidos que quedarían fuera de la autorización incremental, ¿qué valores serían necesarios para capturar el monto restante?
-- 

-- 5. ¿Qué tiendas son las más problemáticas en términos de pedidos y valor monetario?
-- 

-- 6. Para los pedidos subautorizados, ¿hay una correlación entre la diferencia en los precios y la cancelación del pedido? En otras palabras: ¿Es más probable que se cancele un pedido a medida que aumenta la diferencia de precio?
-- 
