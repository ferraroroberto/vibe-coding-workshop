## English

# Exercise: ETL 3 - The Messy Survey (The Human Factor)

## The scenario

While you are finalizing the sales data, HR pings you. They have an "Employee Satisfaction Survey" (~1000 rows) and want to know if happy sales reps sell more. But their data is a disaster: **Inconsistent Data** (some typed "Male", others "M", "m", or " F "), **Mixed Dates** (join dates in every format imaginable), and **Unstructured Text** (comments with hidden gems like emails or complaint keywords).

## Your mission

Clean this dataset so it can eventually be accurately joined with your Sales data and used for analysis.

1. Standardize the `Gender` column (Male/Female/Other).
2. Standardize `Join_Date` (Datetime objects).
3. Add a new flag column `Compensation_Issue` (True/False) based on keywords.
4. (Optional) Add a new column `extracted_email` pulled from the comments using Regex.

## Expected result

A clean DataFrame (and CSV) with standardized Gender, Join_Date, and the new columns — ready to join with Sales data.

---

## Español

# Ejercicio: ETL 3 - La Encuesta Desordenada (El Factor Humano)

## El escenario

Mientras finalizas los datos de ventas, RRHH te contacta. Tienen una "Encuesta de Satisfacción de Empleados" (~1000 filas) y quieren saber si los vendedores felices venden más. Pero sus datos son un desastre: **Datos Inconsistentes** (algunos escribieron "Male", otros "M", "m" o " F "), **Fechas Mezcladas** (fechas de ingreso en todos los formatos imaginables) y **Texto No Estructurado** (comentarios con correos o palabras clave de quejas).

## Tu misión

Limpiar este conjunto de datos para que eventualmente pueda unirse con tus datos de Ventas y usarse para análisis.

1. Estandarizar la columna `Gender` (Male/Female/Other).
2. Estandarizar `Join_Date` (objetos Datetime).
3. Añadir una nueva columna de indicador `Compensation_Issue` (True/False) basada en palabras clave.
4. (Opcional) Añadir una nueva columna `extracted_email` extraída de los comentarios usando Regex.

## Resultado esperado

Un DataFrame (y CSV) limpio con Gender y Join_Date estandarizados y las nuevas columnas — listo para unir con datos de Ventas.
