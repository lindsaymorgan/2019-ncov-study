import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

today=datetime.date(2020,3,1)


def show_hist():
    data = []
    with open(f'../../new-data-source/agged-record-data/city-confirmed-pivot-day-summary-{today}.csv', encoding='utf-8',newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            #print(row)
            #print("-------------------------------")
            data.append(row)

    data_recovered = []
    with open(f'../../new-data-source/agged-record-data/city-D-pivot-day-summary-{today}.csv', encoding='utf-8',newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            #print(row)
            #print("-------------------------------")
            data_recovered.append(row)

    print(len(data), len(data_recovered))



    tau_vec = []
    p0_vec = []


    for row_idx in range(len(data[1:])):
        row = data[1:][row_idx]
        row_r = data_recovered[1:][row_idx]
        splited = row[0].split(',')
        splited_r = row_r[0].split(',')
        #print(splited)
        #print(splited_r)


        for jj in range(len(splited)):
            if len(splited[jj]) != 0:
                idx = jj
                break

        print(splited[-9])
        if splited[-9]=='西安' or splited[-10]=='' or float(splited[-10]) < 50:
            continue
        a = [float(s) for s in splited[idx:-9] ]
        r = [float(s) for s in splited_r[-(4+len(a)):-4] ]

        #print(a,r, len(a), len(r))

        b = []
        time = []
       # print('---------------------------')


        l = 4
        for i in range(1+ l -1, len(a)):
            if a[i - l] - r[i - l] == 0:
                continue
            b.append((a[i] - a[i - 1]) / (a[i - l] - r[i - l]))
            time.append(i)
        #time = [qq for qq in range(len(b))]



        new_x2 = []
        new_y2 = []
        for w in range(len(b)):
            if b[w]  > 0:
                new_x2.append(time[w])
                new_y2.append(b[w])



        yy = np.log10(new_y2[6:])
        xx = new_x2[6:]

        p0 = np.mean(new_y2[:6])
        if p0 < 5:
            p0_vec.append(p0)


        m, bb = np.polyfit(xx,yy,1)
        tau = -1/m
        if tau > 0 and tau < 50:
            tau_vec.append(tau)




    plt.figure()
    plt.hist(tau_vec, bins = 18, color = cm.cool(0.75))
    plt.tick_params(labelsize=25)
    plt.ylabel(r'Number of cities', fontsize=25)
    plt.xlabel(r'$\tau$', fontsize=32)
    plt.tight_layout()
    plt.show()
    print(np.mean(tau_vec), np.std(tau_vec))

    plt.figure()
    plt.hist(p0_vec, bins = np.arange(0,4,0.25), color = cm.cool(0.25))
    plt.tick_params(labelsize=25)
    plt.ylabel(r'Number of cities', fontsize=25)
    plt.xlabel(r'$P_0$', fontsize=32)
    plt.tight_layout()
    plt.show()

    print(np.mean(p0_vec), np.std(p0_vec))

show_hist()