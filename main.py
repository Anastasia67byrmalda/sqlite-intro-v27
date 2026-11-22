
import sqlite3
from pathlib import Path

folder = Path(__file__).resolve().parent
con = sqlite3.connect(folder / "app.db")

con.execute("""
CREATE TABLE IF NOT EXISTS marathons (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    value INTEGER
)
""")

data = [
    ("Звёздный путь", "Фантастика", 350),
    ("Космический горизонт", "Фантастика", 150),
    ("Хроники далёких миров", "Фантастика", 420),
    ("Туманность Андромеды", "Фантастика", 180),
    ("Тайна старого особняка", "Детектив", 240),
    ("След в тумане", "Детектив", 120),
    ("Осень в Петербурге", "Классика", 190),
    ("Записки путешественника", "Классика", 280)
]

count = con.execute(
    "SELECT COUNT(*) FROM marathons"
).fetchone()

if count == 0:
    con.executemany(
        "INSERT INTO marathons (name, category, value) "
        "VALUES (?, ?, ?)",
        data
    )
    con.commit()

print("Все записи:")
for row in con.execute("SELECT * FROM marathons ORDER BY id"):
    print(row)

chosen_category = "Фантастика"
print("\nМарафоны жанра Фантастика:")
rows = con.execute(
    "SELECT * FROM marathons WHERE category = ?",
    (chosen_category,)
).fetchall()
for row in rows:
    print(row)

limit = 200
print("\nКоличество страниц больше 200:")
rows = con.execute(
    "SELECT * FROM marathons WHERE value > ?",
    (limit,)
).fetchall()
for row in rows:
    print(row)

print("\nСортировка по возрастанию количества страниц:")
rows = con.execute(
    "SELECT * FROM marathons ORDER BY value ASC, id ASC"
).fetchall()
for row in rows:
    print(row)

record_id = 2
new_value = 210
con.execute(
    "UPDATE marathons SET value = ? WHERE id = ?",
    (new_value, record_id)
)
con.commit()
print("\nПосле изменения записи:")
print(con.execute(
    "SELECT * FROM marathons WHERE id = ?",
    (record_id,)
).fetchone())

delete_id = 8
con.execute(
    "DELETE FROM marathons WHERE id = ?",
    (delete_id,)
)
con.commit()
print("\nПосле удаления записи:")
for row in con.execute("SELECT * FROM marathons ORDER BY id"):
    print(row)

con.close()
