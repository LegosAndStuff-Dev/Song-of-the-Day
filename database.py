import sqlite3

conn = sqlite3.connect("static\database\song.sqlite")
cursor = conn.cursor()

def makeTable():
    yn = input("Would you like to reset or make a song table (y/n)? ")

    if yn == "y":
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
    
    elif yn == "n":
        print("No table was reset or made")

def getNumHappy():
    conn = sqlite3.connect("static\database\song.sqlite", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM SONG WHERE happy=1")

    items = cursor.fetchall()

    return len(items)

def getNumSad():
    pass

def getNumCalm():
    pass

def getNumUpbeat():
    pass

def test():
    cursor.execute(f"""
    INSERT INTO SONG VALUES ("2023-12-20", 20223, 12, 20, "Daylight", "1odExI7RdWc4BT515LTAwj", 1, 0, 1, 0)
    """)

    conn.commit()
    conn.close()

getNumHappy()