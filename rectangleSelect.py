import numpy as np

from matplotlib.path import Path
from matplotlib.widgets import RectangleSelector


class SelectFromCollection:
    def __init__(self, ax, collection, alpha_other = 0.3):
        self.canvas = ax.figure.canvas
        self.collection = collection
        self.alpha_other = alpha_other

        self.xys = collection.get_offsets()
        self.Npts = len(self.xys)

        self.fc = collection.get_facecolors()
        if len(self.fc) == 0:
            raise ValueError('Collection must have a facecolor')
        elif len(self.fc) == 1:
            self.fc = np.tile(self.fc, (self.Npts, 1))

        self.rectangle = RectangleSelector(ax,
                onselect = self.onselect)
        self.ind = []
    
    def selectionPath(self, x1, y1, x2, y2):
        return Path([(x1, y1), (x1, y2), (x2, y2), (x2, y1)])
        

    def onselect(self, event_click, event_release):
        path = self.selectionPath(event_click.xdata,
                event_click.ydata,
                event_release.xdata, 
                event_release.ydata
                )
        self.ind = np.nonzero(path.contains_points(self.xys))[0]
        self.fc[:, -1] = self.alpha_other
        self.fc[self.ind, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

    def getDataAndReset(self):
        self.fc[:, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()



def plotScatter(x, y):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1)

    pts = ax.scatter(x, y)
    selector = SelectFromCollection(ax, pts)

    def accept(event):
        if event.key == "enter":
            print("Selected points:")
            print(selector.xys[selector.ind])
            selector.getDataAndReset()
            fig.canvas.draw()

    fig.canvas.mpl_connect("key_press_event", accept)
    ax.set_title("Press enter to accept selected points.")

    plt.show()


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    x = np.arange(-5, 6)
    y = x**2

    plotScatter(x, y)

