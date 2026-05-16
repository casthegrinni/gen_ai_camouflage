import random
import sys

import matplotlib
import matplotlib.backends.backend_agg as agg
import pygame
import pylab
from pygame.locals import *

# Força o matplotlib a renderizar em buffer de memória
matplotlib.use("Agg")

# Importa as suas funções do arquivo core
from camouflage import (
    calculate_fitness,
    crossover,
    generate_heuristic_population,
    mutate,
)

#### CONFIGURAÇÕES GRÁFICAS E HIPERPARÂMETROS ####
WINDOW_SIZE = (800, 460)  # Janela um pouco mais alta para caber os botões
FPS = 15
POPULATION_SIZE = 25
MUTATION_PROBABILITY = 0.15
MUTATION_INTENSITY = 15
ALPHA = 0.5

# Definição dos botões interativos (Preset de cores para trocar o Target)
BUTTONS = [
    {"name": "Vermelho", "color": (200, 20, 20), "rect": pygame.Rect(450, 340, 75, 30)},
    {"name": "Verde", "color": (20, 180, 20), "rect": pygame.Rect(535, 340, 75, 30)},
    {"name": "Azul", "color": (20, 20, 200), "rect": pygame.Rect(620, 340, 75, 30)},
    {"name": "Amarelo", "color": (200, 200, 20), "rect": pygame.Rect(705, 340, 75, 30)},
]

#### FUNÇÕES DE RENDERIZAÇÃO ####


def draw_plot(screen, x, y):
    """Gera o gráfico de fitness via Matplotlib e blita na tela."""
    fig = pylab.figure(figsize=[4, 4], dpi=100)
    ax = fig.gca()
    ax.plot(x, y, color="blue", linewidth=2)
    ax.set_xlabel("Geracao")
    ax.set_ylabel("Erro (Fitness)")
    ax.set_title("Curva de Convergencia")
    pylab.tight_layout()

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (0, 10))
    pylab.close(fig)


def draw_squares(screen, population):
    """Desenha a grade 5x5 de indivíduos."""
    n = 5
    square_size = 50
    distance = 10
    x_offset = 450
    y_offset = 30

    i = 0
    for row in range(n):
        for col in range(n):
            x = col * (square_size + distance) + x_offset
            y = row * (square_size + distance) + y_offset
            pygame.draw.rect(
                screen, (0, 0, 0), (x, y, square_size + 1, square_size + 1)
            )
            pygame.draw.rect(screen, population[i], (x, y, square_size, square_size))
            i += 1


def draw_buttons(screen):
    """Desenha os botões na tela com uma borda branca para destaque."""
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 11, bold=True)

    for btn in BUTTONS:
        # Fundo do botão com a respectiva cor
        pygame.draw.rect(screen, btn["color"], btn["rect"])
        # Borda indicativa
        pygame.draw.rect(screen, (255, 255, 255), btn["rect"], 2)

        # Texto centralizado no botão
        text_surf = font.render(btn["name"], True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=btn["rect"].center)
        screen.blit(text_surf, text_rect)


def draw_text(screen, text, x, y):
    pygame.font.init()
    font = pygame.font.SysFont("Courier New", 14, bold=True)
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x, y))


#### LOOP PRINCIPAL OTIMIZADO ####


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Camouflage Sandbox - Algoritmo Genetico")
    clock = pygame.time.Clock()

    generation = 0
    target_color = [140, 20, 60]  # Alvo inicial dinâmico
    population = generate_heuristic_population(POPULATION_SIZE, target_color, 50)
    best_fitness_values = []

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

            # Monitoramento do clique do mouse para detecção dos botões
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    mouse_pos = event.pos
                    for btn in BUTTONS:
                        if btn["rect"].collidepoint(mouse_pos):
                            # Altera o alvo material em tempo de execução
                            target_color = list(btn["color"])

        # Renderiza o ambiente (fundo)
        screen.fill(target_color)

        # Processamento Genético
        population = sorted(
            population, key=lambda ind: calculate_fitness(ind, target_color)
        )
        best_individual = population[0]
        best_fitness = calculate_fitness(best_individual, target_color)
        best_fitness_values.append(best_fitness)

        generation += 1

        # Renderização de tela
        draw_plot(screen, list(range(len(best_fitness_values))), best_fitness_values)
        draw_squares(screen, population)
        draw_buttons(screen)

        # Painel de texto inferior
        draw_text(screen, f"Geracao: {generation}", 450, 390)
        draw_text(
            screen,
            f"Melhor Solucao: {best_individual} (Erro: {best_fitness})",
            450,
            410,
        )
        draw_text(screen, f"Alvo Ambiente : {tuple(target_color)}", 450, 430)

        pygame.display.flip()
        clock.tick(FPS)

        # REPRODUÇÃO: Só acontece se a população ainda não estiver perfeitamente camuflada
        if best_fitness > 0:
            new_population = [population[0]]  # Elitismo puro
            while len(new_population) < POPULATION_SIZE:
                parent1, parent2 = random.choices(population[:5], k=2)
                child1, child2 = crossover(parent1, parent2, alpha=ALPHA)
                child1 = mutate(child1, MUTATION_PROBABILITY, MUTATION_INTENSITY)
                child2 = mutate(child2, MUTATION_PROBABILITY, MUTATION_INTENSITY)

                new_population.append(child1)
                if len(new_population) < POPULATION_SIZE:
                    new_population.append(child2)
            population = new_population

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
