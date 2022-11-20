from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import numpy as np

import random


distribution_num = 1000
run_num = 20

def question1():
    result_list = []
    x_list = []
    bound_list = []
    max_num = float('-inf')
    prophet_expected_value = float('-inf')
    median = float('-inf')

    for run in range(run_num):
        for idx in range(distribution_num):
            a = random.random()
            width = 1
            b = random.random() + width
            bound_list.append((a,b))
            random_number = truncnorm.rvs(a, b)
            x_list.append(random_number)

        max_idx = np.argmax(x_list)
        a,b = bound_list[max_idx]
        prophet_expected_value = truncnorm.stats(a, b, moments='m')
        median = truncnorm.median(a, b)
        lambda_value = prophet_expected_value * 0.5


        median_threshold = median
        # The alg.

        for time_i in range(len(x_list)):
            if x_list[time_i] >= lambda_value:
                mean_alg = truncnorm.stats(bound_list[time_i][0], bound_list[time_i][1], moments='m')
                break

        for time_i in range(len(x_list)):
            if x_list[time_i] >= median_threshold:
                median_alg = truncnorm.stats(bound_list[time_i][0], bound_list[time_i][1], moments='m')
                break
        
        result_list.append((mean_alg / prophet_expected_value, 
                            median_alg / prophet_expected_value))


    fig, ax = plt.subplots(1, 1)
    mean_ratio_list = [i[0] for i in result_list]
    median_ratio_list = [i[1] for i in result_list]
    ax.plot([i for i in range(run_num)], mean_ratio_list,
        'r-', lw=1, alpha=0.6, label='mean')
    ax.plot([i for i in range(run_num)],median_ratio_list ,
        'b-', lw=1, alpha=0.6, label='median')
    plt.title("Median threshold and mean threshold")
    plt.xlabel("# of runs")
    ax.legend()
    txt=f"Min median ratio {min(mean_ratio_list)}, Min mean ratio {min(median_ratio_list)}"
    fig.text(.5, 0.02, txt, ha='center')
    fig.set_size_inches(7, 7, forward=True)
    plt.ylabel("E[Alg] / E[Prophet]")
    plt.savefig('prophet_k=1.png')

def question_2_3(k):
    assert k <= distribution_num,"k is too large"
    result_list = []
    x_list = []
    bound_list = []
    max_num = float('-inf')
    prophet_expected_value = float('-inf')
    median = float('-inf')

    for run in range(run_num):
        for idx in range(distribution_num):
            a = random.random()
            width = 1
            b = random.random() + width
            bound_list.append((a,b))
            random_number = truncnorm.rvs(a, b)
            x_list.append(random_number)


        max_idx_array = np.argpartition(x_list, (-1)*k)[(-1)*k:]
        max_bound_list = [(bound_list[i][0],bound_list[i][1]) for i in max_idx_array]
        median_sum = 0
        for each_bound in max_bound_list:
            median = truncnorm.median(each_bound[0], each_bound[1])
            median_sum += median

        median_sum /= k
        
        prophet_sum = 0
        for each_max_idx in max_idx_array:
            a, b = bound_list[each_max_idx]
            prophet_expected_value = truncnorm.stats(a, b, moments='m')
            prophet_sum += prophet_expected_value

            median = truncnorm.median(a, b)

        prophet_sum /= k

        lambda_value = prophet_sum * 0.5

        median_threshold = median_sum
        # The alg.
        mean_counter = 0
        mean_alg = 0
        for time_i in range(len(x_list)):
            if mean_counter == k:
                break
            if x_list[time_i] >= lambda_value:
                mean_alg += truncnorm.stats(bound_list[time_i][0], bound_list[time_i][1], moments='m')
                mean_counter+=1
        mean_alg/=k 

        median_counter = 0
        median_alg = 0
        for time_i in range(len(x_list)):
            if median_counter == k:
                break
            if x_list[time_i] >= median_threshold:
                median_alg += truncnorm.stats(bound_list[time_i][0], bound_list[time_i][1], moments='m')
                median_counter+= 1
        median_alg /=k        
        
        result_list.append((mean_alg / prophet_sum, 
                            median_alg / prophet_sum))

    #print(result_list)
    fig, ax = plt.subplots(1, 1)
    mean_ratio_list = [i[0] for i in result_list]
    median_ratio_list = [i[1] for i in result_list]
    ax.plot([i for i in range(run_num)], mean_ratio_list,
        'r-', lw=1, alpha=0.6, label='mean')
    ax.plot([i for i in range(run_num)],median_ratio_list ,
        'b-', lw=1, alpha=0.6, label='median')
    plt.title(f"Median threshold and mean threshold with k={k}")
    plt.xlabel("# of runs")
    ax.legend()
    txt=f"Min median ratio {min(mean_ratio_list)}, Min mean ratio {min(median_ratio_list)}"
    fig.text(.5, 0.02, txt, ha='center')
    fig.set_size_inches(7, 7, forward=True)
    plt.ylabel("E[Alg] / E[Prophet]")
    plt.savefig(f'general_case_with_k={k}.png')

# Question 1
question1()
# Question 2

k = 2
question_2_3(k)

# Question 3
k = 5
question_2_3(k)


