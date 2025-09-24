import boto3
import pandas as pd
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",         # Si MySQL está en la misma VM
    user="tu_usuario_mysql",  # Ejemplo: root, utec, etc.
    password="tu_password_mysql",
    database="tu_base_datos"  # Ejemplo: testdb
)

cursor = conexion.cursor()
cursor.execute("SELECT * FROM tu_tabla")  # <-- Cambia por la tabla real

columnas = [desc[0] for desc in cursor.description]
registros = cursor.fetchall()

df = pd.DataFrame(registros, columns=columnas)
ficheroUpload = "data.csv"
df.to_csv(ficheroUpload, index=False)
print(f"✅ CSV generado: {ficheroUpload}")

cursor.close()
conexion.close()

nombreBucket = "asaldarriaga-students"

s3 = boto3.client(
    's3',
    aws_access_key_id="TU_AWS_ACCESS_KEY",      # o usa variables de entorno
    aws_secret_access_key="TU_AWS_SECRET_KEY",  # para no poner claves aquí
    region_name="us-east-1"                     # ajusta si tu bucket es otra región
)

s3.upload_file(ficheroUpload, nombreBucket, ficheroUpload)
print("✅ Ingesta completada y archivo subido a S3")
