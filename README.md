# Trabalho 2: Desenvolvimento de Jogo Multiplayer com Sincronização de Estado

Este projeto consiste em um jogo 2D (Pong) com arquitetura cliente-servidor para avaliar o desempenho dos protocolos TCP e UDP em ambientes de rede com latência. O servidor é executado em um container Docker (Raspberry Pi) e o cliente nativamente no host.

## Estrutura do Projeto

* `client.py`: Renderização gráfica, predição de estado e coleta de métricas.
* `requirements.txt`: Lista de dependências Python.
* `Dockerfile`: Instruções para build da imagem do servidor.

## Requisitos Prévios

* Python 3.10+
* Docker e Docker Compose (para o servidor)
* Biblioteca Pygame (para o cliente)

## Passo a passo de como rodar

### Com o terminal aberto

* 1 - Instalando o virtual enviroment do Python 

```
sudo apt update
sudo apt install python3-venv python3-full
```

* 2 - Criando o ambiente virutal

```
source venv/bin/activate
```

* 3 - Instalação das dependências

```
pip install -r requirements.txt
```

* 4 - Execução

```
python client.py
```

### OBSERVAÇÃO

Após a instalação, em caso de re-execução do programa pule para o passo 2 e posteriormente para o 4.
