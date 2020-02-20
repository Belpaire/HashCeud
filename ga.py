import numpy as np
import math as m
import numpy.random as random


def run(n_ind, gens, p_cross=0, p_mut=0):
    pop = init_pop(n_ind)
    for g in range(0, gens):
        p_fit = fitness(pop)
        rank = linrank(p_fit)
        # rank = exprank(fit)
        parent_idx = sus(rank, n_ind)
        # parent_idx = tournament(rank, n_ind)

        def get_at_index(popu, idx):
            #whatever
            return popu

        parents = get_at_index(pop, parent_idx)
        children = crossover(parents, 1)
        children = mutate(children, 1)
        c_fit = fitness(children)
        new_idx = best_n(p_fit, c_fit, n_ind)
        # new_idx = round_robin(p_fit, c_fit, n_ind, 10)
        pop = get_at_index([parents, children], new_idx)
    return pop


def init_pop(n):
    population = np.random.rand(n)
    return population


def fitness(population):
    fit = np.zeros_like(population)
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
    children = parents
    return children


def mutate(parents, prob):
    mutated = parents
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
