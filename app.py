from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)

# Habilitar o CORS para permitir requisições do React
CORS(app)

@app.route('/api/members')
def members():
    return jsonify({'members': ['member1', 'member2', 'member34']})

@app.route('/api/hora')
def hora():
    # Retorna a hora atual com segundos
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return jsonify({'hora': current_time})

if __name__ == '__main__':
    app.run()
