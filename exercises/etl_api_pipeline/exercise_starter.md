## English

# Bonus: ETL API Pipeline (From Web to Warehouse)

## The Scenario
Your company has adopted a new CRM system that exposes customer and order data via a REST API (JSON format). Management wants a single, flat Excel report combining customer profiles with their order history — but the API returns deeply nested JSON with inconsistent fields.

## Your Mission
Build a Python ETL pipeline that: **reads** paginated JSON (simulating API responses), **flattens** nested structures into clean DataFrames, **joins** customer data with orders, **handles** missing values and type inconsistencies, and **exports** the consolidated dataset to CSV and Excel.

## Expected Outcome
A clean `customer_orders_consolidated.csv` with one row per order enriched with customer details, plus a `pipeline_report.xlsx` with "Orders Detail" and "Customer Summary" sheets.

---

## Español

# Bonus: Pipeline ETL API (De la Web al Almacén)

## El Escenario
Tu empresa ha adoptado un nuevo sistema CRM que expone datos de clientes y pedidos vía una API REST (formato JSON). La gerencia quiere un único reporte Excel plano que combine perfiles de clientes con su historial de pedidos — pero la API devuelve JSON profundamente anidado con campos inconsistentes.

## Tu Misión
Construir un pipeline ETL en Python que: **lea** JSON paginado (simulando respuestas de API), **aplane** estructuras anidadas en DataFrames limpios, **una** datos de clientes con pedidos, **maneje** valores faltantes e inconsistencias de tipo, y **exporte** el conjunto de datos consolidado a CSV y Excel.

## Resultado Esperado
Un `customer_orders_consolidated.csv` limpio con una fila por pedido enriquecida con detalles del cliente, más un `pipeline_report.xlsx` con hojas "Orders Detail" y "Customer Summary".
