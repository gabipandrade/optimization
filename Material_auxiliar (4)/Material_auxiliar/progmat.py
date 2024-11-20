import pandas as pd
import time
from mip import Model, xsum, maximize, BINARY, OptimizationStatus

# Função para ler e processar os dados dos monitores e disciplinas a partir de um arquivo Excel.
def ler_dados(path):
    def limpar_nome_coluna(nome):
        return ' '.join(nome.strip().split()).lower()

    # Leitura do arquivo Excel e padronização das colunas
    df = pd.read_excel(path)
    df.columns = [limpar_nome_coluna(col) for col in df.columns]

    print("Colunas disponíveis no arquivo Excel:", df.columns)  # Exibe as colunas do arquivo Excel

    # Verificar se a coluna 'nºusp' existe no arquivo Excel
    if 'nºusp' not in df.columns:
        raise KeyError("A coluna 'nºusp' não foi encontrada no arquivo. Verifique os nomes das colunas disponíveis.")

    # Remoção de duplicatas baseado no número USP
    df = df.drop_duplicates(subset=['nºusp'], keep='last')  # Mantém apenas a última ocorrência de um NUSP

    colunas_n = [
        'nºusp',
        'possui pedido de bolsa de estudos em andamento? (a concessão de bolsa de estudos implicará no cancelamento da monitoria a partir do início da vigência da bolsa)',
        'pretende se inscrever no peeg? (o acúmulo das duas monitorias não é permitido. caso o aluno seja selecionado nas duas modalidades precisará optar por uma delas)',
        'departamento de matemática (início da monitoria em 05/08/2024)',
        'departamento de matemática aplicada e estatística (início da monitoria em 05/08/2024)',
        'departamento de ciências de computação (início da monitoria em 05/08/2024)',
        'departamento de sistemas de computação (início da monitoria em 01/09/2024)',
        'tem interesse na monitoria voluntária (sem recebimento de bolsa)?',
        'média ponderada com reprovações'
    ]

    df_colunas = df[colunas_n].copy()

    # Calcula o status da bolsa e do PEEG
    def calcular_pontuacao(row):
        bolsa = row[colunas_n[1]]
        peeg = row[colunas_n[2]]
        if bolsa == 'Sim' and peeg == 'Sim':
            return 1
        elif bolsa == 'Não' and peeg == 'Não':
            return 3
        return 2

    df_colunas['bolsa_peeg_status'] = df_colunas.apply(calcular_pontuacao, axis=1)
    df_colunas = df_colunas.drop([colunas_n[1], colunas_n[2]], axis=1)

    # Mapeamento de disciplinas e departamentos
    departamento_mapping = {
        colunas_n[3]: 1,
        colunas_n[4]: 2,
        colunas_n[5]: 3,
        colunas_n[6]: 4
    }

    materias_set = set()
    materias_dict = {}
    materia_index = 0

    for dept_col, dept_num in departamento_mapping.items():
        for materias in df_colunas[dept_col].dropna():
            for materia in materias.split(','):
                materia = materia.strip()
                if materia not in materias_set:
                    materias_set.add(materia)
                    materias_dict[materia_index] = (materia, dept_num)
                    materia_index += 1

    # Processamento de alunos e suas informações
    alunos = df_colunas.set_index('nºusp').T.to_dict('list')
    Na = []

    for usp, valores in alunos.items():
        materias_combinadas = []
        valores_limpos = []
        for valor in valores:
            if isinstance(valor, str) and '-' in valor:
                for materia in valor.split(','):
                    materia = materia.strip()
                    for indice, (mat, dept) in materias_dict.items():
                        if materia == mat:
                            materias_combinadas.append(indice)
                            break
            elif isinstance(valor, str) and (valor.upper() == 'POS' or valor.upper() == 'PÓS'):
                valores_limpos.append(1)
            elif not pd.isna(valor):
                valores_limpos.append(valor)

        if materias_combinadas:
            valores_limpos.append(sorted(materias_combinadas))

        alunos[usp] = valores_limpos
        nota = valores_limpos[1] if len(valores_limpos) > 1 else None
        Na.append(nota)

    s_ad = [
        [1 if materia in valores_limpos[-1] else 0 for materia in materias_dict.keys()]
        for usp, valores_limpos in alunos.items()
    ]

    return alunos, Na, s_ad

# Função para criar o modelo de otimização
def criar_modelo(alunos, Na, s_ad, materias):
    A = list(range(len(alunos)))  # Conjunto de monitores
    D = list(range(len(materias)))  # Conjunto de disciplinas

    # Criação do modelo
    m = Model("Alocacao_de_Monitores", solver_name="CBC")

    # Variáveis de decisão
    x_ad = [[m.add_var(var_type=BINARY) for d in D] for a in A]  # x_ad[a][d]: 1 se monitor 'a' é alocado à disciplina 'd'
    y_d = [m.add_var(var_type=BINARY) for d in D]  # y_d[d]: 1 se disciplina 'd' não possui monitor

    # Função objetivo
    m.objective = maximize(
        xsum(Na[a] * x_ad[a][d] for a in A for d in D) - xsum(y_d[d] for d in D)
    )

    # Restrições
    for d in D:
        m += xsum(x_ad[a][d] for a in A) + y_d[d] == 1  # Cada disciplina deve ter, no máximo, um monitor ou ficar sem monitor
    for a in A:
        m += xsum(x_ad[a][d] for d in D) <= 1  # Cada monitor pode ser alocado a, no máximo, uma disciplina
    for a in A:
        for d in D:
            m += x_ad[a][d] <= s_ad[a][d]  # Monitor só pode ser alocado a disciplinas que ele indicou interesse

    return m, x_ad, y_d, D

# Função para resolver o modelo
def resolver_modelo(modelo, presolve, cortes):
    modelo.preprocess = presolve
    modelo.cuts = cortes
    modelo.optimize(max_seconds=1800)

    if modelo.status == OptimizationStatus.OPTIMAL:
        print("\nSolução ótima encontrada.")
    elif modelo.status == OptimizationStatus.FEASIBLE:
        print("\nSolução viável encontrada com gap:", modelo.gap)
    else:
        print("\nNão foi possível encontrar uma solução viável.")

    # Exibir o valor da função objetivo
    print(f"Valor da função objetivo: {modelo.objective_value:.2f}")
    return modelo

# Caminho do arquivo Excel
path = "Material_auxiliar (4)/Material_auxiliar/Dados_monitores.xlsx"

# Processar os dados
alunos, Na, s_ad = ler_dados(path)

# Criar o modelo
materias = list(range(len(s_ad[0])))
mod, x_ad, y_d, D = criar_modelo(alunos, Na, s_ad, materias)

# Resolver o modelo
m = resolver_modelo(mod, presolve=1, cortes=1)
