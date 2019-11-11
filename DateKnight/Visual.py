import pandas as pd
import matplotlib.pyplot as plt
from Cacher import pickled
data = pd.DataFrame()

#MEAN RUNTIME OF MOVIES VISUALIZATION
def first():
    data['runtimeMinutes'].mean()
    data.sort_values('runtimeMinutes')
    plt.ylabel("NO. OF MOVIES")
    plt.xlabel("RUNTIME OF MOVIES IN MINUTE")
    plt.autoscale(enable=True,axis='both',tight=None)
    data['runtimeMinutes'].plot(kind='hist', bins=[0,20,40,80,100,120,140,160,180,200,220,240,260,280,300])
    plt.show()

#AVERAGE RATING OF MOVIES VISUALIZATION
def second():
    data.sort_values('averageRating')
    plt.ylabel("NO. OF MOVIES")
    plt.xlabel("AVG. RATINGS OF MOVIES")
    plt.autoscale(enable=True,axis='both',tight=None)
    data['averageRating'].plot(kind='hist', bins=[0,2,4,6,8,10])
    plt.show()

@pickled
def load_file():
    return pd.read_excel("imdb_output.xlsx",sheet_name="IMDBClean")

def set_data(IMDB):
    global data
    data = IMDB



