# Trabalho 2: Desenvolvimento de Jogo Multiplayer com Sincronização de Estado

Este projeto consiste em um jogo 2D (Pong) com arquitetura cliente-servidor para avaliar o desempenho dos protocolos TCP e UDP em ambientes de rede com latência. O servidor é executado em um container Docker (Raspberry Pi) e o cliente nativamente no host.

## Estrutura do Projeto

* `server.py`: Lógica autoritativa do jogo, física e gerência de conexões.
* `client.py`: Renderização gráfica, predição de estado e coleta de métricas.
* `requirements.txt`: Lista de dependências Python.
* `Dockerfile`: Instruções para build da imagem do servidor.

## Requisitos Prévios

* Python 3.10+
* Docker e Docker Compose (para o servidor)
* Biblioteca Pygame (para o cliente)
