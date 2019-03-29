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
    @point_set:坐标点
    @cvxhu_point:凸包点集合
    """
    # 一定要注意python中赋值、浅拷贝、深拷贝之间的区别呀
    print('1', point_set)
    flag = point_set
    print('f', flag)
    base_line = GetLine(line[0], line[1])
    fir_point = PointSearch(flag, base_line, cvxhu_point)
    for i in range(len(line)):
        print('lien', line)
        line_set = [line[i], fir_point]
        temp_line = GetLine(line[i], fir_point)
        print('temp_line', line[i], fir_point)
        # fir_point = PointSearch
        judge_line =  GetLine(line[1 - i], line[i])
        temp_flag = copy.copy(flag)
        # 最初的划分线
        print('before loop, t_f', temp_flag)
        print('before loop, t_c', cvxhu_point)
        while len(temp_flag) >= 1 :
            sub_po_set, sub_neg_set = PointDivison(temp_flag, temp_line, cvxhu_point)
            print('po:', sub_po_set, 'neg', sub_neg_set)
            CvxVis(temp_flag, cvxhu_point, fir_point, line[i])
            # 使用距离之间是否同号来判断点在哪一侧,一点注意让两个向量是首尾相连
            if len(sub_neg_set):
                if len(sub_po_set):
                    print('sub_neg_set[0]', sub_neg_set[0], 'pdis1', PointDisLine(sub_neg_set[0], temp_line), \
                        'pdis2', PointDisLine(sub_neg_set[0], judge_line))
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
                print('递归前的t_c', cvxhu_point)
                print('递归前的t_flag', temp_flag)
                CvxSearchSm(temp_flag, cvxhu_point, line_set)
                # 我也不知道为什么递归后temp_flag总是会还有值，那这里我们直接将递归后的flag赋值为空集
                print('递归后的t_c', cvxhu_point)
                print('递归后的t_flag', temp_flag)
                # 递归后我们只需要一个为空的temp_flag
                if len(list(set(cvxhu_point).intersection(flag))):
                    temp_flag = []
                print('赋值后的t_flag', temp_flag)
                print('递归后的cv', cvxhu_point)
            if len(temp_flag) == 1:
                cvxhu_point.append(temp_flag[0])
                temp_flag = []
            print('出t_flag:', temp_flag)
            print('出t_c:', cvxhu_point)
    print('con_p',list(set(cvxhu_point)))
    CvxVis(point_set, list(set(cvxhu_point)))

def CvxSearchtry(point_set, point_set1, cvxhu_point, cvxhu_point1, line):
    """
    在点集中寻找凸包点
    @point_set:坐标点
    @cvxhu_point:凸包点集合
    """
    # 一定要注意python中赋值、浅拷贝、深拷贝之间的区别呀
    print('1', point_set)
    flag = point_set
    flag1 = point_set1
    print('f', flag)
    print('f1', flag1)
    base_line = line
    for i in range(2):
        if i == 0:
            temp_flag = flag
            temp_cvxhu = cvxhu_point
            Length = len(temp_cvxhu)
            num = 1
        else:
            temp_flag = flag1
            temp_cvxhu = cvxhu_point1
            Length = len(temp_cvxhu)
            num = -1
        # 最初的划分线
        print('before loop, t_f', temp_flag)
        print('before loop, t_c', temp_cvxhu)
        while len(temp_flag) >= 1 :
            Length = len(temp_cvxhu)
            if len(temp_flag) != 1:
                fir_point = PointSearch(temp_flag, base_line, temp_cvxhu)
                if num == -1:
                    base_line = GetLine(temp_cvxhu[Length - 2], fir_point)
                    print('baseline', temp_cvxhu[Length - 2], fir_point)
                    judge_line = GetLine(temp_cvxhu[Length-1], temp_cvxhu[Length-2])
                    print('ju_line', temp_cvxhu[Length-1], temp_cvxhu[Length-2])
                else:
                    base_line = GetLine(temp_cvxhu[Length - 1], fir_point)
                    print('baseline', temp_cvxhu[Length - 1], fir_point)
                    judge_line = GetLine(temp_cvxhu[Length-2], temp_cvxhu[Length-1])
                    print('ju_line', temp_cvxhu[Length-2], temp_cvxhu[Length-1])
                sub_po_set, sub_neg_set = PointDivison(temp_flag, base_line, temp_cvxhu)
                print('po:', sub_po_set, 'neg', sub_neg_set)
                if num == -1:
                    CvxVis(temp_flag, temp_cvxhu, fir_point, temp_cvxhu[Length - 2])
                else:
                    CvxVis(temp_flag, temp_cvxhu, fir_point, temp_cvxhu[Length - 1])
                # 使用距离之间是否同号来判断点在哪一侧,一点注意让两个向量是首尾相连
                if len(sub_neg_set):
                    if len(sub_po_set):
                        print('sub_neg_set[0]', sub_neg_set[0], 'pdis1', PointDisLine(sub_neg_set[0], base_line), 'twopoint', temp_cvxhu[Length-1], temp_cvxhu[Length-2],\
                            'pdis2', PointDisLine(sub_neg_set[0], judge_line), 't_cv', temp_cvxhu)
                        # 使用距离的乘积的正负来判断哪一个点集是我们需要的
                        if PointDisLine(sub_neg_set[0], base_line) * PointDisLine(sub_neg_set[0], judge_line)  > 0:
                            temp_flag = sub_po_set
                        elif PointDisLine(sub_neg_set[0], base_line) * PointDisLine(sub_neg_set[0], judge_line)  < 0:
                            temp_flag = sub_neg_set
                        else:
                            print('程序错误点位于线上')
                    else:
                        if PointDisLine(sub_neg_set[0], base_line) * PointDisLine(sub_neg_set[0], judge_line)  < 0:
                            temp_flag = sub_neg_set
                        else:
                            temp_flag = []
                else:
                    if len(sub_po_set):
                        if PointDisLine(sub_po_set[0], base_line) * PointDisLine(sub_po_set[0], judge_line)  < 0:
                            temp_flag = sub_po_set
                        else:
                            temp_flag = []
                    else:
                        temp_flag = []
                print(num, '出t_flag:', temp_flag)
                print(num, '出t_c:', temp_cvxhu)
                # 这里因为flag的赋值不是实时受temp控制，所以加入判断防止错误点进入凸包集
                if len(temp_flag) == 0 and len(flag1) == 1 and len(flag) == 1:
                    flag = []
                    flag1 = []
                print(num, 'f1:', flag1)
                print(num, 'f:', flag)
                if len(temp_flag) > 1:
                    print('开始递归')
                    print('递归前的t_c', temp_cvxhu)
                    print('递归前的t_flag', temp_flag)
                    print('递归前的flag', flag)
                    print('递归前的flag1', flag1)
                    print('递归前的cv', cvxhu_point)
                    print('递归前的cv2', cvxhu_point1)
                    CvxSearchtry(temp_flag, temp_flag, temp_cvxhu, temp_cvxhu, base_line)
                    # 我也不知道为什么递归后temp_flag总是会还有值，那这里我们直接将递归后的flag赋值为空集
                    print('递归后的t_c', temp_cvxhu)
                    print('递归后的t_flag', temp_flag)
                    # 递归后我们只需要一个为空的temp_flag
                    if num == 1 and len(list(set(cvxhu_point).intersection(flag))):
                        flag = []
                        temp_flag = []
                    elif num == -1 and len(list(set(cvxhu_point1).intersection(flag1))):
                        flag1 = []
                        temp_flag = []
                    print('赋值后的t_flag', temp_flag)
                    print('递归后的flag', flag)
                    print('递归后的flag1', flag1)
                    print('递归后的cv', cvxhu_point)
                    print('递归后的cv2', cvxhu_point1) 
            else:
                temp_cvxhu.append(temp_flag[0])
                break
    print('con_p',list(set(cvxhu_point + cvxhu_point1)))
    CvxVis(point_set, list(set(cvxhu_point + cvxhu_point1)))


def CvxSearch(point_set, point_set1, cvxhu_point1, cvxhu_point2):
    """
    在点集中寻找凸包点
    @point_set:坐标点
    @cvxhu_point:凸包点集合
    """
    # 一定要注意python中赋值、浅拷贝、深拷贝之间的区别呀
    flag = point_set
    
    # cvxhu_point1 = copy.copy(cvxhu_point)
    # cvxhu_point2 = copy.copy(cvxhu_point)
    Length = len(cvxhu_point1)
    # 最初的划分线
    base_line = GetLine(cvxhu_point1[Length-1], cvxhu_point1[Length-2])
    #感觉需要递归一下
    while len(flag) > 0 :
        # while 不循环了不知道咋回事
        print('flag:', flag)
        if len(flag) != 1:
            fir_point = PointSearch(flag, base_line, cvxhu_point1)
            n = len(cvxhu_point1)
            base_line = GetLine(cvxhu_point1[n-2], cvxhu_point1[n-1])
            print('cv1-in0:', cvxhu_point1, 'fir:', fir_point, 'cvxhu_point', cvxhu_point1[n-2])
            print('b_line', base_line)
            sub_po_set, sub_neg_set = PointDivison(flag, base_line, cvxhu_point1)
            print('po:', sub_po_set, 'neg', sub_neg_set)
            CvxVis(flag, cvxhu_point1, fir_point, cvxhu_point1[n-2])
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
                        flag = []
            else:
                if len(sub_po_set):
                    if PointDisLine(sub_po_set[0], base_line) * PointDisLine(sub_po_set[0], GetLine(cvxhu_point1[n-2], cvxhu_point1[n-3])) > 0:
                        flag = sub_po_set
                    else:
                        flag = []
                else:
                    flag = [] 
        else:
            cvxhu_point1.append(flag[0])
            print('add')
            break
        # CvxVis(point_set, cvxhu_point1, cvxhu_point1[n-2], fir_point)
        # 递归函数和人类的思维不一样，每次递归都要执行完所有的语句，所以当递归结束后还会将之前因为递归语句而无法执行的语句再次执行一遍。
        print('当前的flag', flag)
        point_set = flag
        print('当前的pos', point_set)
        if len(flag) > 1:
            print('1开始递归')
            print('递归前的flag', flag)
            point_set1 = copy.copy(flag)
            # cvxhu_point2 = cvxhu_point1
            print('递归前的pos1', point_set1)
            cvxhu_point1 = CvxSearch(flag, point_set1, cvxhu_point1, cvxhu_point2)
            # 现在问题集中在递归后得到的flag和pos1的值和我们预期得到的值不符，并且不知道哪里出问题了。
            print('递归后的cv1', cvxhu_point1)
            print('递归后的flag', flag) 
            print('递归后的pos1', point_set1)
            # 递归后的flag不对,原因又出在了python这个赋值上，我们是需要使用赋值来通过递归更新我们的flag
            # 这里我考虑加个值来控制递归，解决一下flag的问题
        else:
            pass
    print('跳出循环的flag', flag)
    print('跳出循环的pos', point_set) 
    print('cv1_out', cvxhu_point1)
    print('cv2_in', cvxhu_point2)
    
    # 向另一个方向寻找
    # 这里出现新的问题，我们只有第一次是和间隔一个点的点相连，之后都是和上一个点相连
    # 想了一下决定使用一个笨办法，加一个记录循环次数的数字，再进行判断   
    flag1 = point_set1
    Length1 = len(cvxhu_point2)
    base_line1 = GetLine(cvxhu_point2[Length1-1], cvxhu_point2[Length1-2])
    while len(flag1) > 0:
        print('flag1:', flag1)
        if len(flag1) != 1:
            num = 1
            fir_point = PointSearch(flag1, base_line1, cvxhu_point2)
            n = len(cvxhu_point2)
            # 笨办法
            if num == 1:
                # 当进入递归后，有可能是需要跳过第一步。
                base_line1 = GetLine(cvxhu_point2[n-3], cvxhu_point2[n-1])
                print('cv2-in0:', cvxhu_point2, 'fir:', fir_point, 'cvxhu_point2', cvxhu_point2[n-3])
            else:
                base_line1 = GetLine(cvxhu_point2[n-2], cvxhu_point2[n-1])
                print('cv2-in0:', cvxhu_point2, 'fir:', fir_point, 'cvxhu_point2', cvxhu_point2[n-2])
            sub1_po_set, sub1_neg_set = PointDivison(flag1, base_line1, cvxhu_point2)
            print('po2:', sub1_po_set, 'neg2', sub1_neg_set)
            if num == 1:
                CvxVis(flag1, cvxhu_point2, fir_point, cvxhu_point2[n-3])
            else:
                CvxVis(flag1, cvxhu_point2, fir_point, cvxhu_point2[n-2])
            num += 1
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
                        flag1 = []
            else:
                if len(sub1_po_set):
                    if PointDisLine(sub1_po_set[0], base_line1) * PointDisLine(sub1_po_set[0], GetLine(cvxhu_point2[n-2], cvxhu_point2[n-3])) < 0:
                        flag1 = sub1_po_set
                    else:
                        flag1 = []
                else:
                    flag1 = []

        else:
            cvxhu_point2.append(flag1[0])
            break
        # if num == 1:
        #     CvxVis(point_set, cvxhu_point2, cvxhu_point2[n-3], fir_point)
        # else:
        #     CvxVis(point_set, cvxhu_point2, cvxhu_point2[n-2], fir_point)
        print('当前的flag1', flag1)
        point_set1 = flag1
        print('当前的pos1', point_set1)
        if len(flag1) > 1:
            print('2开始递归')
            print('递归前的flag1', flag1)
            point_set = copy.copy(flag1)
            # cvxhu_point1 = cvxhu_point2
            print('递归前的pos', point_set)
            # 这里我们再加一个
            cvxhu_point2 = CvxSearch(point_set, flag1, cvxhu_point1, cvxhu_point2)
            print('递归后的cv2', cvxhu_point2)
            print('递归后的flag1', flag1)
            print('递归后的pos', point_set)
        else:
            pass           
    print('跳出循环的flag1', flag1)
    print('跳出循环的pos1', point_set1)
    print('cv2_out', cvxhu_point2)

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
    
    a = GenerScatter(10)
    # 生成10个散点
    dis = {}
    cvxhu_point = []
    for each in a:
        dis[each] = each[0] * each[0] + each[1] * each[1]
    print(dis)
    # sorted_dis=sorted(dis.items(),key=operator.itemgetter(1), reverse = True)
    # 找出离原点最远的两个点
    def SortList(elem):
        """
        对列表进行排序
        """
        return elem[0]
    # print(sorted_dis)
    # for i in range(2):
    #     cvxhu_point.append(sorted_dis[i][0])
    # first_line = GetLine(sorted_dis[0][0], sorted_dis[1][0])
    a.sort(key = SortList)
    cvxhu_point = [a[0], a[len(a)-1]]
    first_line = GetLine(a[0], a[len(a)-1])
    po_set, neg_set = PointDivison(a, first_line, cvxhu_point)
    print('正点集:', po_set, '负点集:', neg_set)
    b = [(-90, -95), (-15, -28), (23, -72), (41, -90), (73, 34), (85, -31)]
    b_c = [(-97, -95), (91, 73)]
    b1 = copy.copy(b)
    b_c1 = copy.copy(b_c)
    cvxhu_po = copy.copy(cvxhu_point)
    po_set1 = copy.copy(po_set)
    # CvxSearchtry(po_set, po_set1, cvxhu_po)
    cvxhu_neg = copy.copy(cvxhu_point)
    neg_set1= copy.copy(neg_set)
    # CvxSearchtry(neg_set, neg_set1, cvxhu_neg)
    # 分别搜索正负点集中的凸包点
    cvxhu_po1 = copy.copy(cvxhu_point)
    cvxhu_neg1 = copy.copy(cvxhu_point)
    # po_hu = CvxSearch(po_set, po_set1, cvxhu_po, cvxhu_neg)
    # print('开始负点集')
    # neg_hu = CvxSearch(neg_set, neg_set1, cvxhu_po1, cvxhu_neg1)
    # CvxSearchtry(po_set, po_set1, cvxhu_po, cvxhu_neg)
    # CvxSearchtry(neg_set, neg_set1, cvxhu_po1, cvxhu_neg1)
    # CvxSearchtry(b, b1, b_c, b_c1, GetLine(b_c[0], b_c[1]))
    CvxSearchSm(po_set, cvxhu_po, cvxhu_po1)
    CvxSearchSm(neg_set, cvxhu_neg, cvxhu_neg1)
    # CvxSearchSm(b, b_c, b_c1)
    # 合并两个凸包点集合
    cvxhu_point = list(set(cvxhu_po + cvxhu_neg))
    print(cvxhu_point)
    CvxVis(a, cvxhu_point)       



if __name__ == "__main__":
    main()
