# db.py
import pyodbc

def get_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-648G0K0\\SQLEXPRESS01;'
            'DATABASE=food;'
            'Trusted_Connection=yes;'
            'TrustServerCertificate=yes;'
        )
        print("✅ Connection successful")
        return conn
    except Exception as e:
        print("❌ Connection failed:", e)
        raise
