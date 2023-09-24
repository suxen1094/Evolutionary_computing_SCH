'''
    Author:             Suxen
    Date:               2023/3/13
    File decription:    Homework 1 for the evolution computation
'''

############# Initial setting ###############
from codes.global_variable import *
from codes.binary_GA_2point_CO import binary_GA_2point_CO
from codes.binary_GA_uniform_CO import binary_GA_uniform_CO
from codes.real_GA_uniform_CO import real_GA_uniform_CO
from codes.real_GA_whole_arithmetic_CO import real_GA_whole_arithmetic_CO

############## Global function definition #############

def write_anytime():
    temp = [anytime_GA1, anytime_GA2, anytime_GA3, anytime_GA4]
    GA_min = [GA1_min, GA2_min, GA3_min, GA4_min]
    slope_GA1 = [0 for k in range(termination)]
    slope_GA2 = [0 for k in range(termination)]
    slope_GA3 = [0 for k in range(termination)]
    slope_GA4 = [0 for k in range(termination)]

    for i in range(termination-1):
        slope_GA1[i] = anytime_GA1[i+1] - anytime_GA1[i]
        slope_GA2[i] = anytime_GA2[i+1] - anytime_GA2[i]
        slope_GA3[i] = anytime_GA3[i+1] - anytime_GA3[i]
        slope_GA4[i] = anytime_GA4[i+1] - anytime_GA4[i]
    
    slope_GA1[termination-1] = slope_GA2[termination-1] = slope_GA3[termination-1] = slope_GA4[termination-1] = 0
    slope = [slope_GA1, slope_GA2, slope_GA3, slope_GA4]

    with open('108062226_aver.csv', 'a') as f:
        f.write('\n================\n')
        f.write('Normal with aver over 30\n')
        for i in range(4):
            f.write('================\n')
            f.write(f'GA{i+1}:\n')
            f.write(f'fitness, slope\n')

            for j in range(termination):
                f.write(f'{temp[i][j]}, {slope[i][j]}\n')
            
            f.write(f"The best result of this GA is:\n")
            f.write(f"{GA_min[i]}\n")

def plot_anytime():
    
    # if 'images' folder doesn't exist then create it
    if not(os.path.isdir('images')):
        os.mkdir('images')

    generation = [k for k in range(1, termination+1)]
    label = ['binary_GA_uniform_CO', 'binary_GA_2point_CO', 'real_GA_uniform_CO', 'real_GA_whole_arithmetic_CO']
    
    plt.plot(generation, anytime_GA1, label=label[0])
    plt.legend(loc='upper right')
    plt.plot(generation, anytime_GA2, label=label[1])
    plt.legend(loc='upper right')
    plt.plot(generation, anytime_GA3, label=label[2])
    plt.legend(loc='upper right')
    plt.plot(generation, anytime_GA4, label=label[3])
    plt.legend(loc='upper right')
    plt.title('GA comparison')
    plt.xlabel('Generation')
    plt.ylabel('f(x)')
    plt.savefig(f'images\Round_{current_round}_Figure_aver_over_30.jpg')
    # plt.show()
    plt.clf()

############### Main function ################

if __name__ == '__main__':

    
    f = open('108062226_aver.csv', 'w')
    f.close()
    with open('108062226_result.csv', 'w') as f:
        for i in range(take_aver):
            
            f.write(f'Round {i}\n')
            print(f'Round {i+1}')

            GA1 = binary_GA_uniform_CO()
            GA1.evolution(f)
            GA1.show_best(f)

            GA2 = binary_GA_2point_CO()
            GA2.evolution(f)
            GA2.show_best(f)

            GA3 = real_GA_uniform_CO()
            GA3.evolution(f)
            GA3.show_best(f)
            
            GA4 = real_GA_whole_arithmetic_CO()
            GA4.evolution(f)
            GA4.show_best(f)

            # Calculate the min over 30 times
            if GA1_min > GA1.global_min:
                GA1_min = GA1.global_min
            if GA2_min > GA2.global_min:
                GA2_min = GA2.global_min
            if GA3_min > GA3.global_min:
                GA3_min = GA3.global_min
            if GA4_min > GA4.global_min:
                GA4_min = GA4.global_min

    plot_anytime()
    write_anytime()
    current_round += 1