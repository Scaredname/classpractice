#！python
#code = utf-8

"""
排序算法的可视化分析
Author:MokeyDChaos
Date:2019-03-03
Version:1.0
"""
import random
import matplotlib.pyplot as plt
import time

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

def time_vis():
    """
    将不同规模下所需要的排序时间绘制为散点图
    """
    N = 1000 
    n = list(range(N))
    t = []
    for i in range(N):
        data = list(range(2 * n[i] ))
        data = random.sample(data, k = 2 * n[i])
        # print(data)
        time_start = time.time()
        BubbleSort(data)
        time_end = time.time()
        t.append(time_end - time_start)
    print(t)
    plt.plot(range(N), t)
    plt.show()


def main():
    
    # data = list(range(100))
    # data = random.sample(data, k = 100)
    # print(data)
    # time_start = time.time()
    # BubbleSort(data)
    # time_end = time.time()
    # print(data)
    # print(time_end - time_start)
    time_vis()

if __name__ == "__main__":
    main()
