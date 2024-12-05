import psycopg2
from urllib.parse import urlparse

DATABASE_URL = "postgresql://postgres:YFxorGsFlhatIjFeMgPZEgXOjQNKbodX@autorack.proxy.rlwy.net:13517/railway"

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
