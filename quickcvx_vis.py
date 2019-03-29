#！python
#code = utf-8
"""
快速凸包算法的可视化分析
Author:MokeyDChaos
Date:2019-03-229
Version:1.0
"""
import random
import math
import operator
import matplotlib.pyplot as plt
import copy

def SortList(elem):
        """
        对列表进行排序时使用
        """
        return elem[0]

def GenerScatter(num):
    """
    生成一定数量的随机整数坐标点
    @num:随机点的数量
    @return:坐标点的数组
    """
    random_sca_list = []
    for i in range(num):
        ran_num = (random.randint(-100, 100), random.randint(-100, 100))
        random_sca_list.append(ran_num)
    
    return random_sca_list

def GetLine(point1, point2, flag = None):
    """
    求出过两点的直线Ax + By + C = 0
    @point1:直线经过的一个点
    @point2:直线经过的另一个点
    @return：[A, B, C]
    """
    A = (point1[1] - point2[1])
    B = (point2[0] - point1[0])
    C = point1[0] * point2[1] - point1[1] * point2[0]
    return [A, B, C]


def PointDisLine(point, line):
    """
    点到线的距离
    @point:点
    @line:线
    @return:距离 dis
    """
    return (line[0] * point[0] + line[1] * point[1] + line[2]) / math.sqrt(line[0] * line[0] + line[1] * line[1])

def PointDivison(point_set, line, cvxhu_point):
    """
    直线将坐标点集划分为两个
    @point_set:坐标点集合
    @line:线
    @cvx:_point:凸包点
    @return:pos_set, neg_set
    """
    pos_set = []
    neg_set = []
    for i in range(len(point_set)):
        dis = PointDisLine(point_set[i], line)
        if dis > 0:
            pos_set.append(point_set[i])
        elif dis < 0:
            neg_set.append(point_set[i])

    return pos_set, neg_set

def PointSearch(point_set, line, cvxhu_point):
    """
    寻找点集中到直线最远的点
    @point_set:作标点
    @line:线
    @cvxhu_point:凸包点集合
    @return:最远的点point
    """
    max_dis = 0
    max_point = (0, 0)
    j = []
    for i in range(len(point_set)):
        dis = abs(PointDisLine(point_set[i], line))
        print('point', point_set[i], 'dis', dis)
        if max_dis < dis:
            max_dis = dis
            max_point = point_set[i]
        # 如果为0说明它已经在凸包点集合中了
        if dis == 0:
            j.append(i)
    # 这里多个点相等的情况下我们是取数组中第一个点
        
    cvxhu_point.append(max_point)
    if len(j):
        point_set.remove(point_set[j[0]])
    point_set.remove(max_point)
    return max_point

def CvxSearchSm(point_set, cvxhu_point, line):
    """
    在点集中寻找凸包点
    @point_set:坐标点集合
    @cvxhu_point:凸包点集合
    @line:存放寻找基线经过的两个点的数组
    """
    # 一定要注意python中赋值、浅拷贝、深拷贝之间的区别呀
    print('1', point_set)
    flag = point_set
    print('f', flag)
    # 最初的基线
    base_line = GetLine(line[0], line[1])
    fir_point = PointSearch(flag, base_line, cvxhu_point)
    for i in range(len(line)):
        # 更新递归需要的点集合，和线
        line_set = [line[i], fir_point]
        temp_line = GetLine(line[i], fir_point)
        # 和基线首尾相连的划分线
        judge_line =  GetLine(line[1 - i], line[i])
        temp_flag = copy.copy(flag)
        while len(temp_flag) >= 1 :
            sub_po_set, sub_neg_set = PointDivison(temp_flag, temp_line, cvxhu_point)
            # 使用距离之间是否同号来判断点在哪一侧,这里一定注意让两个向量是首尾相连
            if len(sub_neg_set):
                if len(sub_po_set):
                    # 使用距离的乘积的正负来判断哪一个点集是我们需要的
                    if PointDisLine(sub_neg_set[0], temp_line) * PointDisLine(sub_neg_set[0], judge_line)  > 0:
                        temp_flag = sub_po_set
                    elif PointDisLine(sub_neg_set[0], temp_line) * PointDisLine(sub_neg_set[0], judge_line)  < 0:
                        temp_flag = sub_neg_set
                    else:
                        print('程序错误点位于线上')
                else:
                    if PointDisLine(sub_neg_set[0], temp_line) * PointDisLine(sub_neg_set[0], judge_line)  < 0:
                        temp_flag = sub_neg_set
                    else:
                        temp_flag = []
            else:
                if len(sub_po_set):
                    if PointDisLine(sub_po_set[0], temp_line) * PointDisLine(sub_po_set[0], judge_line)  < 0:
                        temp_flag = sub_po_set
                    else:
                        temp_flag = []
                else:
                    temp_flag = []
            # 这里因为flag的赋值不是实时受temp控制，所以加入判断防止错误点进入凸包集
            if len(temp_flag) > 1:
                print('开始递归')
                CvxSearchSm(temp_flag, cvxhu_point, line_set)
                # 递归后因为递归函数会继续执行之前不成立判断下的内容太，这里判断如果要搜索的点集已经存在于凸包集合我们就将搜索点集赋值为空集
                if len(list(set(cvxhu_point).intersection(flag))):
                    temp_flag = []
            if len(temp_flag) == 1:
                cvxhu_point.append(temp_flag[0])
                temp_flag = []
    CvxVis(point_set, list(set(cvxhu_point)))


 
def CvxVis(point_set, cvxhu_point, point1 = None, point2 = None):
    """
    将凸包可视化，用来检验算法正确性
    @point_set:坐标点
    @cvxhu_point:凸包点集合
    @point1,point2:用来检验算法正确性的，无意义
    """
    p_x = []
    p_y = []
    c_x = []
    c_y = []
    a = []
    b = []
    # 这里对凸包点集重新排列方便可视化检验程序正确性
    for each in cvxhu_point:
        if each[1] > 0:
            a.append(each)
        else:
            b.append(each)
    a.sort(key = SortList)
    b.sort(key = SortList, reverse = True )
    cvxhu_point = a + b
    # 使凸包相连
    if len(a):
        cvxhu_point.append(a[0])
    else:
        cvxhu_point.append(b[len(b)-1])
    for i in range(len(point_set)):
        p_x.append(point_set[i][0])
        p_y.append(point_set[i][1])
    for i in range(len(cvxhu_point)):
        c_x.append(cvxhu_point[i][0])
        c_y.append(cvxhu_point[i][1])

    plt.scatter(p_x, p_y, c = 'r', marker = 'x')
    plt.scatter(c_x, c_y, c = 'r')
    plt.plot(c_x, c_y, c = 'b')
    if point1:
        plt.plot([point1[0], point2[0]], [point1[1], point2[1]],  c = 'g')
    plt.show()

def main():
    
    a = GenerScatter(100)
    # 生成10个散点
    cvxhu_point = []
    # 按x轴排序
    a.sort(key = SortList)
    cvxhu_point = [a[0], a[len(a)-1]]
    first_line = GetLine(a[0], a[len(a)-1])
    # 分为两个点集
    po_set, neg_set = PointDivison(a, first_line, cvxhu_point)
    # 作为凸包点集合
    cvxhu_po = copy.copy(cvxhu_point)
    cvxhu_neg = copy.copy(cvxhu_point)
    # 作为基线经过点集合
    cvxhu_po1 = copy.copy(cvxhu_point)
    cvxhu_neg1 = copy.copy(cvxhu_point)
    # 分别搜索两个点集中的凸包点
    CvxSearchSm(po_set, cvxhu_po, cvxhu_po1)
    CvxSearchSm(neg_set, cvxhu_neg, cvxhu_neg1)
    # 合并两个凸包点集合
    cvxhu_point = list(set(cvxhu_po + cvxhu_neg))
    print(cvxhu_point)
    CvxVis(a, cvxhu_point)       



if __name__ == "__main__":
    main()
