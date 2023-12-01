import numpy as np
from sklearn.model_selection import train_test_split
import numpy as np
import keras
from keras.layers import Conv2D
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras import Sequential
from gene_to_set import *

(X_train, Y_train), (X_test, Y_test) = keras.datasets.cifar10.load_data()
X_train, X_test = X_train / 255.0, X_test / 255.0
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size = 0.2)
X_val, X_fitness, Y_val, Y_fitness = train_test_split(X_val, Y_val, test_size = 0.5)

POPULATION_SIZE = 50
GENE_LENGTH = 11
MAX_GEN = 10
MUTATION_PROB = 0.1

def Set_to_CNN(decoded_gene):
	model = Sequential()
	flatten_flag = False
	first_flag = False
	if (decoded_gene.count('C') == 0):
		decoded_gene.append('C')
	if (decoded_gene.count('F') == 0):
		decoded_gene.append('F')

	for element in sorted(decoded_gene):
		if element == 'C':
			if (not first_flag):
				model.add(Conv2D(32, (3,3), activation='relu', padding='same', input_shape=(32,32,3)))
				model.add(MaxPooling2D((2,2)))
				first_flag = True
			else:
				model.add(Conv2D(64, (3,3), activation='relu', padding='same))
				model.add(MaxPooling2D((2,2)))
		if element == 'F':
			if (not flatten_flag):
				model.add(Flatten())
				flatten_flag = True
			model.add(Dense(64, activation='relu'))
		
	model.add(Dense(10))
	return model

def fitness(gene):
	gene = bitstring_to_gene(gene)
	decoded_gene = Gene_to_Set(gene)
	model = Set_to_CNN(decoded_gene)
	#model.summary()
	model.compile(loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True), optimizer='adam', metrics=['accuracy'])
	history = model.fit(X_train, Y_train, epochs=10, validation_data=(X_val, Y_val), verbose=0)

	test_loss, test_acc = model.evaluate(X_fitness, Y_fitness, verbose=0)
	return test_acc



'''
	Function reproduce takes in two parent states and generates a random child
	We first choose a random crossover point in the state (there are 9 possibilities for this: 0 through 8 including both)
	The child is generated by appending the first end of parent1 until the crossover point and second end of parent2
'''

def reproduce(parent1, parent2, GENE_LENGTH):
	c = np.random.randint(0,GENE_LENGTH+1)
	child = parent1.copy()
	child[c:] = parent2[c:]
	return child

'''
	Function mutate takes in a state, a mutation probability
	for each position of the state, we choose a random value with probability mutation_prob
'''

def mutate(gene, MUTATION_PROB, GENE_LENGTH):
	mutated_gene = gene.copy()
	for i in range(GENE_LENGTH):
		random_gen = np.random.uniform()
		if (random_gen < MUTATION_PROB):
			mutated_gene[i] = 1 - mutated_gene[i]
	return mutated_gene

'''
	Function genetic_run executes a single run of the genetic algorithm
	It takes in the population size, number of iterations, mutation probability
	We first populate the population randomly
	We also maintain a variable h_opt that keeps track of the minimum heuristic value across all individuals seen so far
	In each iteration, we evaluate the fitness of the current population and define the selection probability by normalizing
	We select two parents at random using this probability distribution and then generate a child and perform mutation
	The population is then updated to consist of these children
	At the end of all iterations, we return the optimal value h* we have seen across all individuals
'''

def genetic_run(MAX_GEN, POPULATION_SIZE, GENE_LENGTH, MUTATION_PROB):
	population = []
	num_individuals = 0

	print("Generation: 0")
	print("-----------------------")

	for i in range(POPULATION_SIZE):
		random_gene = np.random.randint(2, size=GENE_LENGTH)
		population.append(random_gene)

	opt_fitness = fitness(population[0])
	num_individuals += 1
	print(f"Individual Number: {num_individuals}")
	print(f"Fitness observed: {opt_fitness}")
	print()
	opt_gene = population[0]


	for gen in range(MAX_GEN):
		if (gen == 0):
			for i in range(1, POPULATION_SIZE):
				current_gene = population[i]
				current_fitness = fitness(current_gene)
				num_individuals += 1
				print(f"Individual Number: {num_individuals}")
				print(f"Fitness observed: {current_fitness}")
				print()
				if (current_fitness > opt_fitness):
					opt_fitness = current_fitness
					opt_gene = current_gene
			continue
		print(f"Generation: {gen+1}")
		print("-----------------------")
		new_population = []
		population_fitness = [fitness(gene) for gene in population]
		selection_probability = population_fitness / np.sum(population_fitness)
		for j in range(population_size):
			indices = np.random.choice(POPULATION_SIZE,2,p=selection_probability)
			parent1 = population[indices[0]]
			parent2 = population[indices[1]]
			child = reproduce(parent1,parent2, GENE_LENGTH)
			child = mutate(child, MUTATION_PROB, GENE_LENGTH)
			new_population.append(child)
		population = new_population
		for i in range(population_size):
			current_gene = population[i]
			current_fitness = fitness(current_gene)
			if (current_fitness > opt_fitness):
				opt_fitness = current_fitness
				opt_gene = current_gene
	print(f"Optimal Fitness: {opt_fitness}")
	print(f"Optimal Gene: {opt_gene}")

genetic_run(MAX_GEN, POPULATION_SIZE, GENE_LENGTH, MUTATION_PROB)
