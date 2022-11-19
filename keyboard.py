#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Evolve a better keyboard.
This assignment is mostly open-ended,
with a couple restrictions:

# DO NOT MODIFY >>>>
Do not edit the sections between these marks below.
# <<<< DO NOT MODIFY
"""

# %%
import random
from typing import TypedDict
import math
import json
import string

# DO NOT MODIFY >>>>
# First, what should our representation look like?
# Is there any modularity in adjacency?
# What mechanisms capitalize on such modular patterns?
# ./corpus/2_count.py specificies this same structure
# Positions    01234   56789   01234
LEFT_DVORAK = "',.PY" "AOEUI" ";QJKX"
LEFT_QWERTY = "QWERT" "ASDFG" "ZXCVB"
LEFT_COLEMK = "QWFPG" "ARSTD" "ZXCVB"
LEFT_WORKMN = "QDRWB" "ASHTG" "ZXMCV"

LEFT_DISTAN = "11111" "00001" "11111"
LEFT_ERGONO = "00001" "00001" "11212"
LEFT_EDGE_B = "01234" "01234" "01234"

# Positions     56   7890123   456789   01234
RIGHT_DVORAK = "[]" "FGCRL/=" "DHTNS-" "BMWVZ"
RIGHT_QWERTY = "-=" "YUIOP[]" "HJKL;'" "NM,./"
RIGHT_COLEMK = "-=" "JLUY;[]" "HNEIO'" "KM,./"
RIGHT_WOKRMN = "-=" "JFUP;[]" "YNEOI'" "KL,./"

RIGHT_DISTAN = "23" "1111112" "100000" "11111"
RIGHT_ERGONO = "22" "2000023" "100001" "10111"
RIGHT_EDGE_B = "10" "6543210" "543210" "43210"

DVORAK = LEFT_DVORAK + RIGHT_DVORAK
QWERTY = LEFT_QWERTY + RIGHT_QWERTY
COLEMAK = LEFT_COLEMK + RIGHT_COLEMK
WORKMAN = LEFT_WORKMN + RIGHT_WOKRMN

DISTANCE = LEFT_DISTAN + RIGHT_DISTAN
ERGONOMICS = LEFT_ERGONO + RIGHT_ERGONO
PREFER_EDGES = LEFT_EDGE_B + RIGHT_EDGE_B

# Real data on w.p.m. for each letter, normalized.
# Higher values is better (higher w.p.m.)
with open(file="typing_data/manual-typing-data_qwerty.json", mode="r") as f:
    data_qwerty = json.load(fp=f)
with open(file="typing_data/manual-typing-data_dvorak.json", mode="r") as f:
    data_dvorak = json.load(fp=f)
data_values = list(data_qwerty.values()) + list(data_dvorak.values())
mean_value = sum(data_values) / len(data_values)
data_combine = []
for dv, qw in zip(DVORAK, QWERTY):
    if dv in data_dvorak.keys() and qw in data_qwerty.keys():
        data_combine.append((data_dvorak[dv] + data_qwerty[qw]) / 2)
    if dv in data_dvorak.keys() and qw not in data_qwerty.keys():
        data_combine.append(data_dvorak[dv])
    if dv not in data_dvorak.keys() and qw in data_qwerty.keys():
        data_combine.append(data_qwerty[qw])
    else:
        # Fill missing data with the mean
        data_combine.append(mean_value)


class Individual(TypedDict):
    genome: str
    fitness: int


Population = list[Individual]


def print_keyboard(individual: Individual) -> None:
    layout = individual["genome"]
    fitness = individual["fitness"]
    """Prints the keyboard in a nice way"""
    print("______________  ________________")
    print(" ` 1 2 3 4 5 6  7 8 9 0 " + " ".join(layout[15:17]) + " Back")
    print("Tab " + " ".join(layout[0:5]) + "  " + " ".join(layout[17:24]) + " \\")
    print("Caps " + " ".join(layout[5:10]) + "  " + " ".join(layout[24:30]) + " Enter")
    print(
        "Shift " + " ".join(layout[10:15]) + "  " + " ".join(layout[30:35]) + " Shift"
    )
    print(f"\nAbove keyboard has fitness of: {fitness}")


# <<<< DO NOT MODIFY


def initialize_individual(genome: str, fitness: int) -> Individual:
    """
    Purpose:        Create one individual
    Parameters:     genome as string, fitness as integer (higher better)
    User Input:     no
    Prints:         no
    Returns:        One Individual, as a dict[str, int]
    Modifies:       Nothing
    Calls:          ?
    Example doctest:
    """
    return Individual({"genome": genome, "fitness": fitness})


def initialize_pop(example_genome: str, pop_size: int) -> Population:
    """
    Purpose:        Create population to evolve
    Parameters:     Goal string, population size as int
    User Input:     no
    Prints:         no
    Returns:        a population, as a list of Individuals
    Modifies:       Nothing
    Calls:          ?
    Example doctest:
    """
    population = []
    for i in range(pop_size):
        new_genome_list = list(example_genome)
        random.shuffle(new_genome_list)
        new_genome = "".join(new_genome_list)
        new_individual = initialize_individual(new_genome, 0)
        population.append(new_individual)
    return population


def recombine_pair(parent1: Individual, parent2: Individual) -> Population:
    """
    Purpose:        Recombine two parents to produce two children
    Parameters:     Two parents as Individuals
    User Input:     no
    Prints:         no
    Returns:        A population of size 2, the children
    Modifies:       Nothing
    Calls:          ?
    Example doctest:
    """
    # print("Delete this and write")
    random_numbers = []
    for i in {1, 2}:
        random_numbers.append(random.choice(range(len(parent1["genome"]) - 1)))
    # print(random_numbers)
    position1 = min(random_numbers)
    position2 = max(random_numbers) + 1
    child1 = [""] * len(parent1["genome"])
    child2 = [""] * len(parent2["genome"])

    child1[position1:position2:1] = parent1["genome"][position1:position2]
    child2[position1:position2:1] = parent2["genome"][position1:position2]
    # print(child1)

    for i in range(position1, position2):
        while parent2["genome"][i] not in child1:
            k = parent2["genome"][i]
            loc = parent2["genome"].index(parent1["genome"][i])
            if child1[loc] == "":
                child1[loc] = k
            else:
                j = parent2["genome"].index(child1[loc])
                while (position1 <= j and j <= position2) and child1[j] != "":
                    j = parent2["genome"].index(child1[j])
                child1[j] = k

        while parent1["genome"][i] not in child2:
            k = parent1["genome"][i]
            loc = parent1["genome"].index(parent2["genome"][i])
            if child2[loc] == "":
                child2[loc] = k
            else:
                j = parent1["genome"].index(child2[loc])
                while (position1 <= j and j <= position2) and child2[j] != "":
                    j = parent1["genome"].index(child2[j])
                child2[j] = k

    while "" in child1:
        child1[child1.index("")] = parent2["genome"][child1.index("")]

    while "" in child2:
        child2[child2.index("")] = parent1["genome"][child2.index("")]
    """
    if len(set(child1)) == len(child1):
        print("set 1")
    else:
        print("has duplicates 1")

    if len(set(child2)) == len(child2):
        print("set 2")
    else:
        print("has duplicates 2")
    """
    offspring1 = "".join(child1)
    offspring2 = "".join(child2)
    return list(
        (initialize_individual(offspring1, 0), initialize_individual(offspring2, 0))
    )


def recombine_group(parents: Population, recombine_rate: float) -> Population:
    """
    Purpose:        Recombines a whole group, returns the new population
                    Pair parents 1-2, 2-3, 3-4, etc..
                    Recombine at rate, else clone the parents.
    Parameters:     parents and recombine rate
    User Input:     no
    Prints:         no
    Returns:        New population of children
    Modifies:       Nothing
    Calls:          ?
    """
    recombined_population = []
    for i in range(0, len(parents) - 1, 2):

        if recombine_rate > random.random():
            recombined_population.extend(recombine_pair(parents[i], parents[i + 1]))
        else:
            recombined_population.append(parents[i])
            recombined_population.append(parents[i + 1])
    return recombined_population


def mutate_individual(parent: Individual, mutate_rate: float) -> Individual:
    """
    Purpose:        Mutate one individual
    Parameters:     One parents as Individual, mutation rate as float (0-1)
    User Input:     no
    Prints:         no
    Returns:        One Individual, as a TypedDict[str, int]
    Modifies:       Nothing
    Calls:          ?
    Example doctest:
    """
    mutated_genome = ""
    genome_list = list(parent["genome"])
    genome_size = len(parent["genome"])
    for i in parent["genome"]:
        if random.random() < mutate_rate:
            position_1 = random.choice(range(genome_size))
            position_2 = random.choice(range(genome_size))
            if position_1 != position_2:
                temp = genome_list[position_1]
                genome_list[position_1] = genome_list[position_2]
                genome_list[position_2] = temp
            else:
                continue
        else:
            continue
    mutated_genome = "".join(genome_list)
    return initialize_individual(mutated_genome, 0)


def mutate_group(children: Population, mutate_rate: float) -> Population:
    """
    Purpose:        Mutates a whole Population, returns the mutated group
    Parameters:     Population, mutation rate as float (0-1)
    User Input:     no
    Prints:         no
    Returns:        One Individual, as a TypedDict[str, int]
    Modifies:       Nothing
    Calls:          ?
    Example doctest:
    """
    mutated_population = []
    for x in children:
        mutated_population.append(mutate_individual(x, mutate_rate))
    return mutated_population


# DO NOT MODIFY >>>>
def evaluate_individual(individual: Individual) -> None:
    """
    Purpose:        Computes and modifies the fitness for one individual
                    Assumes and relies on the logc of ./corpus/2_counts.py
    Parameters:     One Individual
    User Input:     no
    Prints:         no
    Returns:        None
    Modifies:       The individual (mutable object)
    Calls:          Basic python only
    Example doctest:
    """
    layout = individual["genome"]

    # Basic return to home row, with no extra cost for repeats.
    fitness = 0
    for key in layout:
        fitness += count_dict[key] * int(DISTANCE[layout.find(key)])

    # Vowels on the left, Consosants on the right
    for pos, key in enumerate(layout):
        if key in "AEIOUY" and pos > 14:
            fitness += 1

    # Top-down guess at ideal ergonomics
    for key in layout:
        fitness += count_dict[key] * int(ERGONOMICS[layout.find(key)])

    # [] {} () <> should be adjacent.
    # () ar fixed by design choice (number line).
    # [] and {} are on same keys.
    # Perhaps ideally, <> and () should be on same keys too...
    right_edges = [4, 9, 14, 16, 23, 29, 34]
    for pos, key in enumerate(layout):
        # order of (x or y) protects index on far right:
        if key == "[" and (pos in right_edges or "]" != layout[pos + 1]):
            fitness += 1
        if key == "," and (pos in right_edges or "." != layout[pos + 1]):
            fitness += 1

    # Symbols should be toward edges.
    for pos, key in enumerate(layout):
        if key in "-[],.';/=":
            fitness += int(PREFER_EDGES[pos])

    # Keybr.com querty-dvorak average data as estimate of real hand
    for pos, key in enumerate(layout):
        fitness += count_dict[key] / data_combine[pos]

    # Shortcut characters (skip this one).
    # On right hand for keyboarders (left ctrl is usually used)
    # On left hand for mousers (for one-handed shortcuts).
    pass

    individual["fitness"] = fitness


# <<<< DO NOT MODIFY


def evaluate_group(individuals: Population) -> None:
    """
    Purpose:        Computes and modifies the fitness for population
    Parameters:     example_genome string, Population
    User Input:     no
    Prints:         no
    Returns:        None
    Modifies:       The Individuals, all mutable objects
    Calls:          ?
    Example doctest:
    """
    for x in individuals:
        evaluate_individual(x)


def rank_group(individuals: Population) -> None:
    """
    Purpose:        Create one individual
    Parameters:     Population of Individuals
    User Input:     no
    Prints:         no
    Returns:        None
    Modifies:       The population's order (a mutable object)
    Calls:          ?
    Example doctest:
    """
    ranked_individuals = []
    ranked_individuals = sorted(
        individuals, key=lambda individual: individual["fitness"], reverse=False
    )
    for x in range(len(ranked_individuals)):
        individuals[x] = ranked_individuals[x]


def parent_select(individuals: Population, number: int) -> Population:
    """
    Purpose:        Choose parents in direct probability to their fitness
    Parameters:     Population, the number of individuals to pick.
    User Input:     no
    Prints:         no
    Returns:        Sub-population
    Modifies:       Nothing
    Calls:          ?
    Example doctest:
    """
    fitness_list = []
    for x in individuals:
        fitness_list.append(x["fitness"])
    selected_parents = random.choices(individuals, weights=fitness_list, k=number)
    return selected_parents


def survivor_select(individuals: Population, pop_size: int) -> Population:
    """
    Purpose:        Picks who gets to live!
    Parameters:     Population, and population size to return.
    User Input:     no
    Prints:         no
    Returns:        Population, of pop_size
    Modifies:       Nothing
    Calls:          ?
    Example doctest:
    """
    return individuals[:pop_size]


def evolve(example_genome: str, pop_size: int = 100) -> Population:
    """
    Purpose:        A whole EC run, main driver
    Parameters:     The evolved population of solutions
    User Input:     No
    Prints:         Updates every time fitness switches.
    Returns:        Population
    Modifies:       Various data structures
    Calls:          Basic python, all your functions
    """
    # To debug doctest test in pudb
    # Highlight the line of code below below
    # Type 't' to jump 'to' it
    # Type 's' to 'step' deeper
    # Type 'n' to 'next' over
    # Type 'f' or 'r' to finish/return a function call and go back to caller
    # print("Delete this and write")
    population = initialize_pop(example_genome=example_genome, pop_size=pop_size)
    evaluate_group(individuals=population)
    rank_group(individuals=population)
    best_fitness = population[0]["fitness"]
    dvorak = Individual(genome=DVORAK, fitness=0)
    evaluate_individual(dvorak)
    perfect_fitness = dvorak["fitness"]
    counter = 0
    while best_fitness > 23.9949:
        counter += 1
        parents = parent_select(individuals=population, number=80)
        children = recombine_group(parents=parents, recombine_rate=0.9)
        mutate_rate = ((best_fitness / perfect_fitness) - 1) / 5
        mutants = mutate_group(children=children, mutate_rate=0.05)
        evaluate_group(individuals=mutants)
        everyone = population + mutants
        rank_group(individuals=everyone)
        population = survivor_select(individuals=everyone, pop_size=pop_size)
        if best_fitness != population[0]["fitness"]:
            best_fitness = population[0]["fitness"]
            print("Iteration number", counter, "with best individual", population[0])
    return population


# Seed for base grade.
# For the exploratory competition points (last 10),
# comment this one line out if you want, but put it back please.
seed = True

# DO NOT MODIFY >>>>
if __name__ == "__main__":
    divider = "===================================================="
    # Execute doctests to protect main:
    # import doctest

    # doctest.testmod()
    # doctest.testmod(verbose=True)

    if seed:
        random.seed(42)

    with open("corpus/counts.json") as fhand:
        count_dict = json.load(fhand)

    # print("Counts of characters in big corpus, ordered by freqency:")
    # ordered = sorted(count_dict, key=count_dict.__getitem__, reverse=True)
    # for key in ordered:
    #     print(key, count_dict[key])

    print(divider)
    print(
        f"Number of possible permutations of standard keyboard: {math.factorial(len(DVORAK)):,e}"
    )
    print("That's a huge space to search through")
    print("The messy landscape is a difficult to optimize multi-modal space")
    print("Lower fitness is better.")

    print(divider)
    print("\nThis is the Dvorak keyboard:")
    dvorak = Individual(genome=DVORAK, fitness=0)
    evaluate_individual(dvorak)
    print_keyboard(dvorak)

    print(divider)
    print("\nThis is the Workman keyboard:")
    workman = Individual(genome=WORKMAN, fitness=0)
    evaluate_individual(workman)
    print_keyboard(workman)

    print(divider)
    print("\nThis is the Colemak keyboard:")
    colemak = Individual(genome=COLEMAK, fitness=0)
    evaluate_individual(colemak)
    print_keyboard(colemak)

    print(divider)
    print("\nThis is the QWERTY keyboard:")
    qwerty = Individual(genome=QWERTY, fitness=0)
    evaluate_individual(qwerty)
    print_keyboard(qwerty)

    print(divider)
    print("\nThis is a random layout:")
    badarr = list(DVORAK)
    random.shuffle(badarr)
    badstr = "".join(badarr)
    badkey = Individual(genome=badstr, fitness=0)
    evaluate_individual(badkey)
    print_keyboard(badkey)

    print(divider)
    input("Press any key to start")
    population = evolve(example_genome=DVORAK)

    print("Here is the best layout:")
    print_keyboard(population[0])

    grade = 0
    if qwerty["fitness"] < population[0]["fitness"]:
        grade = 0
    if colemak["fitness"] < population[0]["fitness"]:
        grade = 50
    if workman["fitness"] < population[0]["fitness"]:
        grade = 60
    elif dvorak["fitness"] < population[0]["fitness"]:
        grade = 70
    else:
        grade = 80

    with open(file="results.txt", mode="w") as f:
        f.write(str(grade))

    with open(file="best_ever.txt", mode="r") as f:
        past_record = f.readlines()[1]
    if population[0]["fitness"] < float(past_record):
        with open(file="best_ever.txt", mode="w") as f:
            f.write(population[0]["genome"] + "\n")
            f.write(str(population[0]["fitness"]))
# <<<< DO NOT MODIFY

# %%
