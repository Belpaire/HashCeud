import numpy as np
import math as m
import numpy.random as random
from Parser import read_in_file
import Book
import Library

def run(n_ind, gens, params, p_cross=0, p_mut=0):
    libs = params["libs"]
    days = params["days"]
    books = params["books"] #numpy array
    signup = params["signup"] #numpy array
    score = params["score"]
    pop = init_pop(n_ind, params)
    for g in range(0, gens):
        p_fit = fitness(pop, params)
        rank = linrank(p_fit)
        # rank = exprank(fit)
        parent_idx = sus(rank, n_ind)
        # parent_idx = tournament(rank, n_ind)
        parents = pop[parent_idx]
        children = crossover(parents, 1)
        children = mutate(children, 1)
        c_fit = fitness(children)
        new_idx = best_n(p_fit, c_fit, n_ind)
        # new_idx = round_robin(p_fit, c_fit, n_ind, 10)
        pop = np.append(parents, children)[new_idx]
    return pop


def init_pop(n, params):
    libs = params["libs"]
    days = params["days"]
    population = np.random.randint(-1, days, [n, libs])
    return population


def fitness(population, params):
    score = params["score"]
    deadline = params["days"]
    delay = params["signup"]
    books = params["books"]
    fit = np.zeros(population.shape[0])
    for i in range(0,population.shape[0]):
        schedule = population[i]
        order = np.argsort(schedule)
        prev_end = 0
        for lib in order:
            if schedule[lib] < 0:
                break
            s_penalty = 0
            b_penalty = 0
            ships = schedule[lib]+delay[lib]-deadline
            if ships < 0:
                b_penalty = ships
                ships = 0
            if schedule[lib] < prev_end:
                s_penalty = -m.pow(schedule[lib] - prev_end, 2)
            shipped = books[lib][0:ships]
            lib_score = score[shipped].sum()+b_penalty+s_penalty
            fit[i] += lib_score
            prev_end = schedule[lib]+delay[lib]
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
    if n_sel >= n_pop:
        return
    sel_idx = np.zeros(n_sel).astype(int)
    idx_list = np.linspace(0, n_pop-1, n_pop).astype(int)
    cdf = np.cumsum(ranking)
    for i in range(0, n_sel):
        r = (i + random.rand())/n_sel
        sel_idx[i] = idx_list[cdf >= r][0]
    return sel_idx


def tournament(ranking, n_sel, size):
    sel_idx = np.zeros(n_sel)
    for i in range(0, n_sel):
        drafted = random.permutation(range(0, n_sel))[0:size]
        win_idx = np.argsort(ranking[drafted])[-1]
        winner = drafted[win_idx]
        sel_idx[i] = winner
    return sel_idx


def crossover(parents, prob):
    children = np.array(parents)
    for i in range(0, parents.shape[0], 2):
        for j in range(0, parents.shape[1]):
            if random.rand() > prob:
                break
            children[i][j] = parents[i+1][j]
            children[i+1][j] = parents[i][j]
    return children


def mutate(parents, prob, max):
    mutated = np.array(parents)
    for i in range(0, parents.shape[0]):
        for j in range(0, parents.shape[1]):
            if random.rand() > prob:
                break
            toggle = 1/3
            if random.rand() > toggle:
                mutated[i][j] = random.randint(0, max)
            else:
                mutated[i][j] = -1
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
            winner = match[win_idx]
            wins[winner] += 1
    most_wins = np.argsort(wins)
    return most_wins[-1:-n-1:-1]


def data2params(data):
    params = dict()
    params["libs"] = np.array(range(0, len(data.libs)))
    params["books"] = np.zeros(len(data.libs), len(data.allbooks))
    params["days"] = data.nbdays
    params["signup"] = np.zeros_like(params["libs"]).astype(type)
    params["score"] = np.zeros(len(data.allbooks))
    for lib in data.libs:
        booklist = lib.get_best_books()
        params["signup"][lib.id] = lib.sign_time
        for i in range(0, len(booklist)):
            params["books"][lib.id][i] = booklist[i].id
    for i in range(0, len(data.allbooks)):
        params["score"][i] = data.allbooks[i].score
    return params

def main():
    data = read_in_file("input/a_example.txt")
    p = data2params(data)
    return run(50,10000,p)

main()
