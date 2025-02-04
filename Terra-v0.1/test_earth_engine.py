import ee

CREDENTIALS_FILE = "C:/Users/guill/Documents/Terra/Earth Engine.json"

try:
    ee.Initialize(ee.ServiceAccountCredentials.from_service_account_file(CREDENTIALS_FILE))
    print("✅ Google Earth Engine inicializado correctamente.")
except Exception as e:
    print(f"⚠️ Error al inicializar Earth Engine: {e}")
