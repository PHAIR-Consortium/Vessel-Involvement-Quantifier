import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon


def save_boxplot(degrees_matrix):
    degrees = ['0', '0-90', '90-180', '180-270', '270-360']
    data = [degrees_matrix[0], degrees_matrix[1], degrees_matrix[2], degrees_matrix[3], degrees_matrix[4]]

    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    bp = ax1.boxplot(data, notch=False, sym='+', vert=True, whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')

    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)
    ax1.set(
        axisbelow=True,
        title='Comparison of IID Bootstrap Resampling Across Five Distributions',
        xlabel='Radiologist Degree of Vascular Involvement Assessment',
        ylabel='AI Degree of Vascular Involvement Assessment',
    )

    num_boxes = len(data)
    medians = np.empty(num_boxes)
    for i in range(num_boxes):
        box = bp['boxes'][i]
        box_x = []
        box_y = []
        for j in range(5):
            box_x.append(box.get_xdata()[j])
            box_y.append(box.get_ydata()[j])
        box_coords = np.column_stack([box_x, box_y])
        ax1.add_patch(Polygon(box_coords, facecolor='royalblue'))
        med = bp['medians'][i]
        median_x = []
        median_y = []
        for j in range(2):
            median_x.append(med.get_xdata()[j])
            median_y.append(med.get_ydata()[j])
            ax1.plot(median_x, median_y, 'k')
        medians[i] = median_y[0]
        ax1.plot(np.average(med.get_xdata()), np.average(data[i]), color='w', marker='*', markeredgecolor='k')

    ax1.set_xlim(0.5, num_boxes + 0.5)
    ax1.set_ylim(0, 360)
    ax1.set_xticklabels(degrees, rotation=45, fontsize=8)

    pos = np.arange(num_boxes) + 1
    upper_labels = [str(round(s, 2)) for s in medians]
    weights = ['bold', 'semibold']
    for tick, label in zip(range(num_boxes), ax1.get_xticklabels()):
        k = tick % 2
        ax1.text(pos[tick], .95, upper_labels[tick], transform=ax1.get_xaxis_transform(),
                 horizontalalignment='center', size='x-small', weight=weights[k], color='royalblue')

    fig.text(0.80, 0.015, '*', color='white', backgroundcolor='silver', weight='roman', size='medium')
    fig.text(0.815, 0.013, ' Average Value', color='black', weight='roman', size='x-small')

    plt.savefig('boxplot.png')
