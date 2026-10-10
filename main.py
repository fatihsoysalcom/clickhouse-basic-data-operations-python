import os
from datetime import datetime
from clickhouse_connect import get_client

# Configuration for ClickHouse connection
# For a real application, these would come from environment variables or a config file
CLICKHOUSE_HOST = os.getenv('CLICKHOUSE_HOST', 'localhost')
CLICKHOUSE_PORT = int(os.getenv('CLICKHOUSE_PORT', 8123)) # Default HTTP port
CLICKHOUSE_USER = os.getenv('CLICKHOUSE_USER', 'default')
CLICKHOUSE_PASSWORD = os.getenv('CLICKHOUSE_PASSWORD', '')
CLICKHOUSE_DB = "ch_ops_demo"

def main():
    print(f"Connecting to ClickHouse at {CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}...")
    client = None # Initialize client to None
    try:
        # Establish a connection to ClickHouse
        # This is the fundamental interaction that CH-Ops would manage and simplify
        client = get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            user=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD
        )
        print("Connection successful.")

        # Create a database if it doesn't exist
        print(f"\nEnsuring database '{CLICKHOUSE_DB}' exists...")
        client.command(f"CREATE DATABASE IF NOT EXISTS {CLICKHOUSE_DB}")
        client.command(f"USE {CLICKHOUSE_DB}") # Switch to the new database
        print(f"Using database '{CLICKHOUSE_DB}'.")

        # Define table name
        table_name = "events"

        # Create a table if it doesn't exist
        print(f"\nEnsuring table '{table_name}' exists...")
        client.command(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                timestamp DateTime,
                event_type String,
                value UInt64
            ) ENGINE = MergeTree()
            ORDER BY timestamp
        """)
        print(f"Table '{table_name}' is ready.")

        # Insert data into the table
        print(f"\nInserting sample data into '{table_name}'...")
        data_to_insert = [
            [datetime.now(), 'page_view', 101],
            [datetime.now(), 'login', 200],
            [datetime.now(), 'page_view', 102],
            [datetime.now(), 'logout', 201],
            [datetime.now(), 'login', 202],
        ]
        # CH-Ops would provide higher-level abstractions for data ingestion and management
        client.insert(table_name, data_to_insert, column_names=['timestamp', 'event_type', 'value'])
        print(f"Inserted {len(data_to_insert)} rows.")

        # Query data from the table
        print(f"\nQuerying all data from '{table_name}':")
        # Management tools often provide dashboards and query interfaces for such operations
        result_all = client.query(f"SELECT * FROM {table_name} ORDER BY timestamp")
        for row in result_all.result_rows:
            print(row)

        print(f"\nQuerying 'login' events from '{table_name}':")
        result_login = client.query(f"SELECT timestamp, value FROM {table_name} WHERE event_type = 'login' ORDER BY timestamp")
        for row in result_login.result_rows:
            print(row)

        # Optional: Clean up the table and database
        # print(f"\nCleaning up: Dropping table '{table_name}' and database '{CLICKHOUSE_DB}'...")
        # client.command(f"DROP TABLE IF EXISTS {table_name}")
        # client.command(f"DROP DATABASE IF EXISTS {CLICKHOUSE_DB}")
        # print("Cleanup complete.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure ClickHouse is running and accessible at the specified host/port.")
        print("Also, ensure 'clickhouse-connect' is installed (pip install clickhouse-connect).")
    finally:
        if client and client.is_connected():
            client.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    main()
