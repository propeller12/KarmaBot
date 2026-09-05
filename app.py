from flask import Flask, render_template, request, redirect, url_for
from crud import get_user_by_id, create_user, create_habit, assign_habit, get_todays_tasks, mark_habit_completed

app = Flask(__name__)


@app.route('/')
def index():
    user = get_user_by_id(1)

    if not user:
        create_user("Кандидат")
        create_habit("Сделать зарядку", 10, 5)
        create_habit("Почитать книгу", 15, 5)
        assign_habit(1, 1)  # юзер 1, дело 1
        assign_habit(1, 2)  # юзер 1, дело 2
        user = get_user_by_id(1)

    tree_level = user.get_tree_level()

    tasks = get_todays_tasks(user.id)

    return render_template('index.html', user=user, tree_level=tree_level, tasks=tasks)

@app.route('/complete/<int:log_id>', methods=['POST'])
def complete_task(log_id):
    mark_habit_completed(log_id)
    return redirect(url_for('index'))


@app.route('/add_habit', methods=['POST'])
def add_habit():
    title = request.form.get('title')
    reward = int(request.form.get('reward', 10))
    penalty = int(request.form.get('penalty', 5))

    if title:
        new_habit_id = create_habit(title, reward, penalty)

        assign_habit(1, new_habit_id)

if __name__ == '__main__':
    app.run(debug=True)
