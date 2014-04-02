import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

e_omr_same_pre = [
'/home/vburns/Dropbox/ConchisData/2013-10-31/f00833/f00833_2013-10-31-09-54-59.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00834/f00834_2013-10-31-09-55-06.json', #lost tracking
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00835/f00835_2013-10-31-09-55-12.json',#low vel
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00836/f00836_2013-10-31-09-55-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00841/f00841_2013-10-31-13-48-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00842/f00842_2013-10-31-13-49-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00843/f00843_2013-10-31-13-49-05.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00844/f00844_2013-10-31-13-49-11.json', #tracking
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
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00844/f00844_2013-10-31-14-21-50.json',
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

c_omr_pre=[
'/home/vburns/Dropbox/ConchisData/2013-10-31/f00837/f00837_2013-10-31-09-55-55.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00838/f00838_2013-10-31-09-55-44.json', #low vel
 '/home/vburns/Dropbox/ConchisData/2013-10-31/f00839/f00839_2013-10-31-09-55-47.json',
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00840/f00840_2013-10-31-09-55-28.json', #tracking
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
# '/home/vburns/Dropbox/ConchisData/2013-10-31/f00840/f00840_2013-10-31-10-28-52.json',
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

print "Done loading fish"

