import pygame
import sys
import math
import random
import subprocess

# Inicialização do Pygame
pygame.init()

# Configurações do jogo
largura, altura = 1600, 800
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pandemia")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Fonte
fonte = pygame.font.Font(None, 36)

# Texto do menu
titulo = fonte.render("Pandemia", True, PRETO)
jogar_texto = fonte.render("Jogar", True, PRETO)
descricao_texto = fonte.render("Descrição", True, PRETO)
cutscene_texto = fonte.render("CutScene", True, PRETO)
sair_texto = fonte.render("Sair", True, PRETO)
voltar_texto = fonte.render("Voltar ao Menu", True, PRETO)

# Retângulos dos botões
jogar_retangulo = jogar_texto.get_rect(center=(largura // 2, altura // 2 - 30))
descricao_retangulo = descricao_texto.get_rect(center=(largura // 2, altura // 2))
cutscene_retangulo = cutscene_texto.get_rect(center=(largura // 2, altura // 2 + 30))
sair_retangulo = sair_texto.get_rect(center=(largura // 2, altura // 2 + 60))

# Retângulos dos botões na tela de fim de jogo
tentar_de_novo_retangulo = None
sair_fim_retangulo = None
voltar_menu_retangulo = voltar_texto.get_rect(center=(largura // 2, altura // 2 + 30))

# Configuração do clock
clock = pygame.time.Clock()
FPS = 120

# Variável para controlar o estado do jogo
jogando = False

# Variável para controlar a execução da CutScene
cutscene_executada = False

# Variável para controlar o estado do jogo após o fim
fim_de_jogo = False

# Variável para controlar a exibição da tela de descrição
mostrar_descricao = False

# Função para iniciar o jogo principal
def iniciar_jogo():
    global jogando
    jogando = True

# Função para iniciar a CutScene (vídeo)
def iniciar_cutscene():
    global cutscene_executada
    cutscene_executada = True
    pygame.mixer.music.stop()
    subprocess.Popen(['vlc', 'historia.mp4'])

# Função para reiniciar o jogo
def reiniciar_jogo():
    global vida_personagem, pontuação, rodada_atual, max_inimigos_rodada, fim_de_jogo
    vida_personagem = 150
    pontuação = 0
    rodada_atual = 0
    max_inimigos_rodada = 1
    iniciar_rodada()
    fim_de_jogo = False

# Função para mostrar a tela de fim de jogo
def mostrar_fim_de_jogo():
    global jogando
    fim_de_jogo = True
    jogando = False

# Função para exibir a tela de descrição
def exibir_descricao():
    global mostrar_descricao
    mostrar_descricao = True

# Loop do menu
while not jogando and not fim_de_jogo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if jogar_retangulo.collidepoint(evento.pos):
                iniciar_jogo()
            if descricao_retangulo.collidepoint(evento.pos):
                exibir_descricao()
            if cutscene_retangulo.collidepoint(evento.pos):
                iniciar_cutscene()
            if sair_retangulo.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()

    # Preencha a tela com fundo branco
    janela.fill(BRANCO)

    # Desenhe o texto do menu com borda preta
    janela.blit(titulo, titulo.get_rect(center=(largura // 2, altura // 2 - 100)))

    # Adicione a opção "Descrição" no menu
    pygame.draw.rect(janela, PRETO, jogar_retangulo, 2)
    janela.blit(jogar_texto, jogar_retangulo)

    # Adicione o botão "Descrição" acima do botão "CutScene"
    pygame.draw.rect(janela, PRETO, descricao_retangulo, 2)
    janela.blit(descricao_texto, descricao_retangulo)
    
    pygame.draw.rect(janela, PRETO, cutscene_retangulo, 2)
    janela.blit(cutscene_texto, cutscene_retangulo)
    
    # Mantenha o botão "Sair" abaixo dos outros botões
    pygame.draw.rect(janela, PRETO, sair_retangulo, 2)
    janela.blit(sair_texto, sair_retangulo)

    pygame.display.flip()

    # Exibir a tela de descrição quando a variável mostrar_descricao for True
    if mostrar_descricao:
        janela.fill(BRANCO)
        descricao = [
            "Grupo",
            "Calebe de Sa Ferreira | TIA: 32088116",
            "Domingos Soares do Carmo Neto | TIA: 32032889",
            "Joao Pedro de Paula Oliveira do Amaral | TIA: 32049390",
            "Mateus de Pasquali da Silva | TIA: 32086997",
            "",
            "Descrição e Ideia do Jogo",
            "Esse jogo gira em torno de uma narrativa ambientada em um mundo pós-pandemia,",
            "desencadeada por um vazamento de um vírus mortal. O protagonista, ciente da importância",
            "da proteção, usa uma máscara como sua principal defesa. O jogo desafia os jogadores a",
            "navegar por um ambiente repleto de desafios, onde a interação social e a saúde pública",
            "desempenham um papel crucial. O protagonista tem a missão de manter sua própria",
            "segurança e proteger aqueles ao seu redor, atirando máscaras nas pessoas que se",
            "aproximam dele sem usar máscaras, incentivando a conscientização e o cumprimento das",
            "medidas de segurança em um cenário pós-pandêmico.",
            "",
            "Pressione 'Esc' ou 'Voltar ao Menu' para retornar ao menu principal."
        ]
        y_offset = 20
        for linha in descricao:
            texto_descricao = fonte.render(linha, True, PRETO)
            janela.blit(texto_descricao, (20, y_offset))
            y_offset += 36
        pygame.draw.rect(janela, PRETO, voltar_menu_retangulo, 2)
        janela.blit(voltar_texto, voltar_menu_retangulo)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                mostrar_descricao = False

# Código do jogo continua aqui...

# Plano de fundo
fundo = pygame.image.load('fundo.png')
fundo = pygame.transform.scale(fundo, (largura, altura))

# Personagem
personagem_imagem = pygame.image.load('personagem.png')
personagem_rect = personagem_imagem.get_rect()
personagem_rect.center = (largura // 2, altura // 2)
personagem_speed = 5

# Inimigos
inimigos = []
inimigo_imagem = pygame.image.load('inimigo.png')
inimigo_speed = 1

# Balas
balas = []
bala_imagem = pygame.image.load('bala.png')
balas_disponíveis = 12

# Pontuação
pontuação = 0

# Vida do personagem
vida_personagem = 150

# Número da rodada
rodada_atual = 0
max_inimigos_rodada = 1

def iniciar_rodada():
    global rodada_atual, inimigos, max_inimigos_rodada
    rodada_atual += 1
    inimigos = []
    for _ in range(max_inimigos_rodada):
        x = random.randint(0, largura)
        y = random.randint(0, altura)
        inimigos.append([x, y])
    max_inimigos_rodada += 1

iniciar_rodada()

# Loop principal do jogo
while jogando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False

    # Atualização do clock
    clock.tick(FPS)

    # Movimentação do personagem
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w]:
        personagem_rect.y -= personagem_speed
    if teclas[pygame.K_s]:
        personagem_rect.y += personagem_speed
    if teclas[pygame.K_a]:
        personagem_rect.x -= personagem_speed
    if teclas[pygame.K_d]:
        personagem_rect.x += personagem_speed

    # Atualização da direção do personagem em relação ao mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    direcao_x = mouse_x - personagem_rect.centerx
    direcao_y = mouse_y - personagem_rect.centery
    angulo = math.atan2(direcao_y, direcao_x)
    personagem_rotacionado = pygame.transform.rotate(personagem_imagem, math.degrees(angulo))
    personagem_rect = personagem_rotacionado.get_rect(center=personagem_rect.center)

    # Atualização da posição dos inimigos em relação ao jogador
    for inimigo in inimigos:
        direcao_x = personagem_rect.centerx - inimigo[0]
        direcao_y = personagem_rect.centery - inimigo[1]
        angulo = math.atan2(direcao_y, direcao_x)
        inimigo[0] += math.cos(angulo) * inimigo_speed
        inimigo[1] += math.sin(angulo) * inimigo_speed

    # Disparo de balas
    if pygame.mouse.get_pressed()[0] and balas_disponíveis > 0:
        bala_x = personagem_rect.centerx
        bala_y = personagem_rect.centery
        direcao_x = mouse_x - bala_x
        direcao_y = mouse_y - bala_y
        angulo = math.atan2(direcao_y, direcao_x)
        bala_vel_x = math.cos(angulo) * 10
        bala_vel_y = math.sin(angulo) * 10
        balas.append([bala_x, bala_y, bala_vel_x, bala_vel_y])
        balas_disponíveis -= 1

    # Atualização das balas
    balas = [[x + vel_x, y + vel_y, vel_x, vel_y] for x, y, vel_x, vel_y in balas]

    # Remoção das balas que saíram da tela
    balas = [bala for bala in balas if 0 < bala[0] < largura and 0 < bala[1] < altura]

    # Detecção de colisão entre balas e inimigos
    for inimigo in inimigos:
        colisoes = [bala for bala in balas if pygame.Rect(inimigo[0], inimigo[1], inimigo_imagem.get_width(), inimigo_imagem.get_height()).colliderect((bala[0], bala[1], bala_imagem.get_width(), bala_imagem.get_height()))]
        if colisoes:
            pontuação += 10 * len(colisoes)
            for colisão in colisoes:
                balas.remove(colisão)
            inimigos.remove(inimigo)

    # Atualização da vida do personagem
    for inimigo in inimigos:
        if pygame.Rect(personagem_imagem.get_rect(center=personagem_rect.center)).colliderect(inimigo_imagem.get_rect(center=(inimigo[0], inimigo[1]))):
            vida_personagem -= 10

    # Recarrega balas ao pressionar "R"
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_r]:
        balas_disponíveis = 12

    # Limpeza da tela
    janela.blit(fundo, (0, 0))

    # Desenho dos elementos
    janela.blit(personagem_rotacionado, personagem_rect.topleft)
    for inimigo in inimigos:
        janela.blit(inimigo_imagem, (inimigo[0], inimigo[1]))
    for bala in balas:
        janela.blit(bala_imagem, (bala[0], bala[1]))

    # Exibição da pontuação
    texto_pontuação = fonte.render(f'Pontuação: {pontuação}', True, (255, 0, 0))
    janela.blit(texto_pontuação, (10, 10))

    # Exibição das balas disponíveis
    texto_balas = fonte.render(f'Balas: {balas_disponíveis}', True, (255, 0, 0))
    janela.blit(texto_balas, (10, 50))

    # Exibição da vida do personagem
    texto_vida = fonte.render(f'Vida: {vida_personagem}', True, (255, 0, 0))
    janela.blit(texto_vida, (10, 90))

    # Exibição do número da rodada
    texto_rodada = fonte.render(f'Rodada: {rodada_atual}', True, (255, 0, 0))
    janela.blit(texto_rodada, (10, 130))

    # Verificação do fim da rodada
    if not inimigos:
        iniciar_rodada()

    # Verificação do fim do jogo
    if vida_personagem <= 0:
        mostrar_fim_de_jogo()

    # Atualização da tela
    pygame.display.flip()

# Tela de fim de jogo
while fim_de_jogo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_de_jogo = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if tentar_de_novo_retangulo.collidepoint(evento.pos):
                reiniciar_jogo()
            if sair_fim_retangulo.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()

    janela.fill(BRANCO)
    texto_fim = fonte.render("Você foi infectado", True, PRETO)
    janela.blit(texto_fim, texto_fim.get_rect(center=(largura // 2, altura // 2 - 100)))

    tentar_de_novo_texto = fonte.render("Tentar de Novo", True, PRETO)
    sair_fim_texto = fonte.render("Sair", True, PRETO)
    tentar_de_novo_retangulo = tentar_de_novo_texto.get_rect(center=(largura // 2, altura // 2 + 30))
    sair_fim_retangulo = sair_fim_texto.get_rect(center=(largura // 2, altura // 2 + 80))

    pygame.draw.rect(janela, PRETO, tentar_de_novo_retangulo, 2)
    janela.blit(tentar_de_novo_texto, tentar_de_novo_retangulo)
    pygame.draw.rect(janela, PRETO, sair_fim_retangulo, 2)
    janela.blit(sair_fim_texto, sair_fim_retangulo)

    pygame.display.flip()

# Encerramento do jogo
pygame.quit()
sys.exit()