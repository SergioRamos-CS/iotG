from flask import Flask, render_template, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incubadora.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class DadosSensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    temperatura = db.Column(db.Float)
    umidade = db.Column(db.Float)
    aquecedor = db.Column(db.String(10))
    umidificador = db.Column(db.String(10))
    fase = db.Column(db.String(20))

class Configuracao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    t_min = db.Column(db.Float, default=37.5)
    t_max = db.Column(db.Float, default=37.8)
    h_min = db.Column(db.Float, default=50.0)
    h_max = db.Column(db.Float, default=60.0)

with app.app_context():
    db.create_all()
    if not Configuracao.query.first():
        db.session.add(Configuracao())
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config', methods=['GET', 'POST'])
def gerenciar_config():
    conf = Configuracao.query.first()
    if request.method == 'POST':
        data = request.json
        conf.t_min = data['t_min']
        conf.t_max = data['t_max']
        conf.h_min = data['h_min']
        conf.h_max = data['h_max']
        db.session.commit()
        return jsonify({"status": "Configurações aplicadas!"})
    return jsonify({"t_min": conf.t_min, "t_max": conf.t_max, "h_min": conf.h_min, "h_max": conf.h_max})

@app.route('/api/dados', methods=['POST'])
def receber_dados():
    data = request.json
    novo_dado = DadosSensor(
        temperatura=data['temp'], umidade=data['hum'],
        aquecedor=data['heater'], umidificador=data['humidifier'], fase=data['phase']
    )
    db.session.add(novo_dado)
    db.session.commit()
    return jsonify({"status": "sucesso"}), 201

@app.route('/api/atual')
def dados_atuais():
    dado = DadosSensor.query.order_by(DadosSensor.id.desc()).first()
    conf = Configuracao.query.first()
    if dado:
        return jsonify({
            "temp": dado.temperatura, "hum": dado.umidade,
            "heater": dado.aquecedor, "humidifier": dado.umidificador,
            "time": dado.timestamp.strftime('%H:%M:%S'),
            "config": {"t_min": conf.t_min, "t_max": conf.t_max, "h_min": conf.h_min, "h_max": conf.h_max}
        })
    return jsonify({})

@app.route('/exportar')
def exportar_csv():
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')
    query = DadosSensor.query
    if inicio and fim:
        query = query.filter(DadosSensor.timestamp.between(datetime.strptime(inicio, '%Y-%m-%dT%H:%M'), datetime.strptime(fim, '%Y-%m-%dT%H:%M')))
    
    dados = query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Data/Hora', 'Temp', 'Umidade', 'Aquecedor', 'Umidificador'])
    for d in dados:
        writer.writerow([d.timestamp, d.temperatura, d.umidade, d.aquecedor, d.umidificador])
    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=relatorio.csv"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)