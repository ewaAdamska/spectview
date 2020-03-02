import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
from matplotlib.gridspec import GridSpec



def read_data(filename, bg_filename=''):
    #prepare Data Frame
    spect = pd.read_csv(filename, skiprows=1, names=['spectrum'])
    if bg_filename:
        bg = pd.read_csv(bg_filename, skiprows=1, names=['bg'])
        return pd.concat([spect, bg], axis=1)
    else:
        return spect



def addArrow(x, text, y, shiftx=0, length=0, fontsize=12):
    if not length:
        length = 0.2 * (plt.ylim()[1] - plt.ylim()[0])
    plt.annotate(text, xy=(x, y),
                 xytext=(x + shiftx, y + length),
                 rotation=90.,
                 xycoords='data',
                 fontsize=fontsize,
                 verticalalignment='bottom',
                 horizontalalignment='center',
                 arrowprops=dict(width=1, facecolor='black', headwidth=4,
                                 shrink=0.1))


def addEnergy(energy, y, text, shiftx=0, fontsize=10):
    plt.text(energy+shiftx, y, text, fontsize=fontsize, rotation=90)


if __name__=='__main__':

    GATES_LIST = (1436, 444)
    X_RANGE = (500, 900)
    Y_RANGE = (0, 200)
    SAVE_OUTPUT = True
    PRELIMINARY = False
    MARK = True
    LATEX = True

    FONT_SIZE = 22
    # latex
    if LATEX:
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')

    gatename="g{}g{}".format(GATES_LIST[0], GATES_LIST[1])
    try:
        data = read_data(filename="Examples/gate_{}.txt".format(gatename), bg_filename='Examples/bg_{}.txt'.format(gatename))
    except FileNotFoundError:
        data = read_data(filename="Examples/gate_{}.txt".format(gatename))

    try:
        gamma_marks = pd.read_excel('gamma_marks_{}.xlsx'.format(gatename))
    except FileNotFoundError:
        MARK = False




    fig, ax = plt.subplots()
    fig.set_size_inches(10, 5)

    left_margin = 1
    right_margin = 0.2
    top_margin = 0.2
    bottom_margin = 1.1
    size = fig.get_size_inches()


    ax.tick_params(axis='both', labelsize=FONT_SIZE)
    ax.set_xlabel('Energy (keV)', fontsize=FONT_SIZE, labelpad=20)
    ax.set_ylabel('Number of counts', fontsize=FONT_SIZE, labelpad=10)
    plt.subplots_adjust(left=left_margin/size[0], right=1-right_margin/size[0], top=1-top_margin/size[1], bottom=bottom_margin/size[1])

    plt.ylim(Y_RANGE[0], Y_RANGE[1])
    plt.xlim(X_RANGE[0], X_RANGE[1])

    #add gate name
    box_width = (-0.058*fig.get_size_inches()[0]+0.85) * (ax.get_xlim()[1] - ax.get_xlim()[0])
    box_height = 0.1 * (ax.get_ylim()[1] - ax.get_ylim()[0])

    gt = ax.text(ax.get_xlim()[1]-1.35*box_width, ax.get_ylim()[1]-1.1*box_height, "gates {} - {} keV  (a)".format(GATES_LIST[0], GATES_LIST[1]), fontsize=FONT_SIZE)


    #adding marks:
    if MARK:
        for index, gamma in gamma_marks.iterrows():
            if gamma.type == 'text':
                addEnergy(energy=int(gamma.energy), text="{} ({})".format(gamma.energy, gamma.isotope), y=gamma.y, shiftx=gamma.shiftx, fontsize=FONT_SIZE)
            elif gamma.type == 'arrow':
                addArrow(x=int(gamma.energy), text="{} ({})".format(gamma.energy, gamma.isotope), y=gamma.y, length=gamma.length, shiftx=gamma.shiftx, fontsize=FONT_SIZE)
            elif gamma.type == 'sign':
                addEnergy(energy=int(gamma.energy), text="{}".format(gamma.isotope), y=gamma.y, shiftx=gamma.shiftx, fontsize=FONT_SIZE)

    # plotting the data
    plot, = plt.plot(data.spectrum, drawstyle='steps-mid', color='black', lw=1)
    if 'bg' in data.columns:
        plt.plot(data.bg, drawstyle='steps-mid', lw=1, color="#FF7F00")

    # plt.plot(data.spectrum-data.bg, ds='steps-mid', lw=1)

    if PRELIMINARY:
        plt.text((ax.get_xlim()[1] + ax.get_xlim()[0])/2., (ax.get_ylim()[1] + ax.get_ylim()[0])/2.,
                 "PRELIMINARY", horizontalalignment='center', verticalalignment='center',
                 fontsize=54, alpha=0.3, color='grey', rotation=15)


    if SAVE_OUTPUT:
        plt.savefig("Output/{}_{}-{}.eps".format(gatename, int(ax.get_xlim()[0]), int(ax.get_xlim()[1])))
        plt.savefig("Output/{}_{}-{}.svg".format(gatename, int(ax.get_xlim()[0]), int(ax.get_xlim()[1])))
    # plt.show()


plt.show()