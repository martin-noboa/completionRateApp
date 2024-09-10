import seaborn as sns
import matplotlib.pyplot as plt

def countplot(df, path, process):
    statusCounts = df['Status'].value_counts()
    sortedStatuses = statusCounts.index  # Index of sorted counts
    plt.figure(figsize = (10,7))
    sns.countplot(data = df, x = 'Status',order = sortedStatuses)
    ax = sns.countplot(x='Status', data=df)

    for p in ax.patches:
        height = p.get_height()
        ax.annotate(height,
                    (p.get_x() + p.get_width() / 2., height),
                    ha = 'center', va = 'center',
                    xytext = (0, 5),  # 9 points vertical offset
                    textcoords = 'offset points')
    filename = path + "/" + process + "_countplot.png"
    plt.savefig(filename, format='png', dpi=300)
    return filename