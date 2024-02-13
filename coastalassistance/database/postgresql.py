import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="coastal_db",
    user="coe",
    password="your_password",
    host="localhost"
)

# Создание курсора
cur = conn.cursor()

# Пример создания таблицы
cur.execute("""
    CREATE TABLE IF NOT EXISTS your_table_name (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER
    )
""")

# Пример выполнения SQL-запроса
cur.execute("INSERT INTO your_table_name (name, age) VALUES (%s, %s)", ("Alice", 30))

# Подтверждение изменений
conn.commit()

# Закрытие курсора и соединения
cur.close()
conn.close()
