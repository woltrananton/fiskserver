from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'fiskar.db'

# Skapa databas om den inte finns
def skapa_databas():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fiskar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                art TEXT NOT NULL,
                langd REAL,
                vikt REAL
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/fiskar', methods=['GET'])
def hamta_fiskar():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM fiskar')
    rader = cursor.fetchall()
    conn.close()
    return jsonify([
        {'id': r[0], 'art': r[1], 'langd': r[2], 'vikt': r[3]}
        for r in rader
    ])

@app.route('/fiskar', methods=['POST'])
def spara_fisk():
    data = request.get_json()
    art = data.get('art')
    langd = data.get('langd')
    vikt = data.get('vikt')

    if not art or langd is None or vikt is None:
        return jsonify({'error': 'Ogiltig data'}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO fiskar (art, langd, vikt) VALUES (?, ?, ?)', (art, langd, vikt))
    conn.commit()
    conn.close()

    return jsonify({'status': 'OK'}), 201

if __name__ == '__main__':
    skapa_databas()
    app.run(debug=True)
