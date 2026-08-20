import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('/Users/dimitricriswell/boilerplate-page-view-time-series-visualizer/fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean data
df = df[(df['value'] <= df['value'].quantile(0.975)) & (df['value'] >= df['value'].quantile(0.025))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(18,6))
    ax.plot(df.index, df['value'], color='red')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean()
    df_bar = df_bar.unstack()
    # Draw bar plot
    ax = df_bar.plot(figsize=(8,8), legend=True, kind='bar', xlabel='Years', ylabel='Average Page Views')
    ax.legend(['January','February','March','April','May','June','July','August','September','October','November', 'December'], title='Months')
    fig = ax.figure
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1,2,figsize=(16,6))
    sns.boxplot(data=df_box, x='year',y='value',ax=axes[0], hue='year', legend=False, palette=['blue','orange','green','red'] ,width = 1, fliersize =1, gap=0.2)
    axes[0].set(title='Year-wise Box Plot (Trend)', xlabel='Year', ylabel='Page Views', yticks=range(0,200001,20000))

    sns.boxplot(data=df_box,ax=axes[1], x='month', y='value', hue='month', palette='rainbow', legend=False, fliersize=1, gap=0.1, order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[1].set(title='Month-wise Box Plot (Seasonality)', xlabel='Month', ylabel='Page Views', yticks=range(0,200001,20000))

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
