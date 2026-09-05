import sqlite3
from models import User

def get_user_by_id(user_id):
    conn = sqlite3.connect('karma.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, karma
        FROM users
        WHERE id = ?""", (user_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return User(id=row[0], username=row[1], karma=row[2])

    return None


def update_user_karma_in_db(user_id, karma):
    conn = sqlite3.connect('karma.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET karma = ?
        WHERE id = ?""", (karma, user_id))

    conn.commit()
    conn.close()


def create_user(username):
    conn = sqlite3.connect('karma.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username) VALUES (?)""", (username,))

    conn.commit()
    conn.close()


def create_habit(title, reward, penalty):
    conn = sqlite3.connect('karma.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO habits (title, reward, penalty)
        VALUES (?, ?, ?)""", (title, reward, penalty))
    
    habit_id = cursor.lastrowid
    
    conn.commit()
    conn.close()

    return habit_id


def assign_habit(user_id, habit_id):
    conn = sqlite3.connect('karma.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO daily_logs (date, user_id, habit_id)
        VALUES (DATE('now'), ?, ?)""", (user_id, habit_id))

    conn.commit()
    conn.close()


def mark_habit_completed(log_id):
    conn = sqlite3.connect('karma.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT daily_logs.user_id, habits.reward 
        FROM daily_logs
        JOIN habits ON daily_logs.habit_id = habits.id
        WHERE daily_logs.id = ? AND daily_logs.is_completed = 0
    """, (log_id,))

    result = cursor.fetchone()

    if result:
        user_id = result[0]
        reward = result[1]

        cursor.execute("""
            UPDATE daily_logs 
            SET is_completed = 1 
            WHERE id = ?
        """, (log_id,))

        cursor.execute("""
            UPDATE users 
            SET karma = karma + ? 
            WHERE id = ?
        """, (reward, user_id))

        conn.commit()

    conn.close()


def get_todays_tasks(user_id):
    conn = sqlite3.connect('karma.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT daily_logs.id, habits.title, habits.reward, daily_logs.is_completed
        FROM daily_logs
        JOIN habits ON daily_logs.habit_id = habits.id
        WHERE daily_logs.user_id = ? AND daily_logs.date = DATE('now')
        """, (user_id,))

    tasks = cursor.fetchall()
    conn.close()
    return tasks
