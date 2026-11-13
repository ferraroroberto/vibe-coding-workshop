## English

# Exercise: ETL 2 - The Detective

## The scenario

You are a Data analyst at *Global Widgets Inc.* You successfully merged the sales files in the previous project. However, the Finance team has rejected your report. "The numbers don't add up," they said. "We see the same Order ID appearing twice, and why do we have negative sales? Are we paying people to take our products?" Your job is to act as a detective: separate the good data from the bad.

## Your mission

1. **Load** the `combined_sales.csv` file.
2. **Find and Remove** duplicate `Order_ID`s (glitch in the system).
3. **Filter out** negative numbers in the `Revenue` column (erroneous refunds).
4. **Save** the clean dataset as `clean_sales_data.csv`.

**(Optional) Tier 2 Challenge:** Identify "Suspiciously High" revenue transactions (outliers) that are statistically impossible (3 standard deviations from the mean).

## Expected result

A clean file `clean_sales_data.csv` with no duplicate Order IDs and no negative revenue — ready for reporting.

---

## Español

# Ejercicio: ETL 2 - El Detective

## El escenario

Eres analista de datos en *Global Widgets Inc.* Combinaste exitosamente los archivos de ventas en el proyecto anterior. Sin embargo, el equipo de Finanzas ha rechazado tu reporte. "Los números no cuadran", dijeron. "Vemos el mismo Order ID aparecer dos veces, y ¿por qué tenemos ventas negativas? ¿Estamos pagando a la gente para que se lleve nuestros productos?" Tu trabajo es actuar como detective: separar los datos buenos de los malos.

## Tu misión

1. **Cargar** el archivo `combined_sales.csv`.
2. **Encontrar y eliminar** `Order_ID` duplicados (fallo en el sistema).
3. **Filtrar** los números negativos en la columna `Revenue` (reembolsos erróneos).
4. **Guardar** el conjunto de datos limpio como `clean_sales_data.csv`.

**(Opcional) Desafío Nivel 2:** Identificar transacciones de ingresos "Sospechosamente Altas" (valores atípicos) que son estadísticamente imposibles (3 desviaciones estándar de la media).

## Resultado esperado

Un archivo limpio `clean_sales_data.csv` sin Order IDs duplicados y sin ingresos negativos — listo para reportar.
