import sqlite3

conn = sqlite3.connect("static\database\song.sqlite")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS SONG")

table = """
        CREATE TABLE SONG (
            date TEXT,
            year INT,
            month INT,
            day INT,
            songName TEXT,
            trackID TEXT,
            happy INT,
            sad INT,
            Upbeat INT,
            Calm INT

        );
"""

cursor.execute(table)

print("Song table is now ready")

conn.commit()

conn.close()