from flask import Flask, render_template, request, redirect, url_for, session, flash
import database  # Make sure to have database.py in the same directory

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change to your secret key


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    items = database.fetch_items(user_id)
    return render_template('index.html', items=items)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # In a real app, hash and verify this password
        user = database.fetch_user(username)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Remember to hash passwords in a real app
        email = request.form['email']
        database.add_user(username, password, email)
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        completion_date = request.form['completion_date']
        achieved = request.form['achieved'] == 'True'
        user_id = session['user_id']
        database.add_item(name, description, completion_date, achieved, user_id)
        return redirect(url_for('index'))
    return render_template('add_item.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    item = database.fetch_item(id)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        completion_date = request.form['completion_date']
        achieved = request.form['achieved'] == 'True'
        database.update_item(id, name, description, completion_date, achieved)
        return redirect(url_for('index'))
    return render_template('edit_item.html', item=item)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    database.delete_item(id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    database.init_db()
    app.run(debug=True)
