
import pyodbc

# SQL Server connection details
server = 'DESKTOP-648G0K0\\SQLEXPRESS01'
database = 'food'
driver = '{ODBC Driver 17 for SQL Server}'  # Ensure this driver is installed

# Windows Authentication
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes'

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Create or verify tbl_Accounts table
cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'tbl_Accounts')
    CREATE TABLE tbl_Accounts (
        AccountId INT IDENTITY(1,1) PRIMARY KEY,
        AccountUsername NVARCHAR(MAX) NOT NULL,
        AccountPassword NVARCHAR(MAX) NOT NULL,
        AccountRole NVARCHAR(MAX),
        PhoneNumber NVARCHAR(50),
        Address NVARCHAR(50)
    )
""")
conn.commit()
print(f"SQL Server database initialized with connection: {conn}")

def get_connection():
    return conn

__all__ = ['conn', 'get_connection']
