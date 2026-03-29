import pygame
import socket
import json
import time

# --- CONFIGURAÇÕES ---
SERVER_IP = '192.168.1.2' # Coloque o IP do seu Pi aqui
PORT = 5005
WIDTH, HEIGHT = 800, 600

# --- INICIALIZAÇÃO ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Client - UDP Extrapolation & Metrics")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

# Socket UDP (Não bloqueante)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setblocking(False)

# --- ESTADO E MÉTRICAS ---
state = None
last_packet_time = 0
render_pos = [400, 300] # [x, y] suave
metrics = {"latency": 0, "jitter": 0, "packets_lost": 0}
last_latency = 0

def lerp(start, end, t):
    return start + (end - start) * t

running = True
while running:
    current_time = time.time()
    dt = clock.tick(60) / 1000.0 # Delta time local

    # 1. CAPTURA DE INPUT (Envia para o Servidor)
    keys = pygame.key.get_pressed()
    move = 0
    if keys[pygame.K_UP]: move = -10
    if keys[pygame.K_DOWN]: move = 10
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # Envia o input via UDP (Rápido, sem esperar confirmação)
    try:
        client_socket.sendto(json.dumps({"move": move}).encode(), (SERVER_IP, PORT))
    except: pass

    # 2. RECEBIMENTO DE DADOS (Rede)
    try:
        while True: # Lê todos os pacotes na fila, pega o mais recente
            data, _ = client_socket.recvfrom(1024)
            new_state = json.loads(data.decode())
            
            # Cálculo de Latência para o Relatório
            # (Tempo atual - Timestamp do Servidor)
            this_latency = (current_time - new_state["timestamp"]) * 1000
            metrics["jitter"] = abs(this_latency - last_latency)
            metrics["latency"] = this_latency
            last_latency = this_latency
            
            state = new_state
            last_packet_time = current_time
    except BlockingIOError:
        pass

    # 3. LÓGICA DE SINCRONIZAÇÃO (Onde o trabalho é avaliado)
    if state:
        # A) EXTRAPOLAÇÃO
        # Se não chegou pacote novo, "adivinhamos" onde a bola estaria
        time_diff = current_time - last_packet_time
        extrapolated_x = state["ball_x"] + (state["ball_vx"] * time_diff)
        extrapolated_y = state["ball_y"] + (state["ball_vy"] * time_diff)

        # B) INTERPOLAÇÃO (Suavização de Jitter)
        # Em vez de pular direto para a posição, deslizamos 20% do caminho
        render_pos[0] = lerp(render_pos[0], extrapolated_x, 0.2)
        render_pos[1] = lerp(render_pos[1], extrapolated_y, 0.2)
    else:
        render_pos = [400, 300]

    # 4. DESENHO
    screen.fill((30, 30, 30))
    
    # Desenha a bola (Posição suavizada)
    pygame.draw.circle(screen, (0, 255, 128), (int(render_pos[0]), int(render_pos[1])), 10)
    
    # Desenha raquetes (Vindas do estado do servidor)
    if state:
        pygame.draw.rect(screen, (200, 200, 200), (20, state["p1_y"], 15, 90))
        pygame.draw.rect(screen, (200, 200, 200), (WIDTH-35, state["p2_y"], 15, 90))

    # 5. UI DE MÉTRICAS (Para seu Relatório)
    lat_text = font.render(f"Latência: {metrics['latency']:.1f}ms", True, (255, 255, 255))
    jit_text = font.render(f"Jitter: {metrics['jitter']:.1f}ms", True, (255, 255, 255))
    mode_text = font.render("MODO: UDP (Extrapolação Ativa)", True, (0, 255, 0))
    
    screen.blit(lat_text, (10, 10))
    screen.blit(jit_text, (10, 30))
    screen.blit(mode_text, (10, 50))

    pygame.display.flip()

pygame.quit()
