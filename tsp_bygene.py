#！python
#code = utf-8
"""
tsp问题的遗传算法
Author:MokeyDChaos
Date:2019-04-01
Version:1.0
"""
import random
import copy

def GenerateCity(n):
    """
    生成一个n个点的完全图
    @n:tsp问题中的城市的数量
    @return:存有距离的二维数组，和一个记录着城市之间距离的字典
    """
    city_dis = []
    city_dis_temp = []
    city_map = {}
    for i in range(n):
        city_dis_temp = []
        for j in range(i, n):
            if i == j:
                random_dis = 0
            else:
                random_dis = random.randint(1, 11)
            city_dis_temp.append(random_dis)
            city_map['%d-%d'%(i, j)] = random_dis
            city_map['%d-%d'%(j, i)] = random_dis

        for l in range(i - 1, -1, -1):
            city_dis_temp.insert(0, city_dis[l][i])
        city_dis.append(city_dis_temp)
    return city_dis, city_map
    
def GenerateRace(m, n):
    """
    生成一个拥有n个个体的种群
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
    # 在tsp问题中我们希望路径越短越好，遗传算法中希望适应度越高越好，所以应该是路径越小适应度越高
    # 所以我用城市间的最大距离*城市数目-路劲长度来表示适应度
    # 最大距离在生成tsp问题时就已经设置
    fitness_score = 11 * len(individual) - sum_dis
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
        temp_sum = score[i] + temp_sum
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

def UpdateRace(race, dis):
    """
    通过变异交叉等方式，产生新的种群
    @race:种群
    @dis:城市之间的距离
    @return:一个新的种群
    """
    score = []
    new_race = []
    n_score = []
    for i in range(len(race)):
        score.append(FitnessFunction(race[i],dis))
    # 我们想把适应度最大的直接保留到新种群中
    new_race.append(race[score.index(max(score))]) 
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

    return new_race 

def main():
    dis, c_map = GenerateCity(10)
    # print(dis)
    # print('1-9', dis[0][8])
    race = GenerateRace(10, len(dis))
    # new_race = UpdateRace(race, dis)
    # print(new_race)
    # fit_score = []
    # for each in fir_race:
    #     fit_score.append(FitnessFunction(each, dis))
    # print('score', fit_score)
    generation = 0
    while True:
        generation = generation + 1
        print('start')
        race = UpdateRace(race, dis)
        print('new race appeared')
        if generation == 100:
            race_100 = race
            break
        else:
            continue
    temp_score = FitnessScore(race_100, dis)
    print(FitnessScore(race_100, dis))
    best_one =  race_100[temp_score.index(max(temp_score))]
    print(best_one, '长度：', 11 * len(temp_score) - max(temp_score))

    # child1, child2 = GeneCycleCross([1,2,3,4,5,6,7,8], [2,4,6,8,7,5,3,1])
    # child1, child2 = GenePosCross([1,2,3,4,5,6,7,8], [2,4,6,8,7,5,3,1])
    # print(child1, 'other', child2)
    # GeneVar(child1)
    # print('after var', child1)
    # result = Roulette([10,30,90,100,150,260], 3, repeat = False)
    # print(result)
if __name__ == "__main__":
    main()
