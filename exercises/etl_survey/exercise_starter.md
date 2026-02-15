## English

# Exercise: ETL 3 - The Messy Survey (The Human Factor)

## The Goal
A clear, concise explanation of the problem we are solving and what the expected outcome is.

**Scenario:**
While you are finalizing the sales data, HR pings you. They have an "Employee Satisfaction Survey" (~1000 rows) and want to know if happy sales reps sell more. But their data is a disaster:
*   **Inconsistent Data:** Some people typed "Male", others "M", "m", or " F ".
*   **Mixed Dates:** Join dates are in every format imaginable (YYYY-MM-DD, DD/MM/YYYY, etc.).
*   **Unstructured Text:** The comments section is free-text, containing hidden gems like personal email addresses or keywords about complaints.

**Your Mission:**
Clean this dataset so it can eventually be accurately joined with your Sales data and used for analysis.

**Expected Outcome:**
A clean DataFrame (and CSV) with:
1.  Standardized `Gender` column (Male/Female/Other).
2.  Standardized `Join_Date` (Datetime objects).
3.  A new flag column `Compensation_Issue` (True/False) based on keywords.
4.  (Optional) A new column `extracted_email` pulled from the comments using Regex.

---

## Español

# Ejercicio: ETL 3 - La Encuesta Desordenada (El Factor Humano)

## El Objetivo
Una explicación clara y concisa del problema que resolvemos y del resultado esperado.

**Escenario:**
Mientras finalizas los datos de ventas, RRHH te contacta. Tienen una "Encuesta de Satisfacción de Empleados" (~1000 filas) y quieren saber si los vendedores felices venden más. Pero sus datos son un desastre:
*   **Datos Inconsistentes:** Algunos escribieron "Male", otros "M", "m" o " F ".
*   **Fechas Mezcladas:** Las fechas de ingreso están en todos los formatos imaginables (YYYY-MM-DD, DD/MM/YYYY, etc.).
*   **Texto No Estructurado:** La sección de comentarios es texto libre, con cosas como correos personales o palabras clave sobre quejas.

**Tu Misión:**
Limpiar este conjunto de datos para que eventualmente pueda unirse con tus datos de Ventas y usarse para análisis.

**Resultado Esperado:**
Un DataFrame (y CSV) limpio con:
1.  Columna `Gender` estandarizada (Male/Female/Other).
2.  `Join_Date` estandarizada (objetos Datetime).
3.  Una nueva columna de bandera `Compensation_Issue` (True/False) basada en palabras clave.
4.  (Opcional) Una nueva columna `extracted_email` extraída de los comentarios usando Regex.
