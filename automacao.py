from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests
import unicodedata
import re
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Arquivo(Base):
    __tablename__ = "arquivos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    caminho = Column(String, nullable=False)
    competencia = Column(String, nullable=False)
    data_publicacao = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

Base.metadata.create_all(engine)

PASTA_DOWNLOAD = os.path.join(os.getcwd(), "pdfs")
os.makedirs(PASTA_DOWNLOAD, exist_ok=True)
print("Pasta de download:", PASTA_DOWNLOAD)

def normalizar_nome(nome):
    for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
        nome = nome.replace(char, '-')
    return nome

def sanitize_filename(filename):
    nfkd = unicodedata.normalize("NFKD", filename)
    filename = "".join([c for c in nfkd if not unicodedata.combining(c)])
    filename = filename.replace(" ", "_")
    filename = re.sub(r"[^a-zA-Z0-9._-]", "", filename)
    return filename

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/chromium"
chrome_options.add_argument("--headless")
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.natal.rn.gov.br/dom")
wait = WebDriverWait(driver, 10)

def pegar_links_pagina():
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table#example a")))
    links = driver.find_elements(By.CSS_SELECTOR, "table#example a")
    resultados = []
    for link in links:
        url = link.get_attribute("href")
        texto = link.text.strip()
        if url and url.endswith(".pdf"):
            resultados.append((texto, url))
    return resultados

paginas = driver.find_elements(By.CSS_SELECTOR, "ul.pagination li.paginate_button a")
num_paginas = len(paginas) if paginas else 1
print(f"Total de páginas: {num_paginas}")

todos_pdfs = []
for i in range(num_paginas):
    paginas = driver.find_elements(By.CSS_SELECTOR, "ul.pagination li.paginate_button a")
    paginas[i].click()
    time.sleep(2)
    todos_pdfs.extend(pegar_links_pagina())

driver.quit()
print(f"Total de PDFs encontrados: {len(todos_pdfs)}")

arquivos_baixados = []
for texto, url in todos_pdfs:
    nome_arquivo = normalizar_nome(texto) + ".pdf"
    caminho_arquivo = os.path.join(PASTA_DOWNLOAD, nome_arquivo)
    
    print(f"Baixando: {texto}")
    try:
        resposta = requests.get(url, stream=True)
        if resposta.status_code == 200:
            with open(caminho_arquivo, "wb") as f:
                for chunk in resposta.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            arquivos_baixados.append(caminho_arquivo)
            print(f"Salvo em: {caminho_arquivo}")
        else:
            print(f"Erro ao baixar {url} - Status {resposta.status_code}")
    except Exception as e:
        print(f"Erro: {e}")

URL_UPLOAD = "https://0x0.st"
urls_publicas = {}

def upload_file(filepath):
    try:
        sanitized_name = sanitize_filename(os.path.basename(filepath))
        headers = {"User-Agent": "MeuUploader/1.0 (contato@email.com)"}
        with open(filepath, "rb") as f:
            files = {"file": (sanitized_name, f)}
            response = requests.post(URL_UPLOAD, files=files, headers=headers)
        if response.status_code == 200:
            return response.text.strip()
    except Exception as e:
        print(f"Erro upload {filepath}: {e}")
    return None

print("\nIniciando uploads para 0x0.st...\n")
for arquivo in arquivos_baixados:
    nome = os.path.basename(arquivo)
    print(f"Enviando {nome} ...")
    link = upload_file(arquivo)
    if link:
        urls_publicas[nome] = link
        print(f"Upload concluído: {link}")

        competencia = datetime.now().strftime("%Y-%m")
        novo_arquivo = Arquivo(
            nome=nome,
            caminho=link,
            competencia=competencia,
            data_publicacao=datetime.utcnow()
        )
        session.add(novo_arquivo)
        session.commit()
        print(f"Salvo no DB: {nome} -> {link}")

print("\nLista final de uploads:")
for nome, link in urls_publicas.items():
    print(f"{nome} -> {link}")

