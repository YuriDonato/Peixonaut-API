from flask import Flask
from flask_cors import CORS
from routes import members, hora, economic_events, btc_usdt

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

# Registrar os blueprints de cada rota
app.register_blueprint(members.bp)
app.register_blueprint(hora.bp)
app.register_blueprint(economic_events.bp)
app.register_blueprint(btc_usdt.bp)

if __name__ == '__main__':
    app.run(debug=True)
