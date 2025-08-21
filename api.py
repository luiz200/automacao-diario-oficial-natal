import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

from sqlalchemy import DateTime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Arquivo(db.Model):
    __tablename__ = "arquivos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    caminho = db.Column(db.String, nullable=False)
    competencia = db.Column(db.String, nullable=False)
    data_publicacao = db.Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

@app.route("/api/arquivos", methods=["GET"])
def listar_arquivos():
    competencia = request.args.get("competencia")
    query = Arquivo.query
    if competencia:
        query = query.filter(Arquivo.competencia == competencia)
    arquivos = query.order_by(Arquivo.data_publicacao.desc()).all()
    
    resultado = []
    for arquivo in arquivos:
        resultado.append({
            "id": arquivo.id,
            "nome": arquivo.nome,
            "competencia": arquivo.competencia,
            "data_publicacao": arquivo.data_publicacao.isoformat(),
            "url": arquivo.caminho
        })
    return jsonify(resultado)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)