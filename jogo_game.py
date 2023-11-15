import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Configurações do jogo
largura_tela = 800
altura_tela = 600
cor_fundo = (0, 0, 0)

# Configurações da nave
largura_nave = 50
altura_nave = 50
cor_nave = (255, 255, 255)
velocidade_nave = 5

# Configurações dos tiros
largura_tiro = 2
altura_tiro = 5
cor_tiro = (255, 0, 0)
velocidade_tiro = 7

# Configurações dos inimigos
largura_inimigo = 20
altura_inimigo = 20
cor_inimigo = (0, 0, 255)
velocidade_inimigo = 2

# Configurações dos sons
som_explosao = pygame.mixer.Sound("explosao.mp3")
som_tiro = pygame.mixer.Sound("tiro.mp3")

# Configurações da música de fundo
pygame.mixer.music.load("musica_fundo.mp3")
pygame.mixer.music.set_volume(0.5)  # Ajuste o volume conforme necessário
pygame.mixer.music.play(-1)  # -1 para reprodução contínua

# Inicializa a tela do jogo
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Meu Jogo")

# Inicializa a posição da nave
x_nave = largura_tela // 2 - largura_nave // 2
y_nave = altura_tela - altura_nave - 10

# Inicializa a lista de tiros
tiros = []

# Inicializa a lista de inimigos
inimigos = []

# Inicializa a pontuação
pontuacao = 0

# Função para criar um inimigo em uma posição aleatória na parte superior da tela
def criar_inimigo():
    x = random.randint(0, largura_tela - largura_inimigo)
    y = 0
    return pygame.Rect(x, y, largura_inimigo, altura_inimigo)

# Loop principal do jogo
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Captura as teclas pressionadas
    teclas = pygame.key.get_pressed()

    # Movimenta a nave
    if teclas[pygame.K_LEFT] and x_nave > 0:
        x_nave -= velocidade_nave
    if teclas[pygame.K_RIGHT] and x_nave < largura_tela - largura_nave:
        x_nave += velocidade_nave

    # Dispara tiros ao pressionar a tecla de espaço
    if teclas[pygame.K_SPACE]:
        som_tiro.play()
        tiro = pygame.Rect(x_nave + largura_nave // 2 - largura_tiro // 2, y_nave, largura_tiro, altura_tiro)
        tiros.append(tiro)

    # Move os tiros para cima e remove os tiros que saem da tela
    tiros = [tiro for tiro in tiros if tiro.y > 0]
    for tiro in tiros:
        tiro.y -= velocidade_tiro

    # Move os inimigos para baixo e remove os inimigos que atingem o chão
    inimigos = [inimigo for inimigo in inimigos if inimigo.y < altura_tela]
    for inimigo in inimigos:
        inimigo.y += velocidade_inimigo

    # Cria um novo inimigo aleatório a uma taxa determinada
    if random.random() < 0.02:
        inimigos.append(criar_inimigo())

    # Verifica colisões entre tiros e inimigos
    tiros_para_remover = []
    inimigos_para_remover = []
    for tiro in tiros:
        for inimigo in inimigos:
            if tiro.colliderect(inimigo):
                som_explosao.play()
                tiros_para_remover.append(tiro)
                inimigos_para_remover.append(inimigo)
                pontuacao += 10

    # Remove tiros e inimigos colididos
    tiros = [tiro for tiro in tiros if tiro not in tiros_para_remover]
    inimigos = [inimigo for inimigo in inimigos if inimigo not in inimigos_para_remover]

    # Atualiza a tela
    tela.fill(cor_fundo)
    pygame.draw.rect(tela, cor_nave, (x_nave, y_nave, largura_nave, altura_nave))
    for tiro in tiros:
        pygame.draw.rect(tela, cor_tiro, tiro)
    for inimigo in inimigos:
        pygame.draw.rect(tela, cor_inimigo, inimigo)

    # Exibe a pontuação na tela
    fonte = pygame.font.SysFont(None, 36)
    texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
    tela.blit(texto_pontuacao, (10, 10))

    # Atualiza a tela visível
    pygame.display.flip()

    # Define a taxa de atualização
    pygame.time.Clock().tick(60)

    # Adicione no final do arquivo
   

