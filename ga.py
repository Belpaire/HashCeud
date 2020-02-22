import numpy as np
import math as m
import numpy.random as random
import Parser
from tqdm import tqdm


def init_pop(n, params):
    libs = params["libs"]
    population = np.zeros((n, libs.size)).astype(int)
    for i in range(0, n):
        population[i, :] = np.random.permutation(libs.size)
    return population


def fitness(population, params):
    # return np.zeros(population.shape[0])
    score = params["score"]
    deadline = params["days"]
    delay = params["signup"]
    books = params["books"]
    per_day = params["ships"]
    fit = np.zeros(population.shape[0])
    lib_score = np.zeros(population.shape[1])
    for i in range(0, population.shape[0]):
        day = 0
        for lib in population[i]:
            day += delay[lib]
            ships = min((deadline - day)*per_day[lib], len(books[lib]))
            if ships <= 0:
                break
            lib_score[lib] = params["cumscore"][lib][ships-1]
        fit[i] = lib_score.sum()
        lib_score.fill(0)
    return fit



def linrank(fit, s=1.5):
    if s > 2:
        s = 2
    elif s < 1:
        s = 1
    n = fit.size
    indices = np.argsort(fit)
    rank = np.zeros_like(fit)
    for i in range(0, n):
        idx = indices[i]
        rank[idx] = (2-s)/n + 2*i*(s-1)/(n*(n-1))
    return rank


def exprank(fit):
    n = fit.size
    indices = np.argsort(fit)
    rank = np.zeros_like(fit)
    for i in range(0, n):
        idx = indices[i]
        rank[idx] = (1-m.exp(-i))
    rank = rank/rank.sum()
    return rank


def sus(ranking, n_sel):
    n_pop = ranking.size
    if n_sel > n_pop:
        return
    sel_idx = np.zeros(n_sel).astype(int)
    idx_list = np.linspace(0, n_pop-1, n_pop).astype(int)
    cdf = np.cumsum(ranking)
    for i in range(0, n_sel):
        r = (i + random.rand())/n_sel
        sel_idx[i] = idx_list[cdf >= r][0]
    np.random.shuffle(sel_idx)
    return sel_idx


def tournament(ranking, n_sel, size=3):
    sel_idx = np.zeros(n_sel).astype(int)
    n_ind = ranking.size
    for i in range(0, n_sel):
        drafted = random.permutation(range(0, n_ind))[0:size]
        cdf = np.cumsum(ranking[drafted])/ranking[drafted].sum()
        r = random.rand()
        sel_idx[i] = drafted[cdf >= r][0]
    return sel_idx


def crossover(parents, prob):
    children = np.array(parents)
    for i in range(0, parents.shape[0]-1, 2):
        if random.rand() > prob:
            break
        child1 = children[i]
        child2 = children[i+1]
        parent1 = parents[i]
        parent2 = parents[i+1]
        sz = parents.shape[1]
        r1 = random.randint(0, sz)
        r2 = random.randint(0, sz)
        p1 = min(r1, r2)
        p2 = max(r1, r2)
        ic = (p2+1) % sz
        ip = (p2+1) % sz
        while ic != p1:
            if child1[p1:p2+1].__contains__(parent2[ip]):
                ip = (ip+1) % sz
            else:
                child1[ic] = parent2[ip]
                ic = (ic+1) % sz
                ip = (ip+1) % sz
        ic = (p2+1) % sz
        ip = (p2+1) % sz
        while ic != p1:
            if child2[p1:p2+1].__contains__(parent1[ip]):
                ip = (ip+1) % sz
            else:
                child2[ic] = parent1[ip]
                ic = (ic+1) % sz
                ip = (ip+1) % sz
    return children


def mutate(parents, prob):
    mutated = np.array(parents)
    for i in range(0, parents.shape[0]):
        if random.rand() > prob:
            break
        r1 = random.randint(0, parents.shape[1])
        r2 = random.randint(0, parents.shape[1])
        p1 = min(r1, r2)
        p2 = max(r1, r2)
        np.random.shuffle(mutated[i][p1:p2+1])
    return mutated


def best_n(p_fit, c_fit, n):
    total = np.append(p_fit, c_fit)
    indices = np.argsort(total)
    return indices[-1:-n-1:-1]


def round_robin(p_fit, c_fit, n, q):
    if q < 2:
        q = 2
    elif q > (len(p_fit) + len(c_fit)):
        q = (len(p_fit) + len(c_fit))
    total = np.append(p_fit, c_fit)
    drafts = np.zeros_like(total).astype(int)
    wins = np.zeros_like(total).astype(int)
    for i in range(0, total.size):
        matches = q-drafts[i]
        for j in range(0, matches):
            opponent = random.randint(0, total.size)
            while opponent == i:
                opponent = random.randint(0, total.size)
            match = [i, opponent]
            drafts[match] += 1
            win_idx = np.argmax(total[match])
            winner = match[int(win_idx)]
            wins[winner] += 1
    most_wins = np.argsort(wins)
    return most_wins[-1:-n-1:-1]


def local_opt(pop, data, size):
    opt = np.array(pop)
    n = 5
    jmax = min(len(pop)-1, n*size)
    for i in range(0, len(pop)):
        for j in range(0, jmax, size):
            selected = pop[i][j:j+size]
            sort_idx = np.argsort(data["signup"][selected])
            opt[i][j:j+size] = opt[i][sort_idx]
            fit = fitness(np.array([pop[i], opt[i]]), data)
            if fit[1] > fit[0]:
                pop[i] = opt[i]


def run(n_ind, gens, params, p_cross=0., p_mut=0., elitism=0.1, pop=None):
    n_child = m.floor(n_ind*(1-elitism))
    if pop is None:
        pop = init_pop(n_ind, params)
    p_fit = np.zeros(n_ind)
    c_fit = np.zeros(n_child)
    for g in tqdm(range(0, gens)):
        p_fit = fitness(pop, params)
        if g % 50 == 0:
            print(p_fit[np.argsort(p_fit)[-1]])
        rank = linrank(p_fit, 1.2)
        # rank = exprank(p_fit)
        # parent_idx = sus(rank, n_child)
        parent_idx = tournament(rank, n_child)
        parents = pop[parent_idx, :]
        children = crossover(parents, p_cross)
        children = mutate(children, p_mut)
        c_fit = fitness(children, params)
        new_idx = best_n(p_fit, c_fit, n_ind)
        # new_idx = round_robin(p_fit, c_fit, n_ind, 10)
        pop = np.append(pop, children)
        pop = pop.reshape(n_ind+n_child, parents.shape[1])[new_idx, :]
        local_opt(pop, params, pop.size//20)
    return pop


def main():
    ex = "f_libraries_of_the_world.txt"
    data = Parser.read_in_file2("input/"+ex)
    # best = d_opt(data)
    # print(fitness(np.array([best]), data))
    pop = None
    gens = 10
    con = "Y"
    while con.upper() == "Y":
        pop = run(50, gens, data, p_cross=0.5, p_mut=0.9, elitism=0.1, pop=pop)
        con = input("continue? Y/N\n")
        if con.upper() == "Y":
            gens = int(input("Number of generations: "))
    best = pop[fitness(pop, data).argsort()[-1]]
    print([best, fitness(np.array([best]), data)])
    Parser.write_output_file2("output/"+ex, best, data)


def b_opt(data):
    sort_idx = data["signup"].argsort()
    return data["libs"][sort_idx]


def d_opt(data):
    a = np.zeros(data["libs"].size).astype(int)
    for lib in data["libs"]:
        a[lib] = data["cumscore"][lib][-1]
    sort_idx = np.argsort(a)
    return data["libs"][sort_idx]

main()