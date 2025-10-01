import sqlite3
from typing import List, Dict
from datetime import datetime

class DatabaseManager:
    """
    Handles SQLite database interactions for Hacker News stories.
    """

    def __init__(self, db_name: str = "hackernews.db") -> None:
        self.db_name = db_name
        self._create_table()

    def _create_table(self) -> None:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hackernews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    link TEXT NOT NULL,
                    points INTEGER,
                    date_created TEXT, -- stored as ISO 8601
                    UNIQUE(title, link)
                )
            """)
            conn.commit()

    def insert_stories(self, stories: List[Dict]) -> None:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.executemany("""
                INSERT OR IGNORE INTO hackernews (title, link, points, date_created)
                VALUES (?, ?, ?, ?)
            """, [
                (
                    s["title"],
                    s["link"],
                    s["points"],
                    s["date_created"].isoformat() if isinstance(s["date_created"], datetime) else None
                )
                for s in stories
            ])
            conn.commit()

    def update_story_points(self,stories) -> None:
        new_stories = []
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title, link FROM hackernews")
            existing_keys = {(row[0], row[1]) for row in cursor.fetchall()}
            for s in stories:
                key = (s["title"], s["link"])
                if key in existing_keys:
                    cursor.execute("""
                        UPDATE hackernews
                        SET points = ?
                        WHERE title = ? AND link = ?
                    """, (s["points"], s["title"], s["link"]))
                else:
                    new_stories.append(s)
            conn.commit()
            if len(new_stories) > 0:
                self.insert_stories(new_stories)

    def fetch_newest_story(self) -> Dict | None:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT title, link, points, date_created
                FROM hackernews
                WHERE date_created IS NOT NULL
                ORDER BY date_created DESC
                LIMIT 1
            """)
            row = cursor.fetchone()

        if row:
            clean_date = None
            if row[3]:
                try:
                    iso_part = row[3].split()[0]  # strip unix timestamp if it exists
                    clean_date = datetime.fromisoformat(iso_part)
                except ValueError:
                    clean_date = None

            return {
                "title": row[0],
                "link": row[1],
                "points": row[2],
                "date_created": clean_date
            }
        return None


    def fetch_all_stories(self) -> List[Dict]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT title, link, points, date_created
                FROM hackernews
            """)
            rows = cursor.fetchall()

        return [
            {
                "title": r[0],
                "link": r[1],
                "points": r[2],
                "date_created": datetime.fromisoformat(r[3].split()[0]) if r[3] else None
            }
            for r in rows
        ]