import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

'''
e_omr_pre = [

]
e_omr_pre=aba.loadMultipleDataFiles(e_omr_pre)

e_omr = [


]
e_omr = aba.loadMultipleDataFiles(e_omr)

e_omr_post = [

]
e_omr_post = aba.loadMultipleDataFiles(e_omr_post)

e_omr_same_pre = [
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00805/f00805_2013-10-29-10-24-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00806/f00806_2013-10-29-10-24-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00807/f00807_2013-10-29-10-24-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00808/f00808_2013-10-29-10-24-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00813/f00813_2013-10-29-13-39-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00814/f00814_2013-10-29-13-39-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00815/f00815_2013-10-29-13-39-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00816/f00816_2013-10-29-13-39-19.json',
'/home/vburns/Dropbox/ConchisData/2013-10-29/f00817/f00817_2013-10-29-16-13-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00818/f00818_2013-10-29-16-13-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00819/f00819_2013-10-29-16-13-50.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00820/f00820_2013-10-29-16-14-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00821/f00821_2013-10-29-16-14-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00822/f00822_2013-10-29-16-14-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00823/f00823_2013-10-29-16-15-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00824/f00824_2013-10-29-16-15-09.json',
]
e_omr_same_pre=aba.loadMultipleDataFiles(e_omr_same_pre)

e_omr_same = [
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00805/f00805_2013-10-29-10-59-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00806/f00806_2013-10-29-10-59-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00807/f00807_2013-10-29-10-59-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00808/f00808_2013-10-29-10-59-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00813/f00813_2013-10-29-14-10-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00814/f00814_2013-10-29-14-10-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00815/f00815_2013-10-29-14-10-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00816/f00816_2013-10-29-14-10-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00817/f00817_2013-10-29-16-45-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00818/f00818_2013-10-29-16-45-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00819/f00819_2013-10-29-16-45-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00820/f00820_2013-10-29-16-45-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00821/f00821_2013-10-29-16-46-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00822/f00822_2013-10-29-16-46-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00823/f00823_2013-10-29-16-46-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00824/f00824_2013-10-29-16-46-32.json',

]
e_omr_same = aba.loadMultipleDataFiles(e_omr_same)

e_omr_same_last = [
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00805/f00805_2013-10-29-11-47-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00806/f00806_2013-10-29-11-47-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00807/f00807_2013-10-29-11-46-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00808/f00808_2013-10-29-11-46-50.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00813/f00813_2013-10-29-14-10-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00814/f00814_2013-10-29-14-10-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00815/f00815_2013-10-29-14-10-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00816/f00816_2013-10-29-14-10-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00817/f00817_2013-10-29-16-45-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00818/f00818_2013-10-29-16-45-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00819/f00819_2013-10-29-16-45-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00820/f00820_2013-10-29-16-45-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00821/f00821_2013-10-29-16-46-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00822/f00822_2013-10-29-16-46-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00823/f00823_2013-10-29-16-46-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00824/f00824_2013-10-29-16-46-32.json',

]
e_omr_same_last = aba.loadMultipleDataFiles(e_omr_same_last)

for i in range(0,4):
    e_omr_same_last[i]['stateinfo'][1][1]=8


e_omr_same_post = [
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00805/f00805_2013-10-29-12-04-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00806/f00806_2013-10-29-12-04-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00807/f00807_2013-10-29-12-03-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00808/f00808_2013-10-29-12-03-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00813/f00813_2013-10-29-15-14-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00814/f00814_2013-10-29-15-15-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00815/f00815_2013-10-29-15-15-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00816/f00816_2013-10-29-15-15-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00817/f00817_2013-10-29-17-50-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00818/f00818_2013-10-29-17-50-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00819/f00819_2013-10-29-17-50-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00820/f00820_2013-10-29-17-50-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00821/f00821_2013-10-29-17-51-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00822/f00822_2013-10-29-17-51-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00823/f00823_2013-10-29-17-51-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00824/f00824_2013-10-29-17-52-38.json'
]
e_omr_same_post = aba.loadMultipleDataFiles(e_omr_same_post)

c_omr_pre=[
'/home/vburns/Dropbox/ConchisData/2013-10-29/f00801/f00801_2013-10-29-10-23-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00802/f00802_2013-10-29-10-23-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00803/f00803_2013-10-29-10-23-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00804/f00804_2013-10-29-10-23-54.json',
#'/home/vburns/Dropbox/ConchisData/2013-10-29/f00809/f00809_2013-10-29-13-38-37.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00810/f00810_2013-10-29-13-38-33.json',
 #'/home/vburns/Dropbox/ConchisData/2013-10-29/f00811/f00811_2013-10-29-13-38-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00812/f00812_2013-10-29-13-38-22.json',

]
c_omr_pre = aba.loadMultipleDataFiles(c_omr_pre)

c_omr =[
'/home/vburns/Dropbox/ConchisData/2013-10-29/f00801/f00801_2013-10-29-10-59-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00802/f00802_2013-10-29-10-59-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00803/f00803_2013-10-29-10-59-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00804/f00804_2013-10-29-10-59-23.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-29/f00809/f00809_2013-10-29-14-09-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00810/f00810_2013-10-29-14-09-57.json',
 #'/home/vburns/Dropbox/ConchisData/2013-10-29/f00811/f00811_2013-10-29-14-10-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00812/f00812_2013-10-29-14-10-13.json',

]
c_omr = aba.loadMultipleDataFiles(c_omr)

c_omr_last = [
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00801/f00801_2013-10-29-11-46-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00802/f00802_2013-10-29-11-46-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00803/f00803_2013-10-29-11-46-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00804/f00804_2013-10-29-11-46-25.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-29/f00809/f00809_2013-10-29-14-09-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00810/f00810_2013-10-29-14-09-57.json',
 #'/home/vburns/Dropbox/ConchisData/2013-10-29/f00811/f00811_2013-10-29-14-10-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00812/f00812_2013-10-29-14-10-13.json',
]
c_omr_last = aba.loadMultipleDataFiles(c_omr_last)

for i in range(0,4):
    c_omr_last[i]['stateinfo'][1][1]=8


c_omr_post = [
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00801/f00801_2013-10-29-12-03-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00802/f00802_2013-10-29-12-03-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00803/f00803_2013-10-29-12-03-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00804/f00804_2013-10-29-12-03-31.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-29/f00809/f00809_2013-10-29-15-14-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00810/f00810_2013-10-29-15-14-03.json',
 #'/home/vburns/Dropbox/ConchisData/2013-10-29/f00811/f00811_2013-10-29-15-14-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-29/f00812/f00812_2013-10-29-15-14-31.json',
]
c_omr_post = aba.loadMultipleDataFiles(c_omr_post)
'''
e_omr_same_pre = [
'/home/vburns/Dropbox/ConchisData/2013-10-31/f00833/f00833_2013-10-31-09-54-59.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00834/f00834_2013-10-31-09-55-06.json', #lost tracking
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00835/f00835_2013-10-31-09-55-12.json',#low vel
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00836/f00836_2013-10-31-09-55-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00841/f00841_2013-10-31-13-48-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00842/f00842_2013-10-31-13-49-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00843/f00843_2013-10-31-13-49-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00844/f00844_2013-10-31-13-49-11.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00845/f00845_2013-10-31-13-49-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00846/f00846_2013-10-31-13-49-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00847/f00847_2013-10-31-13-49-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00848/f00848_2013-10-31-13-49-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00857/f00857_2013-11-01-13-21-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00858/f00858_2013-11-01-13-21-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00859/f00859_2013-11-01-13-21-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00860/f00860_2013-11-01-13-21-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00861/f00861_2013-11-01-13-21-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00862/f00862_2013-11-01-13-21-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00863/f00863_2013-11-01-13-21-58.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00864/f00864_2013-11-01-13-22-03.json',

]
e_omr_same_pre=aba.loadMultipleDataFiles(e_omr_same_pre)

e_omr_same = [
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00833/f00833_2013-10-31-10-28-04.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00834/f00834_2013-10-31-10-28-11.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00835/f00835_2013-10-31-10-28-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00836/f00836_2013-10-31-10-28-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00841/f00841_2013-10-31-14-22-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00842/f00842_2013-10-31-14-22-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00843/f00843_2013-10-31-14-21-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00844/f00844_2013-10-31-14-21-50.json',
#'/home/vburns/Dropbox/ConchisData/2013-10-31/f00845/f00845_2013-10-31-14-22-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00846/f00846_2013-10-31-14-22-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00847/f00847_2013-10-31-14-22-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00848/f00848_2013-10-31-14-22-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00857/f00857_2013-11-01-13-55-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00858/f00858_2013-11-01-13-55-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00859/f00859_2013-11-01-13-54-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00860/f00860_2013-11-01-13-54-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00861/f00861_2013-11-01-13-55-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00862/f00862_2013-11-01-13-55-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00863/f00863_2013-11-01-13-55-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00864/f00864_2013-11-01-13-55-13.json',

]
e_omr_same = aba.loadMultipleDataFiles(e_omr_same)

e_omr_same_last = e_omr_same

e_omr_same_post = [
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00833/f00833_2013-10-31-11-32-05.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00834/f00834_2013-10-31-11-31-56.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00835/f00835_2013-10-31-11-31-44.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00836/f00836_2013-10-31-11-31-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00841/f00841_2013-10-31-15-25-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00842/f00842_2013-10-31-15-25-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00843/f00843_2013-10-31-15-25-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00844/f00844_2013-10-31-15-25-34.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00845/f00845_2013-10-31-15-25-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00846/f00846_2013-10-31-15-26-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00847/f00847_2013-10-31-15-26-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00848/f00848_2013-10-31-15-26-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00857/f00857_2013-11-01-14-59-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00858/f00858_2013-11-01-14-59-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00859/f00859_2013-11-01-15-00-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00860/f00860_2013-11-01-15-00-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00861/f00861_2013-11-01-15-00-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00862/f00862_2013-11-01-15-00-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00863/f00863_2013-11-01-15-00-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-01/f00864/f00864_2013-11-01-15-00-51.json',
]
e_omr_same_post = aba.loadMultipleDataFiles(e_omr_same_post)

c_omr_pre=[
'/home/vburns/Dropbox/ConchisData/2013-10-31/f00837/f00837_2013-10-31-09-55-55.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00838/f00838_2013-10-31-09-55-44.json', #low vel
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00839/f00839_2013-10-31-09-55-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00840/f00840_2013-10-31-09-55-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00849/f00849_2013-10-31-16-23-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00850/f00850_2013-10-31-16-23-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00851/f00851_2013-10-31-16-23-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00852/f00852_2013-10-31-16-23-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00853/f00853_2013-10-31-16-23-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00854/f00854_2013-10-31-16-23-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00855/f00855_2013-10-31-16-23-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00856/f00856_2013-10-31-16-23-59.json',
]
c_omr_pre = aba.loadMultipleDataFiles(c_omr_pre)

c_omr =[
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00837/f00837_2013-10-31-10-28-32.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00838/f00838_2013-10-31-10-28-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00839/f00839_2013-10-31-10-28-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00840/f00840_2013-10-31-10-28-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00849/f00849_2013-10-31-16-54-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00850/f00850_2013-10-31-16-54-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00851/f00851_2013-10-31-16-54-44.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00852/f00852_2013-10-31-16-54-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00853/f00853_2013-10-31-16-54-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00854/f00854_2013-10-31-16-55-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00855/f00855_2013-10-31-16-55-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00856/f00856_2013-10-31-16-55-15.json',
]
c_omr = aba.loadMultipleDataFiles(c_omr)

c_omr_last = c_omr

c_omr_post = [
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00837/f00837_2013-10-31-11-32-15.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00838/f00838_2013-10-31-11-32-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00839/f00839_2013-10-31-11-32-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00840/f00840_2013-10-31-11-32-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00849/f00849_2013-10-31-17-57-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00850/f00850_2013-10-31-17-58-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00851/f00851_2013-10-31-17-58-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00852/f00852_2013-10-31-17-58-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00853/f00853_2013-10-31-17-58-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00854/f00854_2013-10-31-17-58-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00855/f00855_2013-10-31-17-58-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00856/f00856_2013-10-31-17-58-41.json'
]
c_omr_post = aba.loadMultipleDataFiles(c_omr_post)

print "Done loading fish"

