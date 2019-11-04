import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
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



def addArrow(x, text, y, shiftx=0, length=0):
    if not length:
        length = 0.2 * (plt.ylim()[1] - plt.ylim()[0])
    plt.annotate(text, xy=(x, y),
                 xytext=(x + shiftx, y + length),
                 rotation=90.,
                 xycoords='data',
                 fontsize=12,
                 verticalalignment='bottom',
                 horizontalalignment='center',
                 arrowprops=dict(width=1, facecolor='black', headwidth=4,
                                 shrink=0.1))


def addEnergy(energy, y, text, shiftx=0, fontsize=10):
    plt.text(energy+shiftx, y, text, fontsize=fontsize, rotation=90)


if __name__=='__main__':

    GATES_LIST = (181, 322)
    X_RANGE = (300, 500)
    Y_RANGE = (0, 100)
    SAVE_OUTPUT = False
    PRELIMINARY = False
    MARK = True

    gatename="g{}g{}".format(GATES_LIST[0], GATES_LIST[1])
    try:
        data = read_data(filename="Gates/gate_{}.txt".format(gatename), bg_filename='Gates/bg_{}.txt'.format(gatename))
    except FileNotFoundError:
        data = read_data(filename="Gates/gate_{}.txt".format(gatename))

    try:
        gamma_marks = pd.read_excel('gamma_marks_{}.xlsx'.format(gatename))
    except FileNotFoundError:
        MARK = False

    # fig, ax_array = plt.subplots(ncols=1, nrows=2)
    # ax, ax2 = ax_array


    fig, ax = plt.subplots()
    fig.set_size_inches(10, 5)

    ax.tick_params(axis='both', labelsize=14)
    ax.set_xlabel('Energy (keV)', fontsize=12)
    ax.set_ylabel('Number of counts', fontsize=12)
    plt.subplots_adjust(bottom=0.25)

    plt.ylim(Y_RANGE[0], Y_RANGE[1])
    plt.xlim(X_RANGE[0], X_RANGE[1])

    #add gate name
    box_width = 0.2 * (ax.get_xlim()[1] - ax.get_xlim()[0])
    box_height = 0.1 * (ax.get_ylim()[1] - ax.get_ylim()[0])

    gt = ax.text(ax.get_xlim()[1]-1.2*box_width, ax.get_ylim()[1]-1.1*box_height, "gate {} - {} keV ".format(GATES_LIST[0], GATES_LIST[1]), fontsize=12)

    #adding marks:
    if MARK:
        for index, gamma in gamma_marks.iterrows():
            if gamma.type == 'text':
                addEnergy(energy=int(gamma.energy), text="{} ({})".format(gamma.energy, gamma.isotope), y=gamma.y, shiftx=gamma.shiftx, fontsize=12)
            elif gamma.type == 'arrow':
                addArrow(x=int(gamma.energy), text="{} ({})".format(gamma.energy, gamma.isotope), y=gamma.y, length=gamma.length, shiftx=gamma.shiftx)
            elif gamma.type == 'sign':
                addEnergy(energy=int(gamma.energy), text="{}".format(gamma.isotope), y=gamma.y, shiftx=gamma.shiftx, fontsize=20)

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
        plt.savefig("Output/{}_{}-{}.svg".format(gatename, int(ax.get_xlim()[0]), int(ax.get_xlim()[1])))
        # plt.savefig("Output/{}_{}-{}.png".format(gatename, int(ax.get_xlim()[0]), int(ax.get_xlim()[1])))
    # plt.show()




# buttons
class Index(object):
    ind = 0
    step = 100

    def next(self, event):
        self.ind +=1
        start, stop = ax.get_xlim()
        ax.set_xlim(int(start) + self.step, int(stop) + self.step)
        self._updatePlot()

    def prev(self, event):
        self.ind -= 1
        start, stop = ax.get_xlim()
        ax.set_xlim(int(start) - self.step, int(stop) - self.step)
        self._updatePlot()

    def _updatePlot(self):
        ax.autoscale(axis='y', tight=False)
        box_width = 0.2 * (ax.get_xlim()[1] - ax.get_xlim()[0])
        box_height = 0.1 * (ax.get_ylim()[1] - ax.get_ylim()[0])

        gt.set_position([ax.get_xlim()[1]-1.2*box_width, ax.get_ylim()[1]-1.1*box_height])

        plt.draw()

class Utilities(object):
    def save(self, event):
        plt.savefig("Output/{}_{}-{}.svg".format(gatename, int(ax.get_xlim()[0]), int(ax.get_xlim()[1])))


# prev & next
callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075]) #button coordinates and size
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bprev = Button(axprev, 'Previous')

# save
button = Utilities()
axsave = plt.axes([0.91, 0.8, 0.075, 0.075]) #button coordinates and size
bsave = Button(axsave, 'Save')

bnext.on_clicked(callback.next)
bprev.on_clicked(callback.prev)
bsave.on_clicked(button.save)

plt.show()
