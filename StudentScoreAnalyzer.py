"""学生成绩统计系统
熟悉学生成绩统计业务流程，能够熟练使用一种编程语言实现学生成绩统计的功能。功能需求如下：实现丰富的统计和分析功能，
能按照多种条件，对不同学校、年级、班级等进行对比分析，操作简便，适合学校、教师、培训机构等教学活动总结分析使用。
功能需求：
1. 支持学生成绩文件的导入。能方便的导入各个学生的单科考试成绩数据。学生成绩文件可以是纯文本文件。
2. 计算输出各个学生的各科总分、平均分、绩点、标准差和方差（此版本未实现）
3. 计算输出各班级各科最高分、最低分、平均分、优秀率、及格率、不及格率
4. 绘制相关统计分析图表（柱状图、饼状图）
"""
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from pandas import Series


def main() :
    print("输入文件类型 0为txt 1为csv")
    try:
        file_type = int(input())
    except ValueError:
        print("请输入有效的数字 (0 或 1)")
        return

    if file_type != 1:
        data = loadtxt()
    else:
        data = loadcsv()

    stucount = len(data)
    if stucount == 0:
        print("没有加载到数据")
        return


    calscore(data, stucount, file_type, max, "最高成绩")
    calscore(data, stucount, file_type, min, "最低成绩")
    calscore(data, stucount, file_type,lambda scores: sum(scores) / len(scores), "平均成绩")
    scselect(data,stucount,file_type)


def calscore(data, stucount, file_type, func, funcname):
    """
    Function:
        通用计算函数，根据文件类型遍历各次考试，调用 func 计算并输出结果
    注：重构后的高阶函数，提取出公共逻辑，通过 func 参数实现不同计算
    """
    if file_type == 1:
        for exam in range(len(data[0]) - 1):
            scores = [float(data[i][exam + 1]) for i in range(stucount)]
            res = func(scores)
            print(f"{exam}次考试{funcname}: {res}")
    else:
        scores = [float(data[i][0]) for i in range(stucount)]
        res = func(scores)
        print(f"{funcname}: {res}")


def scselect(data, stucount, file_type):
    """
    Function:
        根据文件类型统计各分数段人数，并输出统计表和图表
    """
    if file_type == 1:
        for exam in range(len(data[0]) - 1):
            level = sclevels(data, stucount, exam + 1)
            sctable(level, stucount)
            bar(level, stucount)
            pie(level)
    else:
        level = sclevels(data, stucount, 0)
        print(level)
        sctable(level, stucount)
        bar(level, stucount)
        pie(level)


def sclevels(data,stucount,exam) :
    """
    Function:
        统计指定列的各分数段人数（0-20, 21-40, 41-60, 61-80, 81-100）
    Returns:
        (level_a, level_b, level_c, level_d, level_e) - 各分数段人数元组
    """
    level_a = level_b = level_c = level_d = level_e = 0

    for i in range(stucount):
        score = float(data[i][exam])
        if score <= 20:
            level_a += 1
        elif score <= 40:
            level_b += 1
        elif score <= 60:
            level_c += 1
        elif score <= 80:
            level_d += 1
        else:
            level_e += 1

    return level_a, level_b, level_c, level_d, level_e


def sctable(level, stucount) :
    """
    Function:
        打印成绩等级统计表（优秀率、良好率、不及格率）
    """
    level_a, level_b, level_c, level_d, level_e = level
    excellent_rate = level_e / stucount * 100
    good_rate = level_d / stucount * 100
    fail_rate = (level_a + level_b + level_c) / stucount * 100

    print(f"{'成绩等级':<10} {'所占比例':<10}")
    print(f"{'优秀':<10} {excellent_rate:.2f}%")
    print(f"{'良好':<10} {good_rate:.2f}%")
    print(f"{'不及格':<10} {fail_rate:.2f}%")


def loadtxt():
    """
    Function:
        从txt文件加载成绩数据
    Returns:
        data - 学生成绩记录
    """
    data = []
    with open('2015score1.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                data.append(line.split())
    return data


def loadcsv():
    """
    Function:
        从csv文件加载成绩数据
    Returns:
        data - 学生成绩记录
    """
    data = []
    with open('2015score.csv', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                data.append(line.split(','))
    return data


def pie(level):
    """
    Function:
        绘制成绩分布饼状图
    """
    level_a, level_b, level_c, level_d, level_e = level

    plt.figure(figsize=(6, 9))
    labels = ['0-20', '21-40', '41-60', '61-80', '81-100']
    sizes = [level_a, level_b, level_c, level_d, level_e]
    colors = ['red', 'green', 'lightskyblue', 'yellow', 'pink']
    explode = (0, 0, 0, 0, 0.05)

    plt.pie(
        sizes,
        explode=explode,
        labels=labels,
        colors=colors,
        labeldistance=1.1,
        autopct='%3.1f%%',
        shadow=False,
        startangle=90,
        pctdistance=0.6
    )
    plt.axis('equal')
    plt.legend()
    plt.title('成绩分布饼状图')
    plt.show()


def bar(level, stucount):
    """
    Function:
        绘制成绩分布柱状图
    """
    level_a, level_b, level_c, level_d, level_e = level

    fig, axes = plt.subplots(1, 1)
    data_series = Series(
        [level_a, level_b, level_c, level_d, level_e],
        index=['0-20', '21-40', '41-60', '61-80', '81-100']
    )
    data_series.plot(kind='bar', ax=axes, color='k', alpha=0.7)
    axes.set_xlabel('成绩等级')
    axes.set_ylabel('人数')
    axes.set_title('成绩分布柱状图')
    plt.ylim((0, 2 * stucount / 3))
    plt.show()


if __name__ == '__main__':
    main()