import snowflake.connector
import os

conn = snowflake.connector.connect(
    user=os.environ['SNOWFLAKE_USER'],
    password=os.environ['SNOWFLAKE_PASSWORD'],
    account=os.environ['SNOWFLAKE_ACCOUNT'],
    warehouse=os.environ['SNOWFLAKE_WAREHOUSE'],
    database=os.environ['SNOWFLAKE_DATABASE'],
    schema=os.environ['SNOWFLAKE_SCHEMA']
)

cursor = conn.cursor()

def execute_sql_file(path):
    with open(path, 'r') as f:
        sql = f.read()
        for statement in sql.split(";"):
            if statement.strip():
                cursor.execute(statement)

print("Deploying setup scripts...")
execute_sql_file("snowflake/setup/setup_objects.sql")

print("Deploying stored procedures...")
execute_sql_file("snowflake/procedures/load_employee.sql")

print("Deployment completed!")

cursor.close()
conn.close()