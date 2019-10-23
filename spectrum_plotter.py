import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


####
# TODO: different colors of marks?

####



def read_data(filename, bg_filename=''):
    #prepare Data Frame
    spect = pd.read_csv(filename, skiprows=1, names=['spectrum'])
    if bg_filename:
        bg = pd.read_csv(bg_filename, skiprows=1, names=['bg'])
        return pd.concat([spect, bg], axis=1)
    else:
        return spect



def addArrow(x, text, y, shiftx=0, length=0):
    if not length:
        length = 0.2 * (plt.ylim()[1] - plt.ylim()[0])
    plt.annotate(text, xy=(x, y),
                 xytext=(x + shiftx, y + length),
                 rotation=90.,
                 xycoords='data',
                 fontsize=10,
                 verticalalignment='bottom',
                 horizontalalignment='center',
                 arrowprops=dict(width=1, facecolor='black', headwidth=4,
                                 shrink=0.1))


def addEnergy(energy, y, text, shiftx=0):
    plt.text(energy+shiftx, y, text, fontsize=10, rotation=90)


if __name__=='__main__':

    GATES_LIST = (1436, 444)
    X_RANGE = (500, 900)
    Y_RANGE = (0, 200)
    SAVE_OUTPUT = True
    PRELIMINARY = False

    gatename="g{}g{}".format(GATES_LIST[0], GATES_LIST[1])
    data = read_data(filename="gate_{}.txt".format(gatename), bg_filename='bg_{}.txt'.format(gatename))
    gamma_marks = pd.read_excel('gamma_marks_{}.xlsx'.format(gatename))

    fig = plt.figure(figsize=(10, 4))
    ax = fig.add_subplot()
    ax.tick_params(axis='both', labelsize=14)
    ax.set_xlabel('energy (keV)', fontsize=12)
    ax.set_ylabel('counts', fontsize=12)
    plt.subplots_adjust(bottom=0.15)

    plt.ylim(Y_RANGE[0], Y_RANGE[1])
    plt.xlim(X_RANGE[0], X_RANGE[1])

    #add gate name
    box_width = 0.2 * (ax.get_xlim()[1] - ax.get_xlim()[0])
    box_height = 0.1 * (ax.get_ylim()[1] - ax.get_ylim()[0])

    ax.text(ax.get_xlim()[1]-1.2*box_width, ax.get_ylim()[1]-1.1*box_height, "gate {} & {} keV ".format(GATES_LIST[0], GATES_LIST[1]), fontsize=12)



    #adding marks:
    for index, gamma in gamma_marks.iterrows():
        if gamma.type == 'text':
            addEnergy(energy=int(gamma.energy), text="{}: {} keV".format(gamma.isotope, gamma.energy), y=gamma.y, shiftx=gamma.shiftx)
        elif gamma.type == 'arrow':
            addArrow(x=int(gamma.energy), text="{}: {} keV".format(gamma.isotope, gamma.energy), y=gamma.y, length=gamma.length, shiftx=gamma.shiftx)


    # plotting the data
    plt.plot(data.spectrum, ds='steps-mid', color='black', lw=1)
    if 'bg' in data.columns:
        plt.plot(data.bg, ds='steps-mid', lw=1, color="#FF7F00")

    # plt.plot(data.spectrum-data.bg, ds='steps-mid', lw=1)

    if PRELIMINARY:
        plt.text((ax.get_xlim()[1] + ax.get_xlim()[0])/2., (ax.get_ylim()[1] + ax.get_ylim()[0])/2.,
                 "PRELIMINARY" ,horizontalalignment='center', verticalalignment='center',
                 fontsize=54, alpha=0.3, color='grey', rotation=15)



    if SAVE_OUTPUT:
        plt.savefig("Output/{}_{}-{}.svg".format(gatename, int(ax.get_xlim()[0]), int(ax.get_xlim()[1])))
        plt.savefig("Output/{}_{}-{}.png".format(gatename, int(ax.get_xlim()[0]), int(ax.get_xlim()[1])))
    plt.show()



