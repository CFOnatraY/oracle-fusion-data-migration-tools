import pandas as pd
import math
import os

# Cargar el archivo original
input_file = 'file_input.csv'
df = pd.read_csv(input_file)

# Configuración
registros_por_lote = 1000
inicio_lote = 5

# Calcular número de lotes
total_registros = len(df)
total_lotes = math.ceil(total_registros / registros_por_lote)

# Crear archivos por lote
for i in range(total_lotes):
    inicio = i * registros_por_lote
    fin = inicio + registros_por_lote
    df_lote = df.iloc[inicio:fin]
    
    nombre_archivo = f"ReceivablesCustomerProfile CuentasBillTo - lote {inicio_lote + i}.csv"
    df_lote.to_csv(nombre_archivo, index=False)

    print(f"Archivo generado: {nombre_archivo} con {len(df_lote)} registros")
