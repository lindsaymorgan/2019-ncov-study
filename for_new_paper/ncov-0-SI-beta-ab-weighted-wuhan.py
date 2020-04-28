import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import datetime

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']



# 不包含end_time
def return_day_list(start_time, end_time):
    # string --> date
    str_date_start = datetime.datetime.strptime(start_time,'%Y-%m-%d').date()
    str_date_end = datetime.datetime.strptime(end_time,'%Y-%m-%d').date()
    delta = (str_date_end - str_date_start).days
    print(delta)

    m=str_date_start.month
    d=str_date_start.day
    date_start='%d-%d' % (m, d)

    list_days = [date_start]
    for day in range(1, delta):
        date = str_date_start + datetime.timedelta(days=day)
        #print(date)
        m=date.month
        d=date.day
        date1='%d-%d' % (m, d)
        list_days.append(date1)
    return list_days

# 用于优化结果
def optimization(a, b, y_real, c_0, f_0):
    import numpy as np
    from scipy.integrate import odeint
    from sklearn import metrics
    def move(P, steps, sets, t):
        a, b = sets
        c, f = P
        dc = math.exp(a*t+b)*c*f
        df = -math.exp(a*t+b)*c*f
        return [c+dc*steps, f+df*steps]
    sets = [a, b]
    
    # 多少个数
    T= int(num * window / aaa)
    t_change=1
    t = np.arange(0, T, t_change)

    P0 = [c_0, f_0]
    P = P0
    d = [P0]
    for v in t:
        P = move(P, 1, sets, v)
        d.append(P)
    dnp = np.array(d)
    y_pred_pre = dnp[:, 0]
    y_pred = []
    for yy in range(0, T+1, num):
        y_pred.append(y_pred_pre[yy])
    y_pred = np.array(y_pred)
    #print(y_pred)
    y_real_opt = [i*all_0 for i in y_real]
    y_real_opt = [i*all_0 for i in y_real]
    opt_result = 1-metrics.r2_score(y_real, y_pred, sample_weight=[w**(len(y_pred)-i) for i in list(range(len(y_pred)))])
    #print(1-opt_result)
    return opt_result

# 用于作图
def optimizationfig(a, b, y_real, c_0, f_0):
    import numpy as np
    from scipy.integrate import odeint
    from sklearn import metrics
    def move(P, steps, sets, t):
        a, b = sets
        c, f = P
        dc = math.exp(a*t+b)*c*f
        df = -math.exp(a*t+b)*c*f
        return [c+dc*steps, f+df*steps]
    sets = [a, b]
    # 多预测5天
    T= int(num * window / aaa)+day_plus
    t_change=1
    t = np.arange(0, T, t_change)
    P0 = [c_0, f_0]
    P = P0
    d = [P0]
    for v in t:
        P = move(P, 1, sets, v)
        d.append(P)
    dnp = np.array(d)
    y_pred_pre = dnp[:, 0]
    f_pred_pre = dnp[:, 1]
    return y_pred_pre, f_pred_pre

def neighbor(a_0, b_0, L_0, y_real, c_0, f_0):
    #print("本次初始解")
    #print(beta_0, miu_0, L_0)
    opt_0 = optimization(a_0, b_0, y_real, c_0, f_0)
    #print("本次误差")
    #print(opt_0)
    for (a, b) in [(a_0+L_0, b_0), (a_0-L_0, b_0), (a_0, b_0+L_0), (a_0, b_0-L_0)]:
        print(a, b)
        if (math.exp(a*window+b)<1):
            opt_try = optimization(a, b, y_real, c_0, f_0)
            #print("邻居")
            #print(beta, miu)
            #print("邻居的误差")
            #print(opt_try)
            if opt_try < opt_0:
                return (a, b)
    return (a_0, b_0)

def return_result(a_0, b_0, L_0, delta, lamda, y_real, c_0, f_0):
    list_result = [a_0, b_0]
    for n in range(xunhuan):
        #print("循环次数")
        #print(n)
        a, b = neighbor(a_0, b_0, L_0, y_real, c_0, f_0)
        if (a, b) == (a_0, b_0):
            L_0 = L_0 * lamda
        else:
            list_result.append((a, b))
            a_0, b_0 = a, b
            L_0 = L_0 * delta
        opt_result = optimization(a_0, b_0, y_real, c_0, f_0)
        if opt_result < 0.001:
            break   
    # 优解的个数
    len_result = len(list_result)
    print("可行解个数")
    print(len_result)
    return a_0, b_0, opt_result

def final_result(y_real, c_0, f_0):
    
    a_best, b_best, opt_result = return_result(a_0, b_0, L_0, delta, lamda, y_real, c_0, f_0)
    print("最优解")
    print(a_best, b_best, opt_result)
    txt_ab_best = open(f'分开最佳ab结果-{title}-{start_day}-{except_day}.txt', 'w')
    txt_ab_best.write("%s, %s, %s" % (a_best, b_best, opt_result))
    txt_ab_best.close()
    y_best_pre, f_best_pre = optimizationfig(a_best, b_best, y_real, c_0, f_0)[0].tolist(), optimizationfig(a_best, b_best, y_real, c_0, f_0)[1].tolist()
    y_best = [i*all_0 for i in y_best_pre]
    f_best = [i*all_0 for i in f_best_pre]
    print(y_best)
    df_y = pd.DataFrame({'y_best_%s' % title: y_best, 'date' : date_list_2})
    df_y.to_excel(f"分开最佳y结果-{title}-{start_day}-{except_day}.xlsx")
    
    # 作拟合图
    RMSE = round(opt_result, 4)
    #x1 = list(range(len(y_real)))
    #x2 = [float(i)/num for i in range(len(y_best_pre))]
    x1 = date_list_1
    x2 = date_list_2
    print(len(x2))
    y1 = y_real_pre
    y2 = y_best
    print(len(y2))
    fig = plt.figure()
    plt.plot(x2, y2, '--', color='firebrick', label='预测值')
    plt.scatter(x1, y1, color='', marker='o', edgecolor='firebrick', linewidths=1, label='实际值')
    #.title("RMSE=%s β=%s μ=%s" % (RMSE, round(beta_best, 4), round(miu_best, 4)))
    plt.xlabel('time', fontsize=20)
    plt.ylabel('I', fontsize=20)
    plt.xticks(range(0,len(x2),5),x2[::5],rotation=45)
    plt.title(title)
    plt.legend(fontsize=12)
    #plt.show()
    plt.savefig(f"{title}-{start_day}-{except_day}.png")

country_first_list=[('Italy','2020-01-30',60482200),('Korea, South','2020-01-20',51269185),('Germany','2020-01-27',82293457),('US','2020-01-21',326766748),('United Kingdom','2020-01-31',66573504),('Denmark','2020-02-27',5754356),
('Iran','2020-02-19',82011735),('Spain','2020-02-01',46397452),('France','2020-01-24',65233271),('Switzerland','2020-02-25',8544034),('Norway','2020-02-26',5353363),('Netherlands','2020-02-27',17084459),
('India','2020-01-30',1354051854),('Africa','2020-02-14',1340598000),('China','2019-12-08',1396984787)]

first_day = '2019-12-08'
start_day = '2020-02-20'
except_day = '2020-04-07'
df_0 = pd.read_csv(f'country_confirmed_{except_day}.csv' )
day_plus = 63
w=0.3
except_day_plus = datetime.datetime.strptime(except_day,'%Y-%m-%d').date() + datetime.timedelta(days=day_plus)
date_list_1 = return_day_list(start_day, except_day)
date_list_2 = return_day_list(start_day, str(except_day_plus))


title = 'US'
all_0 = 326766748


y_real_pre = list(df_0[title][(datetime.datetime.strptime(start_day,'%Y-%m-%d').date()-datetime.datetime.strptime(first_day,'%Y-%m-%d').date()).days:])
# 初始拥堵畅通边
c_00 = y_real_pre[0]/all_0
f_00 = (all_0-y_real_pre[0])/all_0
#beta_0确诊率；miu_0恢复率；L_0两个概率的变化
# a_0, b_0, L_0, delta, lamda = -0.1388738522162562, -0.3580373468075008, 0.01, 1.5, 0.5
a_0, b_0, L_0, delta, lamda = -0.05733708259534795,-0.2968835324687563, 0.01, 1.5, 0.5
xunhuan = 10000
f_real_pre = [all_0-i for i in y_real_pre]
y_real = [i/all_0 for i in y_real_pre]
window = len(y_real)-1
num=1
aaa = 1
print("初始初始误差")
print(optimization(a_0, b_0, y_real, c_00, f_00))

final_result(y_real, c_00, f_00)

