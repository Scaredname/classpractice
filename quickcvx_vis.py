#！python
#code = utf-8
"""
快速凸包算法的可视化分析
Author:MokeyDChaos
Date:2019-03-21
Version:1.0
"""
import random
import math
import operator
import matplotlib.pyplot as plt
import copy

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

def GetLine(point1, point2):
    """
    求出过两点的直线Ax + By + C = 0
    @point1:直线经过的一个点
    @point2:直线经过的另一个点
    @return：[A, B, C]
    """
    # print(point1,point2,'hh')
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
    for i in range(len(point_set)):
        dis = abs(PointDisLine(point_set[i], line))
        if max_dis < dis:
            max_dis = dis
            max_point = point_set[i]
    # 这里多个点相等的情况下我们是取数组中第一个点
        
    cvxhu_point.append(max_point)
    point_set.remove(max_point)
    return max_point


def CvxSearch(point_set, cvxhu_point):
    """
    在点集中寻找凸包点
    @point_set:坐标点
    @cvxhu_point:凸包点集合
    """
    # 一定要注意python中赋值、浅拷贝、深拷贝之间的区别呀
    flag = copy.copy(point_set)
    cvxhu_point1 = copy.copy(cvxhu_point)
    cvxhu_point2 = copy.copy(cvxhu_point)
    # 最初的划分线
    base_line = GetLine(cvxhu_point[1], cvxhu_point[0])
    #感觉需要递归一下
    while len(flag) >= 1:
        print('flag:', flag)
        if len(flag) != 1:
            fir_point = PointSearch(flag, base_line, cvxhu_point1)
            n = len(cvxhu_point1)
            base_line = GetLine(cvxhu_point1[n-2], cvxhu_point1[n-1])
            print('cv1-in0:', cvxhu_point1, 'fir:', fir_point, 'cvxhu_point', cvxhu_point1[n-2])
            sub_po_set, sub_neg_set = PointDivison(flag, base_line, cvxhu_point1)
            print('po:', sub_po_set, 'neg', sub_neg_set)
            # 无法确定我们到底需要的是划分后左侧点集还是右侧点集，这里判断一下两个点集中分别一个点到原点的距离，并与直线到原点的距离比较，距离更远的就是我们需要的点集
            # 上面方法失败，尝试使用距离之间是否同号来判断点在哪一侧
            if len(sub_neg_set):
                if len(sub_po_set):
                    # 使用距离的正负来判断哪一个点集是我们需要的
                    if PointDisLine(sub_neg_set[0], base_line) * PointDisLine(sub_neg_set[0], GetLine(cvxhu_point1[n-2], cvxhu_point1[n-3])) > 0:
                        flag = sub_neg_set
                    elif PointDisLine(sub_neg_set[0], base_line) * PointDisLine(sub_neg_set[0], GetLine(cvxhu_point1[n-2], cvxhu_point1[n-3])) < 0:
                        flag = sub_po_set
                    else:
                        print('程序错误点位于线上')
                else:
                    if PointDisLine(sub_neg_set[0], base_line) * PointDisLine(sub_neg_set[0], GetLine(cvxhu_point1[n-2], cvxhu_point1[n-3])) > 0:
                        flag = sub_neg_set
                    else:
                        break
            else:
                if len(sub_po_set):
                    if PointDisLine(sub_po_set[0], base_line) * PointDisLine(sub_po_set[0], GetLine(cvxhu_point1[n-2], cvxhu_point1[n-3])) > 0:
                        flag = sub_po_set
                    else:
                        break
                else:
                    break 
        else:
            cvxhu_point1.append(flag[0])
            break
        CvxVis(point_set, cvxhu_point1, cvxhu_point1[n-2], fir_point)
    
    # 向另一个方向寻找
    # 这里出现新的问题，我们只有第一次是和间隔一个点的点相连，之后都是和上一个点相连
    # 想了一下决定使用一个笨办法，加一个记录循环次数的数字，再进行判断    
    flag1 = copy.copy(point_set)
    base_line1 = GetLine(cvxhu_point[1], cvxhu_point[0])
    print(base_line, '1', base_line1)
    while len(flag1) >= 1:
        print('flag1:', flag1)
        if len(flag1) != 1:
            num = 1
            fir_point = PointSearch(flag1, base_line1, cvxhu_point2)
            n = len(cvxhu_point2)
            # 笨办法
            if num == 1:
                base_line1 = GetLine(cvxhu_point2[n-3], cvxhu_point2[n-1])
                print('cv2-in0:', cvxhu_point1, 'fir:', fir_point, 'cvxhu_point2', cvxhu_point2[n-3])
            else:
                base_line1 = GetLine(cvxhu_point2[n-2], cvxhu_point2[n-1])
                print('cv2-in0:', cvxhu_point1, 'fir:', fir_point, 'cvxhu_point2', cvxhu_point2[n-2])
            sub1_po_set, sub1_neg_set = PointDivison(flag1, base_line1, cvxhu_point2)
            print('po2:', sub1_po_set, 'neg2', sub1_neg_set)
            # 同上
            if len(sub1_neg_set):
                if len(sub1_po_set):
                    if PointDisLine(sub1_neg_set[0], base_line1) * PointDisLine(sub1_neg_set[0], GetLine(cvxhu_point2[n-2], cvxhu_point2[n-3])) < 0:
                        flag1 = sub1_neg_set
                    elif PointDisLine(sub1_neg_set[0], base_line1) * PointDisLine(sub1_neg_set[0], GetLine(cvxhu_point2[n-2], cvxhu_point2[n-3])) > 0:
                        flag1 = sub1_po_set
                    else:
                        print('程序错误点位于线上')
                else:
                    if PointDisLine(sub1_neg_set[0], base_line1) * PointDisLine(sub1_neg_set[0], GetLine(cvxhu_point2[n-2], cvxhu_point2[n-3])) < 0:
                        flag1 = sub1_neg_set
                    else:
                        break
            else:
                if len(sub1_po_set):
                    if PointDisLine(sub1_po_set[0], base_line1) * PointDisLine(sub1_po_set[0], GetLine(cvxhu_point2[n-2], cvxhu_point2[n-3])) < 0:
                        flag1 = sub1_po_set
                    else:
                        break
                else:
                    print(sub1_neg_set, 'what', sub1_po_set)

        else:
            cvxhu_point2.append(flag1[0])
            break
        CvxVis(point_set, cvxhu_point2, cvxhu_point2[n-3], fir_point)
    
    return list(set(cvxhu_point1 + cvxhu_point2))
 
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
    def SortList(elem):
        """
        对列表进行排序
        """
        return elem[0]
    for each in cvxhu_point:
        if each[1] > 0:
            a.append(each)
        else:
            b.append(each)
    a.sort(key = SortList)
    b.sort(key = SortList, reverse = True )
    cvxhu_point = a + b
    cvxhu_point.append(a[0])
    for i in range(len(point_set)):
        p_x.append(point_set[i][0])
        p_y.append(point_set[i][1])
    for i in range(len(cvxhu_point)):
        c_x.append(cvxhu_point[i][0])
        c_y.append(cvxhu_point[i][1])

    plt.scatter(p_x, p_y, c = 'r', marker = 'x')
    plt.scatter(c_x, c_y, c = 'r')
    plt.plot(c_x, c_y, c = 'b')
    plt.plot([point1[0], point2[0]], [point1[1], point2[1]],  c = 'g')
    plt.show()

def main():
    
    a = GenerScatter(10)
    # 生成10个散点
    dis = {}
    cvxhu_point = []
    for each in a:
        dis[each] = each[0] * each[0] + each[1] * each[1]
    print(dis)
    sorted_dis=sorted(dis.items(),key=operator.itemgetter(1), reverse = True)
    # 找出离原点最远的两个点
    print(sorted_dis)
    for i in range(2):
        cvxhu_point.append(sorted_dis[i][0])
    first_line = GetLine(sorted_dis[0][0], sorted_dis[1][0])
    po_set, neg_set = PointDivison(a, first_line, cvxhu_point)
    print('正点集:', po_set, '负点集:', neg_set)
    # 分别搜索正负点集中的凸包点
    cvxhu_po = copy.copy(cvxhu_point)
    po_hu = CvxSearch(po_set, cvxhu_po)
    cvxhu_neg = copy.copy(cvxhu_point)
    neg_hu = CvxSearch(neg_set, cvxhu_neg)
    # 合并两个凸包点集合
    cvxhu_point = list(set(po_hu + neg_hu))
    print(cvxhu_point)
    CvxVis(a, cvxhu_point, sorted_dis[0][0], sorted_dis[1][0])       



if __name__ == "__main__":
    main()
