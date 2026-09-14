# Rota Inteligente: Otimização de Entregas com Algoritmos de IA

## 1. Descrição do Projeto

O projeto Rota Inteligente foi desenvolvido para a empresa fictícia Sabor Express, uma pequena empresa de delivery de alimentos que enfrenta dificuldades para organizar suas entregas durante períodos de alta demanda.

O objetivo é utilizar algoritmos de Inteligência Artificial para encontrar rotas mais eficientes e organizar os pontos de entrega em regiões próximas.

## 2. Objetivo

O principal objetivo do projeto é desenvolver uma solução computacional capaz de:

- Representar os locais de entrega como um grafo;
- Encontrar caminhos eficientes entre os pontos;
- Agrupar entregas próximas;
- Auxiliar na organização das rotas dos entregadores;
- Reduzir a distância percorrida nas entregas.

## 3. Representação do Problema

A cidade foi representada como um grafo.

Os pontos representam o restaurante e os locais de entrega, enquanto as conexões representam as ruas entre esses locais.

Cada conexão possui um peso relacionado à distância entre os pontos.

Os locais utilizados no projeto são:

- Restaurante
- A
- B
- C
- D
- E
- F
- G

## 4. Algoritmos Utilizados

### A*

O algoritmo A* foi utilizado para encontrar o menor caminho entre dois pontos do grafo.

O algoritmo utiliza o custo do caminho percorrido juntamente com uma função heurística baseada na distância entre o ponto atual e o destino.

### K-Means

O algoritmo K-Means foi utilizado para realizar o agrupamento dos pontos de entrega em duas zonas.

A ideia é identificar grupos de entregas próximas, facilitando a organização dos pedidos.

### Heurística para múltiplas entregas

Para lidar com vários pontos de entrega, foi utilizada uma estratégia que calcula as possíveis rotas com o algoritmo A* e seleciona a próxima entrega com menor distância entre as opções disponíveis.

## 5. Estrutura do Projeto

```text
ROTA-INTELIGENTE/
│
├── data/
│   └── entregas.csv
│
├── docs/
│   ├── mapa_grafo.png
│   └── agrupamento_kmeans.png
│
├── src/
│   └── main.py
│
└── README.md