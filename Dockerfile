# Použij základní obraz s Pythonem
FROM python:3.9-slim

# Nastav pracovní adresář
WORKDIR /app

# Zkopíruj requirements
COPY requirements.txt .

# Nainstaluj závislosti
RUN pip install --no-cache-dir -r requirements.txt

# Zkopíruj celý projekt
COPY . .

# Exponuj port, na kterém aplikace běží
EXPOSE 5000

# Příkaz pro spuštění aplikace
CMD ["flask", "run", "--host=0.0.0.0"]
