import ArenaBehaviorAnalysis as aba
import matplotlib as mpl
import matplotlib.pyplot as plt

if __name__ == '__main__':
    d = aba.loadDataFromFile_UI(initialdir='~/Dropbox/ConchisData/')
    if d is not None:
        aba.plotFishSummary(d)
        plt.show()

