import pandas as pd
import matplotlib.pyplot as plt

result=pd.read_csv('summary-2020-04-07.txt')

plt.scatter(result['a'],result['b'])

for i,txt in enumerate(result['country']):
    plt.annotate(txt,(result['a'][i],result['b'][i]))

plt.scatter(-0.1623,-0.4296)
plt.annotate('China (exc. Hubei)',(-0.1623,-0.4296))
plt.scatter(-0.1847,-0.4598)
plt.annotate('Large Cities',(-0.1847,-0.4598))
plt.scatter(-0.1702,0.1522)
plt.annotate('Hubei (exc. Wuhan)',(-0.1702,0.1522))
plt.scatter(-0.1039,-0.6086)
plt.annotate('Wuhan',(-0.1039,-0.6086))

plt.xlabel('a')
plt.ylabel('b')
plt.show( bbox_inches='tight')