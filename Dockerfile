FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    fonts-liberation libnss3 libxi6 libxcursor1 libxdamage1 libxrandr2 \
    libasound2 libpangocairo-1.0-0 libxss1 libgtk-3-0 libgbm1 \
    chromium chromium-driver \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
COPY automacao.py .
COPY api.py .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/pdfs

ENV DATABASE_URL=postgresql+psycopg2://postgres:Salvares$$$****@db:5432/diariooficial
ENV FLASK_APP=api.py
ENV FLASK_ENV=development
ENV PATH="/usr/bin/chromium:/usr/bin/chromedriver:${PATH}"

CMD ["sh", "-c", "python automacao.py && flask run --host=0.0.0.0 --port=5000"]