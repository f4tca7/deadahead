# Import the necessary libraries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64

def plot_two_vars(data1, data2):
    percentile_list = pd.DataFrame(
        {'variant1': data1,
        'variant2': data2
        })
    ax = sns.boxplot(orient="v", data=percentile_list, color='white')
    ax = sns.swarmplot( data=percentile_list, color=".25")

    fig = ax.get_figure()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    #image_data = str(base64.b64encode(buf.getvalue()))
    image_data = str(buf.getvalue())
    buf.close()
    return image_data