import psycopg2
from urllib.parse import urlparse

DATABASE_URL = "postgresql://postgres:YFxorGsFlhatIjFeMgPZEgXOjQNKbodX@postgres-r0l8.railway.internal:5432/railway"

result = urlparse(DATABASE_URL)
print(result)
try:
    conn = psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
    print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)
