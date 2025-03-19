import sqlite3
from hashlib import sha256
from datetime import datetime

# 📌 Create SQLite Database and Table
def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            votes INTEGER,
            comments INTEGER,
            author TEXT,
            date TEXT,
            scrape_time TEXT,
            hash TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def insert_post(title, link, votes, comments, author, date, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Convert votes and comments to integers
    votes = int(votes) if votes.isdigit() else 0
    comments = int(comments.split()[0]) if comments.split()[0].isdigit() else 0
    
    scrape_time = datetime.now()

    # Generate Unique Hash (SHA256 of Title)
    post_hash = sha256(title.encode()).hexdigest()

    try:
        cursor.execute("""
            INSERT INTO posts (title, link, votes, comments, author, date, scrape_time, hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, link, votes, comments, author, date, scrape_time, post_hash))
        
        conn.commit()
        post_id = cursor.lastrowid  # Get the auto-generated ID
    except sqlite3.IntegrityError:
        # print(f"Skipping duplicate post: {title}")
        post_id = None

    conn.close()
    return post_id



# 📌 Search Posts by Title Keyword
def search_posts(keyword, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM posts WHERE title LIKE ?", ('%' + keyword + '%',))
    results = cursor.fetchall()
    
    conn.close()
    return results