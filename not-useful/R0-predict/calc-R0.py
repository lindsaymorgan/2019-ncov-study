import math
import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pandas as pd

def R0func(defi, susp, t):
    # defi是确诊人数；susp是疑似人数；t是疾病已爆发时间；设出现时间为2019-12-8

    # Tg_1和Tg_2为生成时间（generation period）
    Tg_1 = 8.4
    # Tg_2 = 10.0
    rho = 0.65 # 潜伏期占生成时间的比例
    # p为疑似病例转化为确诊病例的概率
    p = 0.695
    # yt为实际预估感染人数
    yt = susp * p + defi
    # lamda为早期指数增长的增长率
    day=(t-datetime.datetime(2019,12,8)).days
    lamda = math.log(yt) / day

    R0_1 = 1 + lamda * Tg_1 + rho * (1 - rho) * pow(lamda * Tg_1, 2)
    # R0_2 = 1 + lamda * Tg_2 + rho * (1 - rho) * pow(lamda * Tg_2, 2)

    return  R0_1

data=pd.read_csv('../increase-log/country-day-summary-with-outsuspect.csv')
data['updateTime'] = pd.to_datetime(data['updateTime'])
result=list()
for i in data.index:
    result.append(R0func(data['country_confirmedCount'][i],data['country_suspectedCount'][i],data['updateTime'][i]))

data['R0']=result
    
print(data)
data.to_csv('../increase-log/country-day-summary-with-outsuspect.csv',index=0)
# # N为人群总数
# N = 10000
# # β为传染率系数
# beta = 0.6
# # gamma为恢复率系数
# gamma = 0.1
# # Te为疾病潜伏期
# Te = 14
# # I_0为感染者的初始人数
# I_0 = 1
# # E_0为潜伏者的初始人数
# E_0 = 0
# # R_0为治愈者的初始人数
# R_0 = 0
# # S_0为易感者的初始人数
# S_0 = N - I_0 - E_0 - R_0
# # T为传播时间
# T = 150
#
# # INI为初始状态下的数组
# INI = (S_0,E_0,I_0,R_0)
#
#
# def funcSEIR(inivalue,_):
#     Y = np.zeros(4)
#     X = inivalue
#     # 易感个体变化
#     Y[0] = - (beta * X[0] * X[2]) / N
#     # 潜伏个体变化
#     Y[1] = (beta * X[0] * X[2]) / N - X[1] / Te
#     # 感染个体变化
#     Y[2] = X[1] / Te - gamma * X[2]
#     # 治愈个体变化
#     Y[3] = gamma * X[2]
#     return Y
#
# T_range = np.arange(0,T + 1)
#
# RES = spi.odeint(funcSEIR,INI,T_range)
#
#
# plt.plot(RES[:,0],color = 'darkblue',label = 'Susceptible',marker = '.')
# plt.plot(RES[:,1],color = 'orange',label = 'Exposed',marker = '.')
# plt.plot(RES[:,2],color = 'red',label = 'Infection',marker = '.')
# plt.plot(RES[:,3],color = 'green',label = 'Recovery',marker = '.')
#
# plt.title('SEIR Model')
# plt.legend()
# plt.xlabel('Day')
# plt.ylabel('Number')
plt.show()