import psycopg2

connection = psycopg2.connect(
    host="umar",
    database="Mirzajonov",
    user="khanjon",
    password="1"
)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id SERIAL PRIMARY KEY,
        category_id INTEGER REFERENCES categories(id),
        title VARCHAR(200) NOT NULL,
        content TEXT NOT NULL,
        published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_published BOOLEAN DEFAULT FALSE
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id SERIAL PRIMARY KEY,
        news_id INTEGER REFERENCES news(id),
        author_name VARCHAR(100),
        comment_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

connection.commit()
print("Jadvallar muvaffaqiyatli yaratildi.")

cursor.execute("""
    ALTER TABLE news ADD COLUMN IF NOT EXISTS views INTEGER DEFAULT 0;
""")

cursor.execute("""
    ALTER TABLE comments ALTER COLUMN author_name TYPE TEXT;
""")

connection.commit()
print("Jadvallar muvaffaqiyatli o'zgartirildi.")

cursor.executemany("""
    INSERT INTO categories (name, description)
    VALUES (%s, %s);
""", [
    ("Technology", "All about technology."),
    ("Sports", "Latest sports news."),
    ("Health", "Health and wellness tips.")
])

cursor.executemany("""
    INSERT INTO news (category_id, title, content)
    VALUES (%s, %s, %s);
""", [
    (1, "Tech Trends 2024", "The latest in tech."),
    (2, "Football Updates", "Recent matches reviewed."),
    (3, "Healthy Living", "Top health tips for 2024.")
])

cursor.executemany("""
    INSERT INTO comments (news_id, author_name, comment_text)
    VALUES (%s, %s, %s);
""", [
    (1, "Alice", "Great article on technology!"),
    (2, "Bob", "Interesting sports updates."),
    (3, "Charlie", "Very useful health tips.")
])

connection.commit()
print("Ma'lumotlar muvaffaqiyatli qo'shildi.")

cursor.execute("""
    UPDATE news SET views = views + 1;
""")

cursor.execute("""
    UPDATE news
    SET is_published = TRUE
    WHERE published_at < NOW() - INTERVAL '1 day';
""")

connection.commit()
print("Ma'lumotlar muvaffaqiyatli yangilandi.")

cursor.execute("""
    DELETE FROM comments
    WHERE created_at < NOW() - INTERVAL '1 year';
""")

connection.commit()
print("Eski sharhlar o'chirildi.")


cursor.execute("""
    SELECT n.id AS news_id, n.title AS news_title, c.name AS category_name
    FROM news n
    JOIN categories c ON n.category_id = c.id;
""")
print(cursor.fetchall())

cursor.execute("""
    SELECT * FROM news WHERE category_id = (
        SELECT id FROM categories WHERE name = 'Technology'
    );
""")
print(cursor.fetchall())

cursor.execute("""
    SELECT * FROM news
    WHERE is_published = TRUE
    ORDER BY published_at DESC
    LIMIT 5;
""")
print(cursor.fetchall())

cursor.execute("""
    SELECT * FROM news WHERE views BETWEEN 10 AND 100;
""")
print(cursor.fetchall())

cursor.execute("""
    SELECT * FROM comments WHERE author_name LIKE 'A%';
""")
print(cursor.fetchall())

cursor.execute("""
    SELECT * FROM comments WHERE author_name IS NULL;
""")
print(cursor.fetchall())

cursor.execute("""
    SELECT c.name, COUNT(n.id) AS news_count
    FROM categories c
    LEFT JOIN news n ON c.id = n.category_id
    GROUP BY c.name;
""")
print(cursor.fetchall())

cursor.execute("""
    ALTER TABLE news ADD CONSTRAINT unique_title UNIQUE (title);
""")

connection.commit()
print("Qo'shimcha cheklov qo'shildi.")

cursor.close()
connection.close()
print("Bog'lanish yopildi.")
