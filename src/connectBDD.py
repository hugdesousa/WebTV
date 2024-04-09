import pyodbc

# Connection parameters
server = 'localhost'
database = 'LDDProject'
username = 'SA'
password = 'Password123'

# Create connection string
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password}"
)

try:
    # Establish connection
    conn = pyodbc.connect(conn_str)
    print("Connection established successfully.")

    # You can now execute SQL queries, for example:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Fichier")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Close connection when done
    conn.close()

except pyodbc.Error as e:
    print("Error connecting to the database:", e)