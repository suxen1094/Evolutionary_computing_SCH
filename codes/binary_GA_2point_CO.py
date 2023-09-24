from codes.global_variable import *

# Binary GA using 2-point crossover and bit-flip mutation strategies.
class binary_GA_2point_CO:
    def __init__(self, n=2, pc=0.9, pm=1/K):
        # parameters setting
        self.n = n                  # Used in tournament selection
        self.pc = pc                # Possibility of crossover
        self.pm = pm                # Possibility of mutation
        self.local_min = []         # The best result of this GA, initially null 
        self.population = []


        # Create the initial parents, which are 100 vectors
        # And calculate their fitness
        # Each vector has N elements
        # Each element has 10 bits(2^10) representing integers ranging in [-512, 511]
        for i in range(pop_size):
            vector = []
            for j in range(N):
                vector.append([random.randint(0, 1) for k in range(K)])
            self.population.append(vector)

        print('Successfully create binary_GA_2point_CO.')

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

            # deterministic
            best_index = self.the_best(self.population, index)

            best_parent = self.population[best_index]
            
            new_parent.append(best_parent)
        
        return new_parent

    def crossover(self, parent_a, parent_b):
        # 2-point crossover, which choose two index to divide
        # parent_a and parent_b are two vectors with N elements, each element has 10 bit
        child_1 = []
        child_2 = []
        for i in range(N):
            rand = random.random()
            element_1 = []
            element_2 = []

            # Do 2-point crossover
            if(rand < self.pc):

                # Choose two indices to divide (Both are included)
                # For example, if l = 1, r = 5, two bit string = 
                # B1:       [1, |0, 0, 0, 0, 0,| 1, 1, 0, 1], B2  = [0, |1, 1, 1, 1, 1,| 0, 0, 1, 1, 1]
                # => B1':   [1, |1, 1, 1, 1, 1,| 1, 1, 0, 1], B2' = [0, |0, 0, 0, 0, 0,| 0, 0, 1, 1, 1]
                l, r = 0, 0

                # Ensure that two swap indices are not be identical
                # Range from [0, 9]
                while l == r:
                    l = random.randint(0, K-1)
                    r = random.randint(0, K-1)

                    # Make sure that l <= r at all time
                    if l > r:
                        l, r = r, l
                

                for j in range(K):

                    # Swap
                    if j >= l and j <= r:
                        element_2.append(parent_a[i][j])
                        element_1.append(parent_b[i][j])
                    # No swap
                    else:
                        element_1.append(parent_a[i][j])
                        element_2.append(parent_b[i][j])

            # Directly copy it instead of crossover
            else:
                element_1 = parent_a[i]
                element_2 = parent_b[i]

            child_1.append(element_1)
            child_2.append(element_2)

        return (child_1, child_2)

    def mutation(self, x):
        # Bit-flip mutation, mutation possibility = self.pm
        # x is a vector with 10 elements, each has 10-bit
        new_x = []
        for i in range(N):
            xj = []
            for j in range(K):
                rand = random.random()
                if(rand < self.pm):
                    xj.append(1 - x[i][j]) # Bit-flip
                else:
                    xj.append(x[i][j])
            new_x.append(xj)
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

            # deterministic
            best_index = self.the_best(competitor, index)

            survivor.append(competitor[best_index])
        
        return survivor

    def binary_decimal(self, x):
        # Binary to decimal
        # x is a vector with N elements, each has "K" bits 
        # Return value: a vector with N elements, each is an integer
        new_x = []
        for i in range(N):
            ans = 0
            exp = 512
            if(x[i][0] == 0): # Sign bit = 0 => positive
                for j in range(K):
                    ans += x[i][j] * exp
                    exp = exp // 2
            else: # Negative
                tmp = [0 for j in range(K)]
                for j in range(K):
                    
                    tmp = 1 - x[i][j]
                    ans += tmp * exp
                    exp = exp // 2
                ans = (ans + 1) * -1
            new_x.append(ans)
        return new_x
    
    def the_best(self, population, index):
        # population is a list compose of vectors with 10 elements
        # index is a list with the chosen indices
        min_value = np.inf
        min_index = 0
        for i in range(len(index)):
            if min_value > schwefel(self.binary_decimal(population[index[i]])):
                min_value = schwefel(self.binary_decimal(population[index[i]]))
                min_index = index[i]
            
        return min_index

    def find_best(self):
        best = np.inf
        best_vector = []
        for i, s in enumerate(self.population):
            if best > (schwefel(self.binary_decimal(s))):
                best = schwefel(self.binary_decimal(s))
                best_vector = s

        return best, best_vector

    def evolution(self, f):
        
        self.start_time = time.time()
        self.global_min = np.inf
        print('Start the evolution of binary_GA_2point_CO')

        for i in range(termination):

            # Animation
            if (i+1) % 150 == 50: print(f'Running on generation {i+1} ﾍ( ´∀`)ﾉ............')
            elif (i+1) % 150 == 100: print(f'Running on generation {i+1} ......ﾍ( ´∀`)ﾉ......')
            elif (i+1) % 150 == 0: print(f'Running on generation {i+1} ............ﾍ( ´∀`)ﾉ')
            elif (i+1) == termination: print(f'Finish at generation {i+1}.')
                
            # Parent selection
            self.new_parents = self.parent_selection()
            self.offspring = []

            # Crossover
            for j in range(pop_size // 2):
                child1, child2 = self.crossover(self.new_parents[j], self.new_parents[j+1])
                self.offspring.append(child1)
                self.offspring.append(child2)
            
            # Mutation
            for j, child in enumerate(self.offspring):
                self.offspring[j] = self.mutation(child)

            # Survival selection
            self.population = self.survivor_selection()
            
            # Find the best value of this generation
            self.local_min, self.local_min_vector = self.find_best()

            # Update the anytime behavior if needed
            if (anytime_GA2[i] > self.local_min):
                anytime_GA2[i] = self.local_min

            # Update the global minima of this run if needed
            if self.global_min > self.local_min:
                self.global_min = self.local_min
                self.global_min_vector = self.local_min_vector

        self.spend_time = time.time() - self.start_time

    def plot(self):
        plt.plot(self.avr_generation, self.avr_fitness)
        plt.title('2-point-crossover Bit-flip-mutation Binary GA')
        plt.xlabel('Generation')
        plt.ylabel('f(x)')
        plt.show()
        plt.clf()

    def show_best(self, f):
        print('='*20 + '\n')
        print('binary_GA_2point_CO:')
        print(f'The best value of the whole processing: {self.global_min}')
        print(f'The best vector of the whole processing: {self.binary_decimal(self.global_min_vector)}')
        print(f'The end value after the whole processing: {self.local_min}')
        print(f'The end vector after the whole processing: {self.binary_decimal(self.local_min_vector)}')
        print(f'Time spent: {self.spend_time}s')
        print('\n' + '='*20)
        
        f.write('binary_GA_2point_CO:\n')
        f.write(f'{self.global_min}\n')
        for s in self.binary_decimal(self.local_min_vector):
            f.write(f'{s}, ')
        f.write(f'\ntime spent, {self.spend_time}\n')
        f.write('\n')