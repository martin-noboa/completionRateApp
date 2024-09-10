import seaborn as sns
import matplotlib.pyplot as plt

def countplot(df, path, process):
    customPalette = {
        'Complete': '#242B56',   # Space Cadet
        'Pending': '#EFF1F4',    # Anti-Flash White
        'Locked': '#EFF1F4',     # Anti-Flash White
        'Business Exception': '#4AC0E8',  # Picton Blue
        'Exception': '#5593A7'   # Rackley
    }

    statusCounts = df['Status'].value_counts()
    sortedStatuses = statusCounts.index  # Index of sorted counts
    plt.figure(figsize = (10,7))
    ax = sns.countplot(data = df, x = 'Status',hue = "Status",order = sortedStatuses,palette=customPalette)
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