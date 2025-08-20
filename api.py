from flask import Flask, jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuração do PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://usuario:senha@localhost:5432/seu_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Model
class Arquivo(db.Model):
    __tablename__ = "arquivos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    caminho = db.Column(db.String, nullable=False)  # caminho relativo, ex: 'uploads/meuarquivo.pdf'
    competencia = db.Column(db.String, nullable=False)  # Ex: '2025-08'
    data_publicacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Rota pública
@app.route("/api/arquivos", methods=["GET"])
def listar_arquivos():
    """
    Lista arquivos públicos.
    Query string opcional: ?competencia=YYYY-MM
    """
    competencia = request.args.get("competencia")
    query = Arquivo.query

    if competencia:
        query = query.filter(Arquivo.competencia == competencia)

    arquivos = query.order_by(Arquivo.data_publicacao.desc()).all()

    resultado = []
    for arquivo in arquivos:
        # Gera URL pública completa usando url_for
        download_url = url_for('static', filename=arquivo.caminho, _external=True)
        resultado.append({
            "id": arquivo.id,
            "nome": arquivo.nome,
            "competencia": arquivo.competencia,
            "data_publicacao": arquivo.data_publicacao.isoformat(),
            "url": download_url
        })

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True)
