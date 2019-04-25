#！python
#code = utf-8
"""
tsp问题的遗传算法
Author:MokeyDChaos
Date:2019-04-25
Version:4.0
"""
import random
import copy
import math
import matplotlib.pyplot as plt
import itertools
import pysnooper

def GenerateCity(n):
    """
    生成n个随机坐标的城市图
    @n:tsp问题中的城市的数量
    @return:存有距离的二维数组，记录城市位置的数组
    """
    city = []
    for k in range(n):
        city.append((random.randint(-100, 100), random.randint(-100, 100)))
    city_dis = []
    city_dis_temp = []
    for i in range(n):
        city_dis_temp = []
        for j in range(i, n):
            if i == j:
                dis = 0
            else:
                dis = (city[j][0] - city[i][0]) * (city[j][0] - city[i][0]) + (city[j][1] - city[i][1]) * (city[j][1] - city[i][1]) 
            city_dis_temp.append(dis)
            # city_map['城市%d-%d的距离'%(i, j)] = random_dis
            # city_map['城市%d-%d的距离'%(j, i)] = random_dis

        for l in range(i - 1, -1, -1):
            city_dis_temp.insert(0, city_dis[l][i])
        city_dis.append(city_dis_temp)
    return city_dis, city
    
def GenerateRace(m, n):
    """
    生成一个拥有m个个体的种群
    @m:种群个体的数量
    @n:每个个体的长度
    @return:返回一个种族 
    """
    # 排好顺序的一个个体
    fir_in = list(range(n))
    race = []
    for i in range(m):
        a = copy.copy(fir_in)
        random.shuffle(a)
        race.append(a)
    
    return race


def FitnessFunction(individual, dis):
    """
    计算个体的适应度
    @individual:个体，即路径
    @dis:存放每个城市之间的距离的数组
    @return:个体即路径的总长度
    """
    sum_dis = 0
    for i in range(len(individual) - 1):
        sum_dis = sum_dis + dis[individual[i]][individual[i+1]]
    sum_dis = sum_dis + dis[individual[len(individual) - 1]][individual[0]]
    # 在tsp问题中我们希望路径越短越好，遗传算法中希望适应度越高越好，所以应该是路径越小适应度越高
    # 所以我用两个max寻找城市间的近似最大距离*城市数目-路劲长度来表示适应度
    # 近似最大距离在生成城市图时相当于是一个定值
    fitness_score = max(max(dis)) * len(individual) - sum_dis
    return fitness_score

def FitnessScore(race, dis):
    """
    传入一个族群
    @race:族群
    @dis:存放每个城市之间的距离的数组
    @return:包含每个个体的适应度得分的数组
    """
    score = []
    for i in range(len(race)):
        score.append(FitnessFunction(race[i], dis))
    return score

def GeneCycleCross(father_in, mother_in):
    """
    使用循环交叉的方法生成两个子代
    出现bug，暂时不用
    @father_in:父代1
    @mother_in:父代2
    @return:child1, child2
    """
    child2 = copy.copy(father_in)
    child1 = copy.copy(mother_in)
    c1_index = 1
    c2_index = 1
    while True:
        # 将得到的母亲的基因值作为索引，将位于该位置的父代基因添加到相同位置的子代基因中
        child1[c1_index - 1] = father_in[c1_index - 1]
        # 找到母亲基因中索引值等于子代中加入的值的元素   
        c1_index = mother_in[father_in[c1_index - 1] - 1]
        print(c1_index)
        if c1_index != father_in[0]:
            continue
        else:
            break
        
    while True:
        # 同上
        child2[c2_index - 1] = mother_in[c2_index - 1]   
        c2_index = father_in[mother_in[c2_index - 1] - 1]
        if c2_index != mother_in[0]:
            continue
        else:
            break
    return child1, child2

def GenePosCross(father_in, mother_in):
    """
    使用交替位置的方法生成两个子代
    @father_in:父代1
    @mother_in:父代2
    @return:child1, child2
    """
    child1 = []
    child2 = []
    for i in range(len(father_in)):
        if father_in[i] in child1:
            child2.append(father_in[i])
        else:
            child1.append(father_in[i])
        
        if mother_in[i] in child1:
            child2.append(mother_in[i])
        else:
            child1.append(mother_in[i])
    return child1, child2

def GeneVar(individual):
    """
    个体发生变异
    @individual:发生变异的个体
    """
    n = random.randint(0, len(individual)-1 -1)
    individual[n], individual[n+1] = individual[n+1], individual[n]

def Roulette(score, n, repeat = True):
    """
    轮盘法根据得分比例的不同随机选出n个个体
    @score:得分列表
    @n:随机个体的数量
    @repeat:是否容许选出来的数字重复
    @return:个体位置的列表
    """
    add_score = []
    temp_sum = 0
    pos = []
    
    for i in range(len(score)):
        # 这里做一个标定
        temp_sum = score[i] - min(score) + 1 + temp_sum
        add_score.append(temp_sum)
    
    Length = len(add_score) - 1
    
    def dichotomy(in_list, num):
        """
        二分法确定轮盘位置
        """
        l = len(in_list)
        index_left = 0
        index_right = l
        while True:
            index_mid = (index_left + index_right) // 2
            if index_right - index_left != 1 \
                or in_list[index_left - 1] > num or in_list[index_right - 1] < num:
                if num > in_list[index_mid - 1]:
                    index_left = index_mid 
                elif num < in_list[index_mid - 1]:
                    index_right = index_mid
                else:
                    break
            else:
                break
        return index_left - 1   
    
    #在交叉时我们希望两个不同的个体发生交叉，而变异时则没有要求 
    k = n
    if repeat:
        for j in range(n):
            ran_num = random.randint(add_score[0], add_score[Length])    
            pos.append(dichotomy(add_score, ran_num))
                
    else:
        while k > 0:
            ran_num = random.randint(add_score[0], add_score[Length])
            temp_pos = dichotomy(add_score, ran_num)
            if temp_pos not in pos:
                pos.append(temp_pos)
                k = k - 1
            else:
                continue    
    return pos

def UpdateRace(race, dis, best_score):
    """
    通过变异交叉等方式，产生新的种群
    @race:种群
    @dis:城市之间的距离
    @return:一个新的种群
    """
    score = []
    new_race = []
    best_score_set = best_score
    n_score = []
    for i in range(len(race)):
        score.append(FitnessFunction(race[i],dis))
    # 我们想把适应度最大的直接保留到新种群中
    new_race.append(race[score.index(max(score))])
    best_score_set.append(max(score)) 
    # 先交叉，我希望适应度越低的越容易交叉
    race_size = len(race)
    while True:
        parents_pos = Roulette(score, 2, False)
        child1, child2 = GenePosCross(race[parents_pos[0]], race[parents_pos[1]])
        new_race.append(child1)
        new_race.append(child2)
        if len(new_race) < race_size:
            continue
        else:
            break
    
    for j in range(len(new_race)):
        n_score.append(FitnessFunction(new_race[i],dis))
    
    # 再变异
    var_num = random.randint(0, race_size // 2)
    var_pos = Roulette(n_score, var_num)
    for each in var_pos:
        GeneVar(new_race[each])

    return new_race, best_score

def TwoExNeigh(best_individual, best_individual_fitness, n, dis):
    """
    二交换后得到的领域
    @best_individual:通过遗传法得到的最优个体
    @best_individual_fitness:个体的适应度
    @n:二交换的次数
    @dis:城市间距离数组
    @return:最优个体的领域
    """
    neigh_area = []
    score_area = []
    Length = len(best_individual)
    new_individual = copy.copy(best_individual)
    for i in range(n):
        a = random.randint(0, Length - 1)
        index1 = a
        best_individual[a], best_individual[Length - 1] = best_individual[Length - 1], best_individual[a]
        b = random.randint(0, Length - 2)
        index2 = new_individual.index(best_individual[b])
        new_individual[index1], new_individual[index2] = new_individual[index2], new_individual[index1]
        new_individual_score = FitnessFunction(new_individual, dis)
        if new_individual_score > best_individual_fitness:
            neigh_area.append(new_individual)
            score_area.append(math.sqrt(max(max(dis)) * Length - new_individual_score))
    
    return neigh_area, score_area

# @pysnooper.snoop('D:\Study\研一\高级数据结构\path_vis.log')
def PathVisible(individual, city):
    """
    将tsp问题可视化
    @individual:路径
    @city:城市坐标
    """
    city_x = []
    city_y = []
    for each in individual:
        city_x.append(city[each][0])
        city_y.append(city[each][1])
    
    city_x.append(city[individual[0]][0])
    city_y.append(city[individual[0]][1])
    
    plt.scatter(city_x, city_y, c = 'r')
    plt.plot(city_x, city_y, c = 'b')
    plt.show()

# @pysnooper.snoop()
def main():
    dis, city_map = GenerateCity(50)
    # print('max dis', max(max(dis)))
    # print('dis', dis, 'c_m', city_map)
    # dis = [[0, 1125, 5513, 15041, 980, 28565, 754, 34, 37577, 10397], [1125, 0, 10676, 19652, 4121, 36260, 1873, 1297, 47048, 16976], [5513, 10676, 0, 4640, 3637, 10312, 8665, 4825, 15188, 772], [15041, 19652, 4640, 0, 14845, 2824, 21905, 13649, 6660, 3316], [980, 4121, 3637, 14845, 0, 26073, 1258, 986, 33685, 7569], [28565, 36260, 10312, 2824, 26073, 0, 36901, 26693, 820, 6084], [754, 1873, 8665, 21905, 1258, 36901, 0, 1088, 46517, 14545], [34, 1297, 4825, 13649, 986, 26693, 1088, 0, 35477, 9425], [37577, 47048, 15188, 6660, 33685, 820, 46517, 35477, 0, 9448], [10397, 16976, 772, 3316, 7569, 6084, 14545, 9425, 9448, 0]]
    # city_map = [(67, -67), (100, -61), (0, -35), (-4, 33), (39, -81), (-54, 51), (72, -94), (64, -62), (-82, 57), (-24, -21)]
    race = GenerateRace(100, len(dis))
    best_score = []
    last_appro_min_dis = 0
    i = 0
    while True:
        # 对同一个tsp问题计算多次
        best_score = []
        while True:
            # 一次计算
            race, best_score = UpdateRace(race, dis, best_score)
            repeat_num = [len(list(v)) for k,v in itertools.groupby(best_score)]
            # 取最近的一次进化重复次数
            no_evo_generation = repeat_num[len(repeat_num) - 1] 
            # 当同一个路径长度重复出现几次后停止迭代
            if no_evo_generation == 20:
                race_final = race
                break
            else:
                continue
        temp_score = FitnessScore(race_final, dis)
        best_one =  race_final[temp_score.index(max(temp_score))]
        appro_min_dis = math.sqrt(max(max(dis)) * len(race_final[0]) - max(temp_score))
        print(best_one, '长度：', appro_min_dis)
        if last_appro_min_dis == appro_min_dis:
            i = i + 1
        else:
            last_appro_min_dis = appro_min_dis
            i = 0
        # 如果连续3次对这个tsp问题的最优解都相同，就推出循环，视为寻找到了近似解
        if i == 5:
            break

    PathVisible(best_one, city_map)
        
        # ne_area, ne_area_score = TwoExNeigh(best_one, max(temp_score), 1000, dis)
        # print('通过二交换得到的长度为', ne_area_score)
        # if len(ne_area) != 0:
        #     print('进行二交换')
        #     temp_index = ne_area_score.index(min(ne_area_score))
        #     print('index', temp_index)
        #     print('path', ne_area[temp_index])
            # PathVisible(ne_area[temp_index], city_map)
        

if __name__ == "__main__":
    main()
