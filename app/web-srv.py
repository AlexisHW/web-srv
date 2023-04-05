from flask import Flask, request
from datetime import datetime
from prometheus_flask_exporter import PrometheusMetrics
import sys
import os
import sqlite3

app = Flask(__name__)
metrics = PrometheusMetrics(app)

if len(sys.argv) > 1 and sys.argv[1] == 'sqlite':
    USE_SQLITE = True
    DB_PATH = '/var/log/users.db'
    # create table if it doesn't exist
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            request_time TEXT NOT NULL)
        ''')
else:
    USE_SQLITE = False
    LOG_FILE_PATH = '/var/log/users.log'

@app.route('/hello')
def hello():
    return 'Hello, Exness!'

@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        name = request.form.get('name')
        request_time = datetime.now().strftime('%H:%M:%S - %d.%m.%Y')        

        # Save user data to either log file or sqlite database based on storage type
        if USE_SQLITE:
            cursor.execute('INSERT INTO users (name, request_time) VALUES (?, ?)', (name, request_time))
            conn.commit()       
        else:
            with open(LOG_FILE_PATH, 'a+') as f:
                f.write(f'{name}: {request_time}\n')
        return 'User data saved'

    elif request.method == 'GET':
        name = request.args.get('name')
        result = ''   
        # Return user data from either log file or sqlite database based on storage type
        if USE_SQLITE:
            cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
            user = cursor.fetchall()
            if user:
                for i in user:
                    result = result + '<br>' + f"Request #: {i[0]}, User: {i[1]}, Request Time: {i[2]}"
                return result
            else:
                return 'User not found'
        else:
            with open(LOG_FILE_PATH, 'r') as f:
                for line in f:
                    if f'{name}:' in line:
                        user_data = line.strip().split(': ')
                        result = result + '<br>' + f"User: {user_data[0]}, Request Time: {user_data[1]}"
                if result != '':
                    return result
                else:
                    return 'User not found'
        
    return 'Invalid request'

@app.route('/metrics')
def metrics():
    return metrics.export()

if __name__ == '__main__':
    app.run(host='0.0.0.0')