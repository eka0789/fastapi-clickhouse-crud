import clickhouse_connect

# Inisialisasi client ClickHouse
client = clickhouse_connect.get_client(host='localhost', port=8123)

def create_articles_table():
    client.command("""
        CREATE TABLE IF NOT EXISTS articles (
            id UInt32,
            title String,
            content String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY id
    """)
