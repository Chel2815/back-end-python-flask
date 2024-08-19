from flask import Flask
import sqlite3
app = Flask(__name__) # Explicação abaixo da variável __name__

@app.route('/')
def hello_world():
 return 'Hello, World!'
if __name__ == '__main__':
 app.run(debug=True)

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS example (id INTEGER PRIMARY KEY, name TEXT)')
conn.commit()
conn.close()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO example (name) VALUES (?)', (data['name'],))
    conn.commit()
    conn.close()
    return jsonfy({'status': 'Data inserted'})

@app.route('/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM example').fetchall()
    conn.close()
    return jsonfy([dict(row) for row in data])

@