# ClickHouse Basic Data Operations Python

This example demonstrates fundamental ClickHouse database operations using Python. It connects to a ClickHouse instance, creates a database and table, inserts sample data, and performs basic queries. This illustrates the low-level interactions that a management tool like CH-Ops would abstract and simplify for database administrators.

## Language

`python`

## How to Run

1. Ensure ClickHouse is running locally (e.g., via Docker: `docker run -d --name clickhouse-server --ulimit nofile=262144:262144 -p 8123:8123 -p 9000:9000 clickhouse/clickhouse-server`).
2. Install the required Python library: `pip install clickhouse-connect`.
3. Run the script: `python main.py`.

## Original Article

This example accompanies the Turkish article: [CH-Ops: ClickHouse Yönetimini Basitleştiren Araç](https://fatihsoysal.com/blog/ch-ops-clickhouse-yonetimini-basitlestiren-arac/).

## License

MIT — see [LICENSE](LICENSE).
