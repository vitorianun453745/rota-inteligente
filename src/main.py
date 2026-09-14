# ============================================================
# ROTA INTELIGENTE - SABOR EXPRESS
# Projeto de Artificial Intelligence Fundamentals
# ============================================================

import heapq
import math
from pathlib import Path
import csv

PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DOCS = PASTA_PROJETO / "docs"

# ============================================================
# CARREGAMENTO DOS DADOS DE ENTREGA
# ============================================================

arquivo_entregas = PASTA_PROJETO / "data" / "entregas.csv"

entregas_csv = []

with open(arquivo_entregas, "r", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha in leitor:
        entregas_csv.append(linha["local"])

# ============================================================
# 1. MAPA DA CIDADE - REPRESENTAÇÃO COMO GRAFO
# ============================================================

grafo = {
    "Restaurante": {
        "A": 2.0,
        "B": 4.0
    },

    "A": {
        "Restaurante": 2.0,
        "C": 2.5,
        "D": 3.0
    },

    "B": {
        "Restaurante": 4.0,
        "D": 2.0,
        "E": 3.5
    },

    "C": {
        "A": 2.5,
        "D": 1.5,
        "F": 2.5
    },

    "D": {
        "A": 3.0,
        "B": 2.0,
        "C": 1.5,
        "E": 2.0,
        "F": 2.0
    },

    "E": {
        "B": 3.5,
        "D": 2.0,
        "F": 1.5,
        "G": 2.5
    },

    "F": {
        "C": 2.5,
        "D": 2.0,
        "E": 1.5,
        "G": 2.0
    },

    "G": {
        "E": 2.5,
        "F": 2.0
    }
}


# ============================================================
# 2. COORDENADAS DOS LOCAIS
# Usadas pela heurística do algoritmo A*
# ============================================================

coordenadas = {
    "Restaurante": (0, 0),
    "A": (2, 1),
    "B": (1, 3),
    "C": (4, 2),
    "D": (4, 4),
    "E": (6, 4),
    "F": (6, 2),
    "G": (8, 3)
}


# ============================================================
# 3. HEURÍSTICA
# Distância em linha reta entre dois pontos
# ============================================================

def heuristica(atual, destino):

    x1, y1 = coordenadas[atual]
    x2, y2 = coordenadas[destino]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# ============================================================
# 4. ALGORITMO A*
# Encontra o menor caminho entre dois pontos
# ============================================================

def a_estrela(inicio, destino):

    fila = []

    heapq.heappush(fila, (0, inicio))

    custos = {
        inicio: 0
    }

    caminhos = {
        inicio: None
    }

    while fila:

        _, atual = heapq.heappop(fila)

        if atual == destino:
            break

        for vizinho, distancia in grafo[atual].items():

            novo_custo = custos[atual] + distancia

            if vizinho not in custos or novo_custo < custos[vizinho]:

                custos[vizinho] = novo_custo

                prioridade = novo_custo + heuristica(vizinho, destino)

                heapq.heappush(
                    fila,
                    (prioridade, vizinho)
                )

                caminhos[vizinho] = atual

    if destino not in caminhos:
        return [], float("inf")

    caminho = []
    atual = destino

    while atual is not None:

        caminho.append(atual)
        atual = caminhos[atual]

    caminho.reverse()

    return caminho, custos[destino]


# ============================================================
# 5. K-MEANS
# Agrupamento das entregas em regiões próximas
# ============================================================

def distancia(ponto1, ponto2):

    x1, y1 = ponto1
    x2, y2 = ponto2

    return math.sqrt(
        (x1 - x2) ** 2 +
        (y1 - y2) ** 2
    )


def kmeans(pontos, k=2, iteracoes=10):

    centroides = pontos[:k]

    for _ in range(iteracoes):

        grupos = [[] for _ in range(k)]

        # Associar cada ponto ao centroide mais próximo
        for ponto in pontos:

            distancias = [
                distancia(ponto, centroide)
                for centroide in centroides
            ]

            grupo = distancias.index(min(distancias))

            grupos[grupo].append(ponto)

        novos_centroides = []

        for grupo in grupos:

            if grupo:

                x = sum(p[0] for p in grupo) / len(grupo)
                y = sum(p[1] for p in grupo) / len(grupo)

                novos_centroides.append((x, y))

            else:

                novos_centroides.append(
                    centroides[len(novos_centroides)]
                )

        if novos_centroides == centroides:
            break

        centroides = novos_centroides

    return grupos, centroides


# ============================================================
# 6. EXECUÇÃO DO SISTEMA
# ============================================================

print("=" * 60)
print("              SABOR EXPRESS")
print("              ROTA INTELIGENTE")
print("=" * 60)

print("\nSistema de otimização de entregas iniciado!")


# ============================================================
# 7. ENTREGAS
# ============================================================

entregas = entregas_csv

print("\nPontos de entrega:")

for entrega in entregas:
    print(f"- {entrega}")


# ============================================================
# 8. TESTE DO ALGORITMO A*
# ============================================================

print("\n" + "=" * 60)
print("TESTE DO ALGORITMO A*")
print("=" * 60)

origem = "Restaurante"
destino = "G"

caminho, distancia_total = a_estrela(
    origem,
    destino
)

print(f"\nOrigem: {origem}")
print(f"Destino: {destino}")

print("\nMelhor rota encontrada:")

print(" -> ".join(caminho))

print(f"\nDistância total: {distancia_total:.2f} km")


# ============================================================
# 9. K-MEANS PARA AGRUPAR AS ENTREGAS
# ============================================================

print("\n" + "=" * 60)
print("AGRUPAMENTO DAS ENTREGAS COM K-MEANS")
print("=" * 60)

pontos_entrega = [
    coordenadas[ponto]
    for ponto in entregas
]

grupos, centroides = kmeans(
    pontos_entrega,
    k=2
)

for numero, grupo in enumerate(grupos, start=1):

    print(f"\nZona de entrega {numero}:")

    for ponto in grupo:

        local = next(
            nome
            for nome, coordenada in coordenadas.items()
            if coordenada == ponto
        )

        print(f"- {local}")


# ============================================================
# 10. FINALIZAÇÃO
# ============================================================

print("\n" + "=" * 60)
print("PROCESSAMENTO CONCLUÍDO")
print("=" * 60)

print("\nA solução utilizou:")
print("- Representação de cidade como grafo")
print("- Algoritmo A* para busca de rotas")
print("- K-Means para agrupamento de entregas")

# ============================================================
# 11. GERAÇÃO DO MAPA VISUAL DO GRAFO
# ============================================================

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 7))

# Desenhar as ruas (arestas)
for origem, vizinhos in grafo.items():

    x1, y1 = coordenadas[origem]

    for destino in vizinhos:

        x2, y2 = coordenadas[destino]

        plt.plot(
            [x1, x2],
            [y1, y2],
            linewidth=1
        )

# Desenhar os pontos da cidade
for local, (x, y) in coordenadas.items():

    plt.scatter(x, y, s=150)

    plt.text(
        x,
        y + 0.2,
        local,
        ha="center"
    )

# Destacar a rota encontrada
if caminho:

    for i in range(len(caminho) - 1):

        origem = caminho[i]
        destino = caminho[i + 1]

        x1, y1 = coordenadas[origem]
        x2, y2 = coordenadas[destino]

        plt.plot(
            [x1, x2],
            [y1, y2],
            linewidth=4
        )

plt.title("Mapa de Rotas - Sabor Express")

plt.xlabel("Posição X")
plt.ylabel("Posição Y")

plt.grid(True)

plt.tight_layout()

plt.savefig(PASTA_DOCS / "mapa_grafo.png", dpi=300)

plt.show()

# ============================================================
# 12. GRÁFICO DO AGRUPAMENTO K-MEANS
# ============================================================

plt.figure(figsize=(10, 7))

# Mostrar cada grupo de entregas
for numero, grupo in enumerate(grupos, start=1):

    if not grupo:
        continue

    x = [ponto[0] for ponto in grupo]
    y = [ponto[1] for ponto in grupo]

    plt.scatter(
        x,
        y,
        s=180,
        label=f"Zona {numero}"
    )

# Mostrar os centroides
for numero, centroide in enumerate(centroides, start=1):

    x, y = centroide

    plt.scatter(
        x,
        y,
        marker="X",
        s=250
    )

    plt.text(
        x,
        y + 0.2,
        f"Centroide {numero}",
        ha="center"
    )

# Identificar os locais
for local in entregas:

    x, y = coordenadas[local]

    plt.text(
        x,
        y - 0.25,
        local,
        ha="center"
    )

plt.title("Agrupamento de Entregas - K-Means")

plt.xlabel("Posição X")
plt.ylabel("Posição Y")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(PASTA_DOCS / "agrupamento_kmeans.png", dpi=300)

plt.show()

# ============================================================
# 13. ROTA OTIMIZADA PARA MÚLTIPLAS ENTREGAS
# ============================================================

def rota_multiplas_entregas(inicio, entregas):

    atual = inicio
    entregas_restantes = entregas.copy()

    rota_completa = [inicio]
    distancia_total = 0

    while entregas_restantes:

        melhor_destino = None
        melhor_caminho = None
        menor_distancia = float("inf")

        # Testar qual entrega restante está mais próxima
        for destino in entregas_restantes:

            caminho, distancia = a_estrela(
                atual,
                destino
            )

            if distancia < menor_distancia:

                menor_distancia = distancia
                melhor_destino = destino
                melhor_caminho = caminho

        # Adicionar o caminho escolhido à rota
        if melhor_caminho:

            rota_completa.extend(
                melhor_caminho[1:]
            )

            distancia_total += menor_distancia

        atual = melhor_destino

        entregas_restantes.remove(
            melhor_destino
        )

    return rota_completa, distancia_total


# ============================================================
# 14. EXECUÇÃO DA ROTA COM MÚLTIPLAS ENTREGAS
# ============================================================

print("\n" + "=" * 60)
print("ROTA OTIMIZADA PARA MÚLTIPLAS ENTREGAS")
print("=" * 60)

rota_entregas, distancia_entregas = rota_multiplas_entregas(
    "Restaurante",
    entregas
)

print("\nSequência da rota:")

print(" -> ".join(rota_entregas))

print(
    f"\nDistância total percorrida: "
    f"{distancia_entregas:.2f} km"
)

print(
    f"Quantidade de locais visitados: "
    f"{len(set(rota_entregas))}"
)

print("\nRota calculada com sucesso!")