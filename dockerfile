# Usa uma imagem Python com suporte a bibliotecas de sistema
FROM python:3.11-slim

# Instala dependências do sistema necessárias para o Pygame/SDL2 rodar em modo gráfico
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libx11-6 \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do cliente
COPY cliente.py .

# Variável de ambiente para o Pygame não travar se não houver som
ENV SDL_AUDIODRIVER=dummy

# Comando para rodar o cliente
CMD ["python", "cliente.py"]
