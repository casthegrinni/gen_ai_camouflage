import random
from typing import List, Tuple


def generate_random_population(population_size) -> List[Tuple[int, int, int]]:
    # Gera lista contendo a população inicial aleatória
    population = []
    for _ in range(population_size):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        population.append((r, g, b))
    return population


def generate_heuristic_population(
    population_size: int, target_color: Tuple[int, int, int], spread: int = 50
) -> List[Tuple[int, int, int]]:
    """
    HEURÍSTICA: Amostragem de Proximidade (Local Search Initialization).
    Em vez de chutar cores totalmente aleatórias, começamos com cores que já estão
    em uma 'vizinhança' do alvo, mas com algum ruído para manter a diversidade.
    """
    population = []
    for _ in range(population_size):
        # Gera uma cor variando em torno do alvo dentro do limite 'spread'
        r = max(0, min(255, target_color[0] + random.randint(-spread, spread)))
        g = max(0, min(255, target_color[1] + random.randint(-spread, spread)))
        b = max(0, min(255, target_color[2] + random.randint(-spread, spread)))
        population.append((r, g, b))
    return population


def calculate_fitness(individual, target_color) -> int:
    """
    Calcula a qualidade do indivíduo em relação ao ambiente.
    Como queremos camuflagem, o fitness é a SOMA DOS ERROS ABSOLUTOS de cada canal.
    Menor erro = melhor adaptado (mais próximo de 0).
    """

    # Desestruturando as tuplas
    r_ind, g_ind, b_ind = individual
    r_targ, g_targ, b_targ = target_color

    # Calculando a diferença absoluta de cada canal
    error_r = abs(r_ind - r_targ)
    error_g = abs(g_ind - g_targ)
    error_b = abs(b_ind - b_targ)

    # A soma de todos os erros é o fitness (Nesse caso quanto menor, melhor)
    fitness = error_r + error_g + error_b
    return fitness


def crossover(
    parent1: Tuple[int, int, int], parent2: Tuple[int, int, int], alpha: float = 0.5
) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
    """
    Realiza o cruzamento aritmético (média ponderada) entre dois pais RGB.
    Gera dois filhos baseados no hiperparâmetro alpha.
    """
    r1, g1, b1 = parent1
    r2, g2, b2 = parent2

    alpha = 0.5

    r1_child = calc_child1(alpha, r1, r2)
    g1_child = calc_child1(alpha, g1, g2)
    b1_chidl = calc_child1(alpha, b1, b2)

    r2_child = calc_child2(alpha, r1, r2)
    g2_child = calc_child2(alpha, g1, g2)
    b2_child = calc_child2(alpha, b1, b2)

    child1 = (r1_child, g1_child, b1_chidl)
    child2 = (r2_child, g2_child, b2_child)

    return child1, child2


def calc_child1(alpha, parent_1, parent_2) -> int:
    result = alpha * parent_1 + (1 - alpha) * parent_2
    return int(round(result))


def calc_child2(alpha, parent_1, parent_2) -> int:
    result = (1 - alpha) * parent_1 + alpha * parent_2
    return int(round(result))


def mutate(
    individual: Tuple[int, int, int],
    mutation_probability: float,
    mutation_intensity: int = 20,
) -> Tuple[int, int, int]:
    """
    Aplica mutação adicionando ruído aos canais RGB caso a probabilidade seja aceita.
    Garante que os valores finais fiquem rigidamente entre 0 e 255.
    """
    r, g, b = individual

    # 1. Calculando o ruído para cada canal usando o operador ternário do Python
    ruido_r = (
        random.randint(-mutation_intensity, mutation_intensity)
        if random.random() < mutation_probability
        else 0
    )
    ruido_g = (
        random.randint(-mutation_intensity, mutation_intensity)
        if (random.random() < mutation_probability)
        else 0
    )
    ruido_b = (
        random.randint(-mutation_intensity, mutation_intensity)
        if (random.random() < mutation_probability)
        else 0
    )

    # 2. Somando o ruído ao valor original
    r += ruido_r
    g += ruido_g
    b += ruido_b

    # 3. Aplicando a trava de segurança para manter entre 0 e 255
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))

    return (r, g, b)


# ==========================================
# FASE 2: O LOOP DE CONTROLE (EXECUÇÃO)
# ==========================================
if __name__ == "__main__":
    # Hiperparâmetros do Algoritmo
    TARGET_COLOR = [140, 20, 60]  # A cor de fundo que queremos imitar
    POPULATION_SIZE = 100  # Tamanho da grade de indivíduos
    N_GENERATIONS = 100  # Quantas eras o algoritmo vai rodar
    MUTATION_PROBABILITY = 0.1  # 10% de chance de mutação por canal
    MUTATION_INTENSITY = 15  # Força do ruído gerado na mutação
    ALPHA = 0.5  # Peso do crossover aritmético

    print(f"Iniciando simulação. Alvo: {TARGET_COLOR}\n")

    # 1. Inicializa a população aleatória (Fase 1)
    population = generate_heuristic_population(POPULATION_SIZE, TARGET_COLOR, 50)

    # Execução do laço das gerações
    for generation in range(1, N_GENERATIONS + 1):
        # Passo 1: Ordenar a população pelo fitness (menor erro primeiro)
        # Usamos uma função lambda para avaliar cada indivíduo em tempo de execução
        population = sorted(
            population, key=lambda ind: calculate_fitness(ind, TARGET_COLOR)
        )

        # Coleta dados do campeão atual para monitoramento
        best_individual = population[0]
        best_fitness = calculate_fitness(best_individual, TARGET_COLOR)

        # Print de controle para você assistir a evolução material acontecer
        print(
            f"Geração {generation:03d} | Melhor Fitness: {best_fitness:03d} | Melhor Cor: {best_individual}"
        )

        # Condição de parada ideal: se camuflou perfeitamente, encerra o loop
        if best_fitness == 0:
            print("\n[SUCESSO] Camuflagem perfeita alcançada!")
            break

        # Passo 2: Elitismo (Salva o campeão direto na nova população)
        new_population = [best_individual]

        # Passo 3, 4 e 5: Repopular o resto da sociedade
        while len(new_population) < POPULATION_SIZE:
            # Seleção: Escolhe dois pais aleatórios entre os top 10 melhores colocados
            parent1, parent2 = random.choices(population[:10], k=2)

            # Crossover Aritmético
            child1, child2 = crossover(parent1, parent2, alpha=ALPHA)

            # Mutação Numérica
            child1 = mutate(child1, MUTATION_PROBABILITY, MUTATION_INTENSITY)
            child2 = mutate(child2, MUTATION_PROBABILITY, MUTATION_INTENSITY)

            # Adiciona os novos filhos à próxima geração
            new_population.append(child1)
            # Garante que não vai estourar o tamanho limite se a população for ímpar
            if len(new_population) < POPULATION_SIZE:
                new_population.append(child2)

        # Atualiza a população principal para a próxima iteração
        population = new_population

    print(f"\nFim da simulação. Melhor resultado final: {population[0]}")
