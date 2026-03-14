import snowflake.connector
import os
from cryptography.hazmat.primitives import serialization

# Load private key from GitHub Secret
private_key_pem = os.environ['SNOWFLAKE_PRIVATE_KEY'].encode()

# Deserialize the PEM key
p_key = serialization.load_pem_private_key(
    private_key_pem,
    password=None
)

# Convert to DER format required by Snowflake
private_key = p_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=os.environ['SNOWFLAKE_USER'],
    account=os.environ['SNOWFLAKE_ACCOUNT'],
    private_key=private_key,
    warehouse=os.environ['SNOWFLAKE_WAREHOUSE'],
    database=os.environ['SNOWFLAKE_DATABASE'],
    schema=os.environ['SNOWFLAKE_SCHEMA']
)

def execute_sql_file(path):
    with open(path, "r") as f:
        sql = f.read()
        cursor.execute(sql)

cursor = conn.cursor()
cursor.execute("SELECT CURRENT_USER(), CURRENT_ROLE()")
print(cursor.fetchone())

# print("Deploying setup scripts...")
# execute_sql_file("snowflake/setup/snowflake_setup.sql")

print("Deploying stored procedures...")
execute_sql_file("snowflake/procedure/load_employee.sql")

print("Deployment completed!")

cursor.close()
conn.close()