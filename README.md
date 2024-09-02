# Projeto de IA: Connect 4

Este repositório contém o código fonte para o projeto de Inteligência Artificial, onde são implementados agentes para jogar o jogo Connect 4. O projeto envolve dois agentes: um usando a técnica Minimax e outro usando Q-learning, competindo entre si em um ambiente simulado.

## Descrição

O objetivo deste projeto é comparar o desempenho de dois agentes de IA no jogo Connect 4:
- **Agente Minimax**: Implementa o algoritmo Minimax para decidir a melhor jogada, considerando uma profundidade de pesquisa definida.
- **Agente Q-learning**: Utiliza aprendizado por reforço para aprender a política ótima ao longo de múltiplas partidas simuladas.
- **Agente Aleatório**: Seleciona uma jogada válida aleatória.

## Estrutura do Projeto

- game.py : Contém classes do connect4 e agentes
- main.py : Funções para treinar e testar o agente Q-Learning
- util.py : Licenciado e disponibilizado por UC Berkeley (http://ai.berkeley.edu )
