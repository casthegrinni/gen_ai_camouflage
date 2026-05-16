# Desafio de Camuflagem - Algoritmo Genético

Este projeto foi desenvolvido como parte dos estudos da segunda etapa da **FIAP - IA para Devs**. O objetivo é implementar um Algoritmo Genético (AG) capaz de evoluir uma população de cores (indivíduos RGB) para que se camuflem perfeitamente em uma cor de fundo (ambiente).

## 🚀 Sobre o Projeto

O desafio consiste em aplicar os conceitos fundamentais de computação evolutiva:
- **População Inicial:** Geração aleatória ou heurística de cores RGB.
- **Função de Fitness (Aptidão):** Cálculo da diferença absoluta entre as cores dos indivíduos e a cor alvo.
- **Seleção:** Escolha dos indivíduos mais aptos para reprodução (Elitismo e Torneio/Ranking).
- **Crossover (Cruzamento):** Mistura aritmética de cores para gerar descendentes.
- **Mutação:** Introdução de ruído aleatório para exploração de novos tons e prevenção de convergência prematura.

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**
- **Pygame:** Para a interface visual e interação em tempo real.
- **Matplotlib:** Para geração do gráfico de convergência (fitness ao longo das gerações).
- **Conda:** Para gerenciamento do ambiente virtual.

## 📦 Instalação e Execução

1. Certifique-se de ter o Conda instalado.
2. Crie o ambiente a partir do arquivo `environment.yml`:
   ```bash
   conda env create -f environment.yml
   conda activate fiap_camouflage
   ```
3. Execute a simulação interativa:
   ```bash
   python run_camouflage.py
   ```

## 🎮 Como Interagir

- Observe a grade de 5x5 quadrados evoluindo para a cor de fundo.
- Use os **botões coloridos** no painel lateral para mudar a cor do ambiente em tempo real e ver a população se adaptando ao novo desafio.
- Pressione **'Q'** para sair da aplicação.

## 📄 Licença

Este projeto está licenciado sob a [CC0 1.0 Universal](LICENSE).
