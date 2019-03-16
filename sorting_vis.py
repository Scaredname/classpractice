#！python
#code = utf-8

"""
排序算法的可视化分析
Author:MokeyDChaos
Date:2019-03-16
Version:2.0
"""
import random
import matplotlib.pyplot as plt
import time

def ShellSort(input_array):
    """
    对数组进行希尔排序
    @input_array:输入数组
    """ 
    Length = len(input_array)
    delt = [3,2,1]
    temp = 0
    k = 0
    for each in delt:
        for i in range(each):
            for j in range(i + each, Length, each):
                if input_array[j] < input_array[j - each]:
                    temp = input_array[j]
                    for k in range( j - each, -2*each, -each):
                        # 这里把c语言的for语句改过来的时候出现了问题，for是先执行语句再改变循环值再判断，range是直接得到所有符合规则的循环值 
                        if temp < input_array[k]:
                            input_array[k + each] = input_array[k]
                        else:
                            break
                    input_array[k + each] = temp
        

def MergeSort(input_array):
    """
    对数组进行归并排序
    """

def QuickSort(input_array):
    """
    对数组进行快速排序
    @input_array:输入数组
    """
    Length = len(input_array)
    def sort(array, low, high):
        """
        从前后两边开始进行快速排序
        @array:输入数组
        @low:小数的下标
        @high:大数的下标
        """
        temp = 0
        pivot = array[low]
        while low < high:
            while low < high and array[high] >= pivot:
                high -= 1 
            temp = array[low]
            array[low] = array[high]
            array[high] = temp
            while low < high and array[low] <= pivot:
                low += 1
            temp = array[low]
            array[low] = array[high]
            array[high] = temp
        return low

    def qusort(array, n, low, high):
        """
        递归调用对函数进行快速排序
        @n:数组长度
        """
        if low < high:
            pivot = sort(array, low, high)
            qusort(array, n, low, pivot - 1)
            qusort(array, n, pivot + 1, high)

    qusort(input_array, Length, 0, Length - 1)

def BubbleSort(input_array):
    """
    对一个数组进行冒泡排序
    @input_array:进行排列的数组
    @return：升序排列的数组
    """
    Length = len(input_array)

    for i in range(1, Length):
        for j in range(0, Length - i):
            if input_array[j] > input_array[j + 1]:
                input_array[j], input_array[j + 1] = input_array[j + 1], input_array[j]
            # visual(Length, input_array, i, j)
            
def visual(L, array, i, j):
    """
    可视化冒泡排序过程
    @L:数组长度
    @array:输入数组
    @i:第几轮比较，用于图片的命名
    @j:在作比较的数组元素下标
"""
    plt.bar(range(L), array)
    z = 0
    for x,y in zip(range(L), array):
        font = 10
        num_color = 'g'
        if z == j or z == j + 1:
            font = 15
            num_color = 'r'
        plt.text(x, y + 0.5, y, ha = 'center', va = 'top', fontsize = font, color = num_color)
        z += 1 
    plt.savefig('D:/Study/研一/高级数据结构/gif/sorting%s-%s'%(i,j))
    plt.clf()

def time_vis(func):
    """
    将不同规模下所需要的排序时间绘制为散点图
    @func:输入进来的函数；格式为func（input_array)
    """
    N = 1000 
    n = list(range(N))
    t = []
    for i in range(N):
        data = list(range(3 * n[i] ))
        data = random.sample(data, k = 3 * n[i])
        # print(data)
        time_start = time.time()
        func(data)
        time_end = time.time()
        t.append(time_end - time_start)
    print(t)
    plt.plot(range(N), t)
    plt.show()


def main():
    
    # data = list(range(1000))
    # data = random.sample(data, k = 1000)
    # print(data)
    # time_start = time.time()
    # ShellSort(data)
    # time_end = time.time()
    # print(data)
    # print(time_end - time_start)
    time_vis(ShellSort)

if __name__ == "__main__":
    main()
