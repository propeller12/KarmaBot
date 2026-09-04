import sqlite3
from crud import get_user_by_id, update_user_karma_in_db


def apply_penalties():
    conn = sqlite3.connect('karma.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT daily_logs.user_id, habits.penalty 
        FROM daily_logs
        JOIN habits ON daily_logs.habit_id = habits.id
        WHERE daily_logs.is_completed = 0 AND daily_logs.date = DATE('now')
    """)

    failed_tasks = cursor.fetchall()
    conn.close()

    for i in failed_tasks:
        user_id = i[0]
        penalty = i[1]

        user = get_user_by_id(user_id)
        user.update_karma(-penalty)
        update_user_karma_in_db(user.id, user.karma)

if __name__ == '__main__':
    apply_penalties()
    print("Проверка завершена, штрафы начислены.")