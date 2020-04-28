import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import datetime
import numpy as np

# Import PySwarms
import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx

def return_day_list(start_time, end_time):
    # string --> date
    str_date_start = datetime.datetime.strptime(start_time,'%Y-%m-%d').date()
    str_date_end = datetime.datetime.strptime(end_time,'%Y-%m-%d').date()
    delta = (str_date_end - str_date_start).days

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

def optimization(a,b, c_0, f_0): #, y_real
    from sklearn import metrics
    def move(P, steps, sets, t):
        a, b = sets
        c, f = P
        dc = math.exp(a * t + b) * c * f
        df = -math.exp(a * t + b) * c * f
        return [c + dc * steps, f + df * steps]

    sets = [a, b]

    # 多少个数
    T = int(window)
    t_change = 1
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
    for yy in range(T + 1):
        y_pred.append(y_pred_pre[yy])
    y_pred = np.array(y_pred)
    y_real_opt = [i * all_0 for i in y_real]
    opt_result = 1 - metrics.r2_score(y_real, y_pred,sample_weight=[w ** (len(y_pred) - i) for i in list(range(len(y_pred)))])
    # print(1-opt_result)
    return opt_result

def deviation(x, c_0, f_0):
    op=list()
    for i in range(len(x[:, 0])):
        a=x[:, 0][i]
        b=x[:, 1][i]
        op.append(optimization(a,b, c_0, f_0))
    return op

def optimizationfig(a, b, y_real, c_0, f_0):
    def move(P, steps, sets, t):
        a, b = sets
        c, f = P
        dc = math.exp(a*t+b)*c*f
        df = -math.exp(a*t+b)*c*f
        return [c+dc*steps, f+df*steps]
    sets = [a, b]
    # 多预测5天
    T= int(window)+day_plus
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

def final_result(y_real, c_0, f_0):
    opt_result, [a_best,b_best] = optimizer.optimize(deviation, c_0=c_00, f_0=f_00, iters=2000)
    txt_ab_best = open(f'分开最佳ab结果-{title}-{except_day}.txt', 'a+')
    txt_ab_best.write(f"{start_day}, {a_best}, {b_best}, {opt_result}")
    txt_ab_best.write('\n')
    txt_ab_best.close()
    y_best_pre = optimizationfig(a_best, b_best, y_real, c_0, f_0)[0].tolist()
    y_best = [i * all_0 for i in y_best_pre]

    df_y = pd.DataFrame({'y_best_%s' % title: y_best, 'date': date_list_2})
    df_y.to_csv(f"分开最佳y结果-{title}-{start_day}-{except_day}.csv",index=0)

    # 作拟合图
    x1 = date_list_1
    x2 = date_list_2

    y1 = y_real_pre
    y2 = y_best

    fig = plt.figure()
    plt.plot(x2, y2, '--', color='firebrick', label='predict')
    plt.scatter(x1, y1, color='', marker='o', edgecolor='firebrick', linewidths=1, label='reality')

    plt.xlabel('time', fontsize=20)
    plt.ylabel('I', fontsize=20)
    plt.xticks(range(0, len(x2), 5), x2[::5], rotation=45)
    plt.title(title)
    plt.legend(fontsize=12)
    plt.savefig(f"{title}-{start_day}-{except_day}.png")

first_day = '2019-12-08'
except_day = '2020-04-07'
df_0 = pd.read_csv(f'country_confirmed_{except_day}.csv' )
day_plus = 63
except_day_plus = datetime.datetime.strptime(except_day,'%Y-%m-%d').date() + datetime.timedelta(days=day_plus)

# country_first_list=[('Italy','2020-01-30',60482200),('Korea, South','2020-01-20',51269185),('Germany','2020-01-27',82293457),('US','2020-01-21',326766748),('United Kingdom','2020-01-31',66573504),('Denmark','2020-02-27',5754356),
# ('Iran','2020-02-19',82011735),('Spain','2020-02-01',46397452),('France','2020-01-24',65233271),('Switzerland','2020-02-25',8544034),('Norway','2020-02-26',5353363),('Netherlands','2020-02-27',17084459),
# ('India','2020-01-30',1354051854),('Africa','2020-02-14',1340598000),('China','2019-12-08',1396984787)]

# country_first_list=[('Turkey','2020-03-11',82000000),('Belgium','2020-02-04',11422068),('Canada','2020-01-26',35151728),('Portugal','2020-03-02',10276617),('Japan','2020-01-22',124800000),('Austria','2020-02-25',9000000),('Australia','2020-01-26',22039500)]

country_first_list=[('Russia','2020-01-31',144500000),('Brazil','2020-02-26',209500000)]
w=0.3


# start_day = '2020-02-20'
#
# title = 'US'
# all_0 = 326766748

for title,start_day_o,all_0 in country_first_list:
    for day_add in range(0,36,5):
        start_day=str(datetime.datetime.strptime(start_day_o,'%Y-%m-%d').date() + datetime.timedelta(days=day_add))
        date_list_1 = return_day_list(start_day, except_day)
        date_list_2 = return_day_list(start_day, str(except_day_plus))
        y_real_pre = list(df_0[title][(datetime.datetime.strptime(start_day,'%Y-%m-%d').date()-datetime.datetime.strptime(first_day,'%Y-%m-%d').date()).days:])

        c_00 = y_real_pre[0]/all_0
        f_00 = (all_0-y_real_pre[0])/all_0

        f_real_pre = [all_0-i for i in y_real_pre]
        y_real = [i/all_0 for i in y_real_pre]
        window = len(y_real)-1

        # x_max =  np.zeros(2)
        # bounds = (-1 * np.ones(2), np.zeros(2))
        bounds = (np.array([-1,-1]), np.array([0,1]))
        options = {'c1': 0.5, 'c2': 0.3, 'w':0.8,'k':5,'p':30}

        # Call instance of PSO
        optimizer = ps.single.LocalBestPSO(n_particles=40, dimensions=2, options=options, bounds=bounds)

        # Perform optimization
        # cost, pos = optimizer.optimize(deviation, c_0=c_00, f_0=f_00, iters=1)
        # print(cost,pos)
        final_result(y_real, c_00, f_00)