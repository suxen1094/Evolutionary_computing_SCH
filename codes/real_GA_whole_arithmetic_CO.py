from codes.global_variable import *

# Real-valued GA using whole-arithmetic crossover and uniform mutation strategies.
class real_GA_whole_arithmetic_CO:
    def __init__(self, n=2, pc=0.9, pm=1/K):
        # parameters setting
        self.n = n                  # Used in tournament selection
        self.pc = pc                # Possibility of crossover
        self.pm = pm                # Possibility of mutation
        self.local_min = []         # The best result of this GA, initially null 
        self.population = []

        # Create the initial parents, which are 100 vectors
        # Each vector has N elements
        # Each element has a floating value ranging in [-512, 511]
        for i in range(pop_size):
            minimum = (2 ** (K-1)) * -1
            maximum = 2 ** (K-1) - 1
            vector = [random.uniform(minimum, maximum) for k in range(N)]
            self.population.append(vector)
        
        print('Successfully create real_GA_whole_arithmetic_CO.')

    def parent_selection(self):
        # Tournament selection, n = self.n
        # Return value: a list whose elements are vectors representing the parents selected.
        new_parent = []
        for i in range(pop_size):
            best_parent = []
            # Pick n population and choose the best one
            index = []
            k = list(range(0, pop_size-1))
            random.shuffle(k)
            for j in range(self.n):
                index.append(k[j])

            best_index = self.the_best(self.population, index)
            best_parent = self.population[best_index]
            
            new_parent.append(best_parent)
        
        return new_parent

    def crossover(self, parent_a, parent_b):
        # Whole-arithmetic crossover
        # parent_a and parent_b are two vectors with N elements, each element is a value range in [-512, 511]
        child_1 = []
        child_2 = []

        # Starting whole-arithmetic crossover
        for i in range(N):

            child_1.append(self.pc * parent_a[i] + (1-self.pc) * parent_b[i])
            child_2.append(self.pc * parent_b[i] + (1-self.pc) * parent_a[i])

        return (child_1, child_2)

    def mutation(self, x):
        # Uniform mutation, mutation possibility = self.pm
        # x is a vector with 10 elements, each has value ranging in [-512, 511]

        new_x = []
        for i in range(N):
            rand = random.random()
            minimum = (2 ** (K-1)) * -1
            maximum = 2 ** (K-1) - 1

            # Do mutation
            if rand < self.pm: 
                new_x.append(random.uniform(minimum, maximum))

            # Do nothing, just copy it
            else:
                new_x.append(x[i])
        return new_x

    def survivor_selection(self):
        # Also use tournament selection just like parent selection
        # Use Tournament selection to choose "pop_size" survivors from self.population and self.offspring
        competitor = []
        survivor = []
        for i in range(pop_size):
            competitor.append(self.population[i])
            competitor.append(self.offspring[i])
        # Tournament selection
        for i in range(pop_size):
            index = []
            k = list(range(0, 2*pop_size-1))
            random.shuffle(k)
            for j in range(s):
                index.append(k[j])

            best_index = self.the_best(competitor, index)
            survivor.append(competitor[best_index])
        
        return survivor
    
    def the_best(self, population, index):
        # population is a list compose of vectors with 10 elements
        # index is a list with the chosen indices
        min_value = np.inf
        min_index = 0
        for i in range(len(index)):
            if min_value > schwefel(population[index[i]]):
                min_value = schwefel(population[index[i]])
                min_index = index[i]
            
        return min_index
    
    def find_best(self):
        best = np.inf
        best_vector = []
        for s in self.population:
            if best > schwefel(s):
                best = schwefel(s)
                best_vector = s

        return best, best_vector

    def evolution(self, f):
        
        self.start_time = time.time()
        self.global_min = np.inf
        average = 0
        self.avr_fitness = []
        self.avr_generation = []
        print('Start the evolution of real_GA_whole_arithmetic_CO')

        for i in range(termination):
            if (i+1) % 30 == 0:
                f.write(f'{i+1}, {average/30}\n')
                self.avr_fitness.append(average/30)
                self.avr_generation.append(i+1)
                average = 0

            if (i+1) % 90 == 30: 
                print(f'Running on generation {i+1} ﾍ( ´∀`)ﾉ............')
            elif (i+1) % 90 == 60: 
                print(f'Running on generation {i+1} ......ﾍ( ´∀`)ﾉ......')
            elif (i+1) % 90 == 0: 
                print(f'Running on generation {i+1} ............ﾍ( ´∀`)ﾉ')
            elif (i+1) == termination: print(f'Finish at generation {i+1}.')
                
            self.new_parents = self.parent_selection()
            self.offspring = []

            for j in range(pop_size // 2):
                child1, child2 = self.crossover(self.new_parents[j], self.new_parents[j+1])
                self.offspring.append(child1)
                self.offspring.append(child2)
            
            for j, child in enumerate(self.offspring):
                self.offspring[j] = self.mutation(child)
            self.population = self.survivor_selection()
            
            self.local_min, self.local_min_vector = self.find_best()
            average += self.local_min

            anytime_GA4[i] += self.local_min

            if self.global_min > self.local_min:
                self.global_min = self.local_min
                self.global_min_vector = self.local_min_vector
            
        self.spend_time = time.time() - self.start_time

    def plot(self):
        plt.plot(self.avr_generation, self.avr_fitness)
        plt.title('Whole-arithmetic-crossover Uniform-mutation real-valued GA')
        plt.xlabel('Generation')
        plt.ylabel('f(x)')
        plt.show()
        plt.clf()

    def show_best(self, f):
        print('='*20 + '\n')
        print('real_GA_whole_arithmetic_CO:')
        print(f'The best value of the whole processing: {self.global_min}')
        print(f'The best vector of the whole processing: {self.global_min_vector}')
        print(f'The end value after the whole processing: {self.local_min}')
        print(f'The end vector after the whole processing: {self.local_min_vector}')
        print(f'Time spent: {self.spend_time}s')
        print('\n' + '='*20)

        f.write('real_GA_whole_arithmetic_CO:\n')
        f.write(f'{self.global_min}\n')
        for s in self.global_min_vector:
            f.write(f'{s}, ')
        f.write(f'\ntime spent, {self.spend_time}\n')
        f.write('\n')