import pygame
import sys
import math
import random
import subprocess

# Inicialização do Pygame
pygame.init()

#Recomendado que utilize está mesma configuração
# Configurações do jogo
largura, altura = 1600, 900
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pandemia")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Fonte
fonte = pygame.font.Font(None, 36)

# Texto do menu
titulo = fonte.render("Pandemia", True, (255, 0, 0))
jogar_texto = fonte.render("Jogar", True, PRETO)
descricao_texto = fonte.render("Instruções", True, PRETO)
sair_texto = fonte.render("Sair", True, PRETO)
voltar_texto = fonte.render("Voltar ao Menu", True, PRETO)
texto_som = fonte.render("Ligar/ Desligar Som", True, PRETO)

# Retângulos dos botões
# Coordenadas dos retângulos dos botões
jogar_retangulo = jogar_texto.get_rect(center=(largura // 2, altura // 2 - 30))
descricao_retangulo = descricao_texto.get_rect(center=(largura // 2, altura // 2))
som_retangulo = texto_som.get_rect(center=(largura // 2, altura // 2 + 60))  
sair_retangulo = sair_texto.get_rect(center=(largura // 2, altura // 2 + 120))  

# Retângulos dos botões na tela de fim de jogo
tentar_de_novo_retangulo = None
sair_fim_retangulo = None
voltar_menu_retangulo = voltar_texto.get_rect(center=(largura // 2, altura // 2 + 30))

# Carregar a música do menu
pygame.mixer.music.load('menu_song.mp3')  

# Som do inimigo
som_inimigo_aparece = pygame.mixer.Sound('inimigo_aparece.mp3')  
# Som de eliminação do Inimigo 
som_inimigo_eliminado = pygame.mixer.Sound('inimigo_eliminado.mp3')  

# Variável para controlar o estado do jogo
jogando = False
Tela_Menu = True
som_ligado = True

# Variável para controlar a execução da CutScene
cutscene_executada = False

# URL do vídeo do YouTube
youtube_video_url = "https://youtu.be/hDqqdBw6Oc8" 

# Variável para controlar o estado do jogo após o fim
fim_de_jogo = False

# Variável para controlar a exibição da tela de descrição
mostrar_descricao = False

# Variável para controlar a execução da CutScene
cutscene_executada = False

# Contador de pressionamento da tecla Esc
esc_press_count = 0

# Configuração do clock
clock = pygame.time.Clock()
FPS = 120

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

# Defina a função para tocar a música do menu
def tocar_musica_menu():
    pygame.mixer.music.play(-1)  # -1 faz com que a música se repita indefinidamente

# Função para reiniciar o jogo
def reiniciar_jogo():
    global vida_personagem, pontuacao, rodada_atual, max_inimigos_round, fim_de_jogo
    vida_personagem = 150
    pontuacao = 0
    rodada_atual = 0
    max_inimigos_round = 1
    iniciar_rodada()
    fim_de_jogo = False
    
# Defina a função para controlar ligar/desligar o som
def controlar_som():
    global som_ligado
    if som_ligado:
        pygame.mixer.music.set_volume(0.0)  # Mute o som
        som_ligado = False
    else:
        pygame.mixer.music.set_volume(1.0)  # Ligue o som
        som_ligado = True

# Função para mostrar a tela de fim de jogo
def mostrar_fim_de_jogo():
    global jogando
    fim_de_jogo = True
    jogando = False

# Função para exibir a tela de descrição
def exibir_descricao():
    global mostrar_descricao
    mostrar_descricao = True

# Função para exibir a tela de fim de jogo
def exibir_tela_fim_de_jogo():
    global Tela_Menu
    global fim_de_jogo
    tocar_musica_menu()
    
    # Atualização do clock
    clock.tick(FPS)            

    janela.fill(BRANCO)
    texto_fim = fonte.render("Você foi infectado!", True, (255, 0, 0))
    janela.blit(texto_fim, texto_fim.get_rect(center=(largura // 2, altura // 2 - 100)))

    pro_menu_texto = fonte.render("Voltar para o menu", True, PRETO)
    tentar_de_novo_texto = fonte.render("Tentar de Novo", True, PRETO)
    sair_fim_texto = fonte.render("Sair", True, PRETO)
    tentar_de_novo_retangulo = tentar_de_novo_texto.get_rect(center=(largura // 2, altura // 2 + 50))
    voltar_menu_retangulo = pro_menu_texto.get_rect(center=(largura // 2, altura // 2 + 90))
    sair_fim_retangulo = sair_fim_texto.get_rect(center=(largura // 2, altura // 2 + 130))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_de_jogo = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if tentar_de_novo_retangulo.collidepoint(evento.pos):
                reiniciar_jogo()
                iniciar_jogo()
            if voltar_menu_retangulo.collidepoint(evento.pos):
                Tela_Menu = True
                tocar_musica_menu()
            elif sair_fim_retangulo.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()

    pygame.draw.rect(janela, PRETO, voltar_menu_retangulo, 2)
    janela.blit(pro_menu_texto, voltar_menu_retangulo)
    
    pygame.draw.rect(janela, PRETO, tentar_de_novo_retangulo, 2)
    janela.blit(tentar_de_novo_texto, tentar_de_novo_retangulo)

    pygame.draw.rect(janela, PRETO, sair_fim_retangulo, 2)
    janela.blit(sair_fim_texto, sair_fim_retangulo)

    pygame.display.flip()

def menu():
    global Tela_Menu
    global mostrar_descricao
    global som_ligado
    # Loop do menu
    #while not jogando and not fim_de_jogo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if jogar_retangulo.collidepoint(evento.pos):
                Tela_Menu = False
                reiniciar_jogo()
                iniciar_jogo()
            if descricao_retangulo.collidepoint(evento.pos):
                exibir_descricao()
            if sair_retangulo.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()
            # Verifica se o botão de som foi clicado
            if som_retangulo.collidepoint(evento.pos):
                controlar_som()  # Chama a função para controlar o som
    # Atualização do clock
    clock.tick(FPS)    

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

    # Exibir botão de som
    pygame.draw.rect(janela, PRETO, som_retangulo, 2)
    janela.blit(texto_som, som_retangulo)
    
    # Mantenha o botão "Sair" abaixo dos outros botões
    pygame.draw.rect(janela, PRETO, sair_retangulo, 2)
    janela.blit(sair_texto, sair_retangulo)

    pygame.display.flip()
    
    # Exibir a tela de descrição quando a variável mostrar_descricao for True
    while mostrar_descricao:
        janela.fill(BRANCO)
        descricao = [
            "Grupo",
            "Calebe de Sa Ferreira | TIA: 32088116",
            "Domingos Soares do Carmo Neto | TIA: 32032889",
            "Joao Pedro de Paula Oliveira do Amaral | TIA: 32049390",
            "Mateus de Pasquali da Silva | TIA: 32086997",
            "",
            "Descrição e Ideia do Jogo",
            "Esse jogo gira em torno de uma narrativa ambientada em um mundo pandemia,",
            "desencadeada por um vazamento de um vírus mortal. O protagonista, ciente da importância",
            "da proteção, usa uma máscara como sua principal defesa. O jogo desafia os jogadores a",
            "navegar por um ambiente repleto de desafios, onde a interação social e a saúde pública",
            "desempenham um papel crucial. O protagonista tem a missão de manter sua própria",
            "segurança e proteger aqueles ao seu redor, atirando máscaras nas pessoas que se",
            "aproximam dele sem usar máscaras, incentivando a conscientização e o cumprimento das",
            "medidas de segurança em um cenário pós-pandêmico.",
            "",
            "Teclas e Regras para poder jogar",
            "'W','A','S','D' para poder movimentar o personagem no mapa",
            "A mira é teu mouse então, para mirar nos inimigos use teu ponteiro para apontar nos inimigos que irão te caçar",
            "Para atirar use o botão esquerdo do mouse e para recarregar aperta 'R'",
            "A cada round sobrevivido sua vida é curada",
            "",
            "Pressione 'Esc' para retornar ao menu principal."
        ]

        y_offset = 20
        for linha in descricao:
            texto_descricao = fonte.render(linha, True, PRETO)
            janela.blit(texto_descricao, (20, y_offset))
            y_offset += 36
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                mostrar_descricao = False
                
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if som_retangulo.collidepoint(evento.pos):
                    controlar_som()


# Código do jogo continua aqui...

# Plano de fundo
fundo = pygame.image.load('fundo.png')
fundo = pygame.transform.scale(fundo, (largura, altura))

# Personagem 1
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
    global vida_personagem, max_inimigos_round, rodada_atual, inimigos, max_inimigos_rodada
    max_inimigos_round = 1
    vida_personagem = 150
    rodada_atual += 1
    inimigos = []
    for _ in range(max_inimigos_rodada):
        x = random.randint(0, largura)
        y = random.randint(0, altura)
        inimigos.append([x, y])
    max_inimigos_rodada += 1
    som_inimigo_aparece.play()

iniciar_rodada()

tocar_musica_menu()

# Adicione uma variável para controlar se o botão de tiro foi pressionado
tiro_pressionado = False

# Loop principal do jogo
while True:
    if Tela_Menu == True:
        menu()
    # Verificação do fim do jogo
    elif vida_personagem <= 0:
        exibir_tela_fim_de_jogo()
    else:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
             jogando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    esc_press_count += 1
                    if esc_press_count == 2:
                        jogando = False
                elif evento.key == pygame.K_r:
                    balas_disponiveis = 12
    
        # Atualização do clock
        clock.tick(FPS)

        # Movimentação do personagem
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and personagem_rect.y > 0:
            personagem_rect.y -= personagem_speed
        if teclas[pygame.K_s] and personagem_rect.y < altura - personagem_rect.height:
            personagem_rect.y += personagem_speed
        if teclas[pygame.K_a] and personagem_rect.x > 0:
            personagem_rect.x -= personagem_speed
        if teclas[pygame.K_d] and personagem_rect.x < largura - personagem_rect.width:
            personagem_rect.x += personagem_speed

            # Restaurar o contador se não houver pressionamento da tecla Esc
        if not pygame.key.get_pressed()[pygame.K_ESCAPE]:
            esc_press_count = 0

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
            inimigo[0] = max(0, min(largura - inimigo_imagem.get_width(), inimigo[0] + math.cos(angulo) * inimigo_speed))
            inimigo[1] = max(0, min(altura - inimigo_imagem.get_height(), inimigo[1] + math.sin(angulo) * inimigo_speed))

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
                # som_inimigo_eliminado.play()
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

        # Atualização da tela
        pygame.display.flip()

# Encerramento do jogo
pygame.quit()
sys.exit()