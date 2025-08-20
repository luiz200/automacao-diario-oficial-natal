import requests

def upload_to_0x0(file_path):
    headers = {
        "User-Agent": "MeuUploader/1.0 (contato@email.com)"
    }
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            response = requests.post('https://0x0.st', files=files, headers=headers)
            response.raise_for_status()
            return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"Erro durante o upload: {e}")
        return None
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {file_path}")
        return None

if __name__ == '__main__':
    file_to_upload = r"C:\Users\MKT3\Documents\ProjetoAutomação\automacao-diario-oficial-natal\pdfs\exemplo.pdf"
    short_url = upload_to_0x0(file_to_upload)

    if short_url:
        print(f"URL encurtada: {short_url}")
