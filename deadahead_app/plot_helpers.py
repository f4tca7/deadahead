# Import the necessary libraries
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import io
import base64

def plot_to_base64_png(figure):
    buf = None
    image_data = ""
    buf = io.BytesIO()
    figure.savefig(buf, format='png', bbox_inches='tight', frameon=True)
    buf.seek(0)
    image_data = str(base64.b64encode(buf.getvalue()))
    buf.close()
    image_data = image_data[2:-1]

    return image_data   


def plot_box_swarm(data1, data2):
    try:
        my_dict = dict(variant1 = data1, variant2 = data2) 
        df = pd.DataFrame.from_dict(my_dict, orient='index')    
        df = df.transpose()    
        sns.set_style("whitegrid")
        sns.set_context("paper")
        box_swarm_fig, box_swarm_ax = plt.subplots()
        ax = sns.boxplot(orient="v", data=df, color='white')
        if len(data1) < 200:
            ax = sns.swarmplot( data=df, color=".25")
        box_swarm_fig.set_figheight(5)
        box_swarm_fig.set_figwidth(3)

        return plot_to_base64_png(box_swarm_fig)
    except:
        return ""

def plot_hist(data1, data2):    
    #if len(data1) < 2 | len(data2) < 2 :
    try:
        my_dict = dict(variant1 = data1, variant2 = data2) 
        df = pd.DataFrame.from_dict(my_dict, orient='index')
        df = df.transpose()    
        
        df['dummy'] = 'dummy'
        df = df.melt(id_vars=['dummy'])
        df = df[['variable', 'value']]
        g = sns.FacetGrid(df, row="variable",
                        height=2.25, aspect=3,)
        g = g.map(sns.distplot, "value", hist=True, rug=True, norm_hist=False, kde=False)
        return plot_to_base64_png(g)
    except:
        return ""
