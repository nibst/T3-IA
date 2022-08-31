from audioop import cross
from cProfile import label
import random
import matplotlib.pyplot as plt

def evaluate(individual):
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 9.

    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """
    """
    Dicionario de ataques. Cada key é a coluna da peça em questão (em nosso caso terão keys de 1 a 8).
    Cada valor desse dicionário será uma lista com numeros, esses numeros são as colunas que a peça de key=x ataca

    {1: [1,2,3]} -> significa que a peça que está na coluna 1 ataca peças nas colunas 1 2 e 3
    """
    attack_dict = {}

    for column,pos in enumerate(individual):
        attack_dict[column+1] = get_columns_attacked(column+1,pos,individual)#column+1 porque daí colunas e posicoes ficam no msm padrao de 1-8

    #para contabilizar ataques, tirar ataques feitos a colunas que ja tiveram seus ataques contabilizados
    #EX: estou vendo o attack_dict da coluna 3 (apos ter visto a 1 e 2) e ela ataca [1,2,4,6], portanto remover o 1 e 2 da contabilizacao
    num_attacks = 0
    checked_columns = []
    for column in attack_dict.keys():
        for column_attacked in attack_dict[column]:
            if column_attacked not in checked_columns:
                num_attacks+=1
        checked_columns.append(column)
    return num_attacks

def get_columns_attacked(my_column, my_pos,individual):
    
    #direcoes ortogonais e diagonais
    directions_operations = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]] # um passo na direcao [coluna,posicao]
    columns_attacked = []
    my_cell  = [my_column,my_pos]
    for direction in directions_operations:
        checked_cell = [my_cell[0] + direction[0], my_cell[1] + direction[1]]
        while is_in_bounds(checked_cell):
            #se o individuo tem uma peca na coluna coluna checked_cell[1] e na linha checked_cell[0]
            #então tem ataque diagonal
            if individual[checked_cell[0]-1] == checked_cell[1]: #-1 pq minha coluna vai de 1-8, mas o acesso eh feito de 0-7
                columns_attacked.append(checked_cell[0])
            checked_cell = [checked_cell[0] + direction[0], checked_cell[1] + direction[1]]
    return columns_attacked        

     
        
def is_in_bounds(cell):
    for coordinate in cell:
        if coordinate > 8 or coordinate < 1:
            return False
    return True

def selection(k,population):
    parents = [None,None]
    for i in range(2):
        participants = random.choices(population=population,k=k)    
        parents[i] = tournament(participants)
    return parents[0],parents[1]

def tournament(participants):
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """
    top_participant = top(1,participants)            
    return top_participant[0]

def crossover(parent1, parent2, index):
    """
    Realiza o crossover de um ponto: recebe dois indivíduos e o ponto de
    cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
    dois indivíduos com o material genético trocado.
    Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
    deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
    A ordem dos dois indivíduos retornados não é importante
    (o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
    :param parent1:list
    :param parent2:list
    :param index:int
    :return:list,list
    """        
    #talvez fazer em um loop só dps, mas por enquanto ta bom
    cutPoint = index
    parent = parent1
    offspring1 = []
    for i in range(len(parent)):
        if i == cutPoint:
            parent = parent2 #swap from which parent take genes
        offspring1.append(parent[i])
        
    parent = parent2
    offspring2 = []
    for i in range(len(parent)):
        if i == cutPoint:
            parent = parent1 #swap from which parent take genes
        offspring2.append(parent[i])
   
    return offspring1,offspring2

def mutate(individual, m):
    """
    Recebe um indivíduo e a probabilidade de mutação (m).
    Caso random() < m, sorteia uma posição aleatória do indivíduo e
    coloca nela um número aleatório entre 1 e 8 (inclusive).
    :param individual:list
    :param m:int - probabilidade de mutacao
    :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
    """
    domain  = [1,2,3,4,5,6,7,8]
    if random.random() < m:
        geneToMutate = random.randint(0,len(individual)-1)
        gene = individual[geneToMutate]
        domain.remove(gene) #remove current gene value from the choices
        mutation = random.choice(domain)
        individual[geneToMutate] = mutation
    return individual
    


def run_ga(g, n, k, m, e):
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:bool - se vai haver elitismo
    :return:list - melhor individuo encontrado
    """
    """
        P<-aleatorios(n)
        repetir g vezes:
            se houver elitismo:
                P' <- top(k,P)
            senao:
                P' <-  Vazio
            enquanto tam(P')<n:
                pai1,pai2 <- selecao(P)
                o1,o2 <- crossover(pai1,pai2)
                o1 <- mutation(o1)
                o2 <- mutation(o2)
                P' <- P'  U {o1,o2}
        P <- P'
        retornar top(x,P,f) #top x individuos de P
    """
    max_conflicts = []
    min_conflicts = []
    avg_conflicts = []
    population = random_sample(n)
    for i in range(g):
        if e:
            new_population = top(e,population)
        else:
            new_population = []
        while len(new_population) < n:
            parent1,parent2 = selection(k,population)
            offspring1,offspring2 = crossover(parent1,parent2,3)
            offspring1 = mutate(offspring1,m)
            offspring2 = mutate(offspring2,m)
            new_population.append(offspring1)
            new_population.append(offspring2)
        population = new_population
        evaluations = [evaluate(individual) for individual in population]
        max_conflicts.append(max(evaluations)) 
        min_conflicts.append(min(evaluations))
        avg_conflicts.append(sum(evaluations) / len(evaluations))
    plot(max_conflicts,min_conflicts,avg_conflicts)
    return top(1,population)

def plot(max_conflicts,min_conflicts,avg_conflicts):
    plt.figure(figsize=(6, 2))
    plt.plot(max_conflicts,label='max conflicts')
    plt.plot(avg_conflicts,label='avg conflicts')
    plt.plot(min_conflicts,label='min conflicts')
    plt.xlabel('generations')
    plt.ylabel('fitness score')
    plt.title('Genetic run')
    plt.legend()

    #plt.legend(['Max Conflicts', line1, 'Avg Confclits', line2, 'Min Conflicts', line3])
    plt.show()
    

def top(k,population):
    """
    get top k individuals of population
    """
    top_individuals = [] #top k individuals
    for count,individual in enumerate(population):
        top_individuals.append(individual) 
        if count >= k:
            remove_worst_solution(top_individuals)
    return top_individuals

def remove_worst_solution(top_individuals):
    
    worst = float('-inf') #maior numero é pior
    for index,individual in enumerate(top_individuals):
        num_attakcs = evaluate(individual)
        if num_attakcs > worst:
            worst = num_attakcs
            worst_individual_index = index
    top_individuals.pop(worst_individual_index)

def random_sample(n):
    sample = []
    for i in range(n):
        one_individual = generate_random_individual()
        sample.append(one_individual)
    
    return sample

def generate_random_individual():
    domain =  [1,2,3,4,5,6,7,8]
    individual = []
    for i in range(len(domain)):
        individual.append(random.choice(domain))
    return individual  

