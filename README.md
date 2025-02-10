# Otimização - Alocação de Alunos Monitores

---

## Resumo

Com o auxílio do template em Python disponibilizado, foi implementado um modelo para a alocação de monitores às disciplinas, visando maximizar as médias ponderadas dos monitores e minimizar as disciplinas sem monitores. Diversos testes computacionais foram realizados para avaliar o desempenho do modelo em diferentes situações. Todo o trabalho foi realizado pela única integrante do grupo.

---

## 1. Descrição do Problema

O problema consiste em alocar monitores às disciplinas de forma otimizada, maximizando a soma ponderada das médias dos monitores e minimizando as disciplinas não atendidas. O modelo matemático é composto por uma função objetivo e restrições que garantem alocações compatíveis e justas. Foram utilizados dados sobre as preferências e qualificações dos monitores, e o solver CBC foi aplicado para resolver as instâncias geradas.

---

## 2. Resultados Obtidos

### 2.1 Teste Computacional 1

- **Função Objetivo:** 478,3
- **Disciplinas sem monitor:** 4
- **Tempo de execução:** 0,25 segundos

> **Observação:** Bom desempenho do modelo para a resolução do problema.

### 2.2 Teste Computacional 2

- **Observação:**  
  Identificar monitores que já cursaram as disciplinas, mesmo sem estarem inscritos, e que possuem boas médias pode ser útil. Recomenda-se entrar em contato com esses alunos para incentivá-los a se inscreverem, melhorando assim a alocação.

### 2.3 Teste Computacional 3

- **Função Objetivo:** 458,9 (com alocação arbitrária de 5 alunos)
- **Disciplinas sem monitor:** 5

> **Conclusão:** A alocação sem critérios objetivos resulta em desempenho inferior.

### 2.4 Teste Computacional 4

Utilizando a função `aumentar_dados`, foram geradas 5 instâncias com fatores de escala 2, 3, 5, 10 e 15. A seguir, os resultados:

**Tabela 1: Resultados para instâncias com diferentes fatores de escala**

| Instância | Melhor Solução | % Gap | Tempo de Execução (s) |
|-----------|----------------|-------|-----------------------|
| 1         | 852,33         | 0,00  | 0,44                  |
| 2         | 1353,16        | 0,00  | 0,88                  |
| 3         | 2287,99        | 0,00  | 2,64                  |
| 4         | 4623,08        | 0,00  | 10,60                 |
| 5         | 6601,22        | 0,00  | 45,78                 |

> **Conclusão:** O aumento dos dados gera maior valor na função objetivo devido ao maior número de alunos alocados, mas também eleva o tempo de execução.

### 2.5 Teste Computacional 5

Ao desativar a opção `cuts`, foram observados tempos de execução maiores em instâncias grandes, embora o valor da solução permanecesse o mesmo.

**Tabela 2: Resultados para instâncias com cortes desativados**

| Instância | Melhor Solução | % Gap | Tempo de Execução (s) |
|-----------|----------------|-------|-----------------------|
| 1         | 852,33         | 0,00  | 0,41                  |
| 2         | 1353,16        | 0,00  | 0,87                  |
| 3         | 2287,99        | 0,00  | 2,29                  |
| 4         | 4623,08        | 0,00  | 8,47                  |
| 5         | 6601,22        | 0,00  | 107,29                |

> **Recomendação:** Utilizar a opção `cuts` em instâncias grandes para manter o desempenho.

### 2.6 Teste Computacional 6

Ao desativar a opção `presolve`, o tempo de execução aumentou significativamente.

**Tabela 3: Resultados para instâncias com presolve desativado**

| Instância | Melhor Solução | % Gap | Tempo de Execução (s) |
|-----------|----------------|-------|-----------------------|
| 1         | 852,33         | 0,00  | 1,19                  |
| 2         | 1353,16        | 0,00  | 2,50                  |
| 3         | 2287,99        | 0,00  | 6,25                  |
| 4         | 4623,08        | 0,00  | 24,10                 |
| 5         | 6601,22        | 0,00  | 96,55                 |

> **Conclusão:** A ativação do `presolve` é crucial para evitar aumentos drásticos no tempo de execução.

### 2.7 Teste Computacional 7

Alterando a função objetivo para incluir as prioridades dos alunos (utilizando o método Big M), foram obtidos resultados ligeiramente diferentes. Essa modificação priorizou alunos com maior afinidade pelas disciplinas.

**Tabela 4: Resultados com inclusão de prioridades dos alunos**

| Instância | Melhor Solução | % Gap | Tempo de Execução (s) |
|-----------|----------------|-------|-----------------------|
| 1         | 852,56         | 0,00  | 0,42                  |
| 2         | 1353,48        | 0,00  | 1,12                  |
| 3         | 2288,45        | 0,00  | 2,57                  |
| 4         | 4623,90        | 0,00  | 9,26                  |
| 5         | 6602,39        | 0,00  | 94,94                 |

> **Conclusão:** A inclusão de prioridades não afetou negativamente o desempenho, permitindo uma melhor adequação às preferências dos alunos.

---

## 3. Conclusão

O modelo implementado demonstrou eficiência em otimizar a alocação de monitores, principalmente em instâncias menores. Testes realizados sem certas opções computacionais (como `presolve` e `cuts`) revelaram que, apesar de manterem soluções otimizadas, os tempos de execução aumentam consideravelmente. A inclusão de prioridades na função objetivo resultou em alocações mais alinhadas às preferências dos monitores, evidenciando que tais modificações podem melhorar a satisfação dos alunos sem prejudicar o desempenho geral do modelo. O modelo se mostrou adequado para ser utilizado como ferramenta de gestão em universidades.

---

## Créditos

Este projeto foi desenvolvido com base no template e nas orientações fornecidas pelo monitor da disciplina. Agradeço imensamente ao monitor pelo suporte e pelas contribuições fundamentais que possibilitaram a realização deste trabalho.

---
