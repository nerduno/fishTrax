import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

if len(e_first) < 1:
    print "No fish"
    1/0
else: 
    print "Fish data found"

e_water_first = [
'/home/vburns/Dropbox/ConchisData/2013-05-15/f00422/f00422_2013-05-15-14-37-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00423/f00423_2013-05-15-14-37-29.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00424/f00424_2013-05-15-14-37-25.json',#low starting velocity
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00425/f00425_2013-05-15-14-37-21.json', #problem with plotting ##CHECKCHECK
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00426/f00426_2013-05-15-14-40-23.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00427/f00427_2013-05-15-14-40-20.json', #current imbalance
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00428/f00428_2013-05-15-14-40-18.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00429/f00429_2013-05-15-14-40-13.json', #tracking in sec?
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00430/f00430_2013-05-16-10-04-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00431/f00431_2013-05-16-10-04-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00432/f00432_2013-05-16-10-04-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00433/f00433_2013-05-16-10-04-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00434/f00434_2013-05-16-10-05-40.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-16/f00435/f00435_2013-05-16-10-05-42.json', #low starting velocity
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00436/f00436_2013-05-16-10-05-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00437/f00437_2013-05-16-10-05-47.json',
]
e_water_first = aba.loadMultipleDataFiles(e_water_first)

#this is new water in shock tank
e_water_shock = [
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00422/f00422_2013-05-15-15-08-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00423/f00423_2013-05-15-15-08-34.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00424/f00424_2013-05-15-15-08-45.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00425/f00425_2013-05-15-15-08-54.json', 
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00426/f00426_2013-05-15-15-11-28.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00427/f00427_2013-05-15-15-11-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00428/f00428_2013-05-15-15-11-41.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00429/f00429_2013-05-15-15-11-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00430/f00430_2013-05-16-10-35-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00431/f00431_2013-05-16-10-35-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00432/f00432_2013-05-16-10-35-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00433/f00433_2013-05-16-10-35-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00434/f00434_2013-05-16-10-37-23.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-16/f00435/f00435_2013-05-16-10-37-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00436/f00436_2013-05-16-10-36-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00437/f00437_2013-05-16-10-36-50.json',
]
e_water_shock = aba.loadMultipleDataFiles(e_water_shock)

e_water_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00422/f00422_2013-05-15-16-04-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00423/f00423_2013-05-15-16-04-02.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00424/f00424_2013-05-15-16-03-56.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00425/f00425_2013-05-15-16-03-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00426/f00426_2013-05-15-16-07-09.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00427/f00427_2013-05-15-16-07-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00428/f00428_2013-05-15-16-07-33.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00429/f00429_2013-05-15-16-07-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00430/f00430_2013-05-16-11-31-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00431/f00431_2013-05-16-11-31-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00432/f00432_2013-05-16-11-31-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00433/f00433_2013-05-16-11-30-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00434/f00434_2013-05-16-11-34-22.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-16/f00435/f00435_2013-05-16-11-34-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00436/f00436_2013-05-16-11-35-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00437/f00437_2013-05-16-11-35-21.json',
]
e_water_sec = aba.loadMultipleDataFiles(e_water_sec)

#safe tank with shock water
e_safe_shockwater_first = [
#'/home/vburns/Dropbox/ConchisData/2013-06-19/f00554/f00554_2013-06-19-10-19-13.json',#current imbalance
# '/home/vburns/Dropbox/ConchisData/2013-06-19/f00555/f00555_2013-06-19-10-19-11.json', #lost tracking
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00556/f00556_2013-06-19-10-19-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00557/f00557_2013-06-19-10-19-07.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-19/f00558/f00558_2013-06-19-10-20-11.json',#potential current imbalcne? only a few times
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00559/f00559_2013-06-19-10-20-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00560/f00560_2013-06-19-10-20-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00561/f00561_2013-06-19-10-20-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00570/f00570_2013-06-20-10-16-15.json',
#'/home/vburns/Dropbox/ConchisData/2013-06-20/f00571/f00571_2013-06-20-10-16-03.json', #low starting velocity
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00572/f00572_2013-06-20-10-15-52.json', #lost tracking in shock
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00573/f00573_2013-06-20-10-15-42.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00574/f00574_2013-06-20-10-16-59.json', #tracking and current?
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00575/f00575_2013-06-20-10-16-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00576/f00576_2013-06-20-10-16-38.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00577/f00577_2013-06-20-10-16-28.json', #low starting velocity
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00587/f00587_2013-06-27-10-22-04.json',#9 to 21
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00588/f00588_2013-06-27-10-22-08.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00590/f00590_2013-06-27-10-23-18.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00591/f00591_2013-06-27-10-23-16.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00592/f00592_2013-06-27-10-23-14.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00593/f00593_2013-06-27-13-12-48.json', #high current (imbalance?)
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00594/f00594_2013-06-27-13-12-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00595/f00595_2013-06-27-13-12-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00596/f00596_2013-06-27-13-12-22.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00597/f00597_2013-06-27-13-13-47.json', #current imbalance/weird 
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00598/f00598_2013-06-27-13-13-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00599/f00599_2013-06-27-13-13-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00600/f00600_2013-06-27-13-13-11.json',
]
e_safe_shockwater_first = aba.loadMultipleDataFiles(e_safe_shockwater_first)

e_safe_shockwater_shock = [
# '/home/vburns/Dropbox/ConchisData/2013-06-19/f00554/f00554_2013-06-19-10-54-27.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-19/f00555/f00555_2013-06-19-10-54-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00556/f00556_2013-06-19-10-54-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00557/f00557_2013-06-19-10-54-56.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-19/f00558/f00558_2013-06-19-10-56-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00559/f00559_2013-06-19-10-56-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00560/f00560_2013-06-19-10-56-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00561/f00561_2013-06-19-10-56-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00570/f00570_2013-06-20-10-47-17.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00571/f00571_2013-06-20-10-47-21.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00572/f00572_2013-06-20-10-47-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00573/f00573_2013-06-20-10-47-33.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00574/f00574_2013-06-20-10-48-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00575/f00575_2013-06-20-10-48-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00576/f00576_2013-06-20-10-48-42.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00577/f00577_2013-06-20-10-48-48.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00587/f00587_2013-06-27-10-57-08.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00588/f00588_2013-06-27-10-57-15.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00590/f00590_2013-06-27-10-57-36.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00591/f00591_2013-06-27-10-57-42.json',
#'/home/vburns/Dropbox/ConchisData/2013-06-27/f00592/f00592_2013-06-27-10-57-51.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00593/f00593_2013-06-27-13-45-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00594/f00594_2013-06-27-13-45-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00595/f00595_2013-06-27-13-45-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00596/f00596_2013-06-27-13-45-29.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00597/f00597_2013-06-27-13-47-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00598/f00598_2013-06-27-13-47-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00599/f00599_2013-06-27-13-47-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00600/f00600_2013-06-27-13-47-20.json',
]
e_safe_shockwater_shock = aba.loadMultipleDataFiles(e_safe_shockwater_shock)

e_safe_shockwater_sec = [
# '/home/vburns/Dropbox/ConchisData/2013-06-19/f00554/f00554_2013-06-19-11-48-29.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-19/f00555/f00555_2013-06-19-11-48-37.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00556/f00556_2013-06-19-11-48-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00557/f00557_2013-06-19-11-49-03.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-19/f00558/f00558_2013-06-19-11-51-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00559/f00559_2013-06-19-11-51-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00560/f00560_2013-06-19-11-51-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00561/f00561_2013-06-19-11-51-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00570/f00570_2013-06-20-11-42-36.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00571/f00571_2013-06-20-11-42-33.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00572/f00572_2013-06-20-11-42-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00573/f00573_2013-06-20-11-42-07.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00574/f00574_2013-06-20-11-45-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00575/f00575_2013-06-20-11-45-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00576/f00576_2013-06-20-11-45-38.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00577/f00577_2013-06-20-11-45-50.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00587/f00587_2013-06-27-11-50-01.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00588/f00588_2013-06-27-11-49-59.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00590/f00590_2013-06-27-11-51-51.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00591/f00591_2013-06-27-11-51-58.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00592/f00592_2013-06-27-11-52-04.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00593/f00593_2013-06-27-14-39-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00594/f00594_2013-06-27-14-39-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00595/f00595_2013-06-27-14-39-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00596/f00596_2013-06-27-14-39-43.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-27/f00597/f00597_2013-06-27-14-42-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00598/f00598_2013-06-27-14-42-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00599/f00599_2013-06-27-14-42-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-27/f00600/f00600_2013-06-27-14-42-28.json',
]
e_safe_shockwater_sec = aba.loadMultipleDataFiles(e_safe_shockwater_sec)

e_shock_safewater_first = [
#'/home/vburns/Dropbox/ConchisData/2013-06-19/f00562/f00562_2013-06-19-12-41-20.json', #current imbalance
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00563/f00563_2013-06-19-12-40-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00564/f00564_2013-06-19-12-40-35.json', #potential tracking issue in post
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00565/f00565_2013-06-19-12-40-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00566/f00566_2013-06-19-12-42-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00567/f00567_2013-06-19-12-42-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00568/f00568_2013-06-19-12-42-31.json',#potential tracking in post
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00569/f00569_2013-06-19-12-42-38.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00578/f00578_2013-06-20-12-34-00.json',#tracking in shock
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00579/f00579_2013-06-20-12-34-04.json',#low starting velocity
#'/home/vburns/Dropbox/ConchisData/2013-06-20/f00580/f00580_2013-06-20-12-34-12.json',#low starting velocity
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00581/f00581_2013-06-20-12-34-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00582/f00582_2013-06-20-12-35-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00583/f00583_2013-06-20-12-34-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00584/f00584_2013-06-20-12-34-44.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00585/f00585_2013-06-20-12-34-42.json', #potential tracking in post
]
e_shock_safewater_first = aba.loadMultipleDataFiles(e_shock_safewater_first)

e_shock_safewater_shock = [
# '/home/vburns/Dropbox/ConchisData/2013-06-19/f00562/f00562_2013-06-19-13-13-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00563/f00563_2013-06-19-13-13-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00564/f00564_2013-06-19-13-13-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00565/f00565_2013-06-19-13-13-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00566/f00566_2013-06-19-13-13-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00567/f00567_2013-06-19-13-14-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00568/f00568_2013-06-19-13-14-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00569/f00569_2013-06-19-13-14-11.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00578/f00578_2013-06-20-13-05-49.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00579/f00579_2013-06-20-13-05-56.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00580/f00580_2013-06-20-13-06-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00581/f00581_2013-06-20-13-06-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00582/f00582_2013-06-20-13-07-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00583/f00583_2013-06-20-13-07-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00584/f00584_2013-06-20-13-07-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00585/f00585_2013-06-20-13-07-24.json',
]
e_shock_safewater_shock = aba.loadMultipleDataFiles(e_shock_safewater_shock)

e_shock_safewater_sec = [
# '/home/vburns/Dropbox/ConchisData/2013-06-19/f00562/f00562_2013-06-19-14-09-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00563/f00563_2013-06-19-14-09-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00564/f00564_2013-06-19-14-09-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00565/f00565_2013-06-19-14-10-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00566/f00566_2013-06-19-14-14-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00567/f00567_2013-06-19-14-14-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00568/f00568_2013-06-19-14-14-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-19/f00569/f00569_2013-06-19-14-15-05.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00578/f00578_2013-06-20-14-01-51.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00579/f00579_2013-06-20-14-01-40.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-20/f00580/f00580_2013-06-20-14-01-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00581/f00581_2013-06-20-14-01-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00582/f00582_2013-06-20-14-05-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00583/f00583_2013-06-20-14-05-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00584/f00584_2013-06-20-14-04-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-20/f00585/f00585_2013-06-20-14-04-49.json',
]
e_shock_safewater_sec = aba.loadMultipleDataFiles(e_shock_safewater_sec)

#velocity analysis 
sm = 15; #smooth over 15 frames.

endWinLen = 5 * 60; #seconds

eBaseVel5_1a = aba.getMedianVelMulti(e_first, (0,900), smoothWinLen = sm)
eBaseVel5_1b = aba.getMedianVelMulti(e_first, (900,1800), smoothWinLen = sm)
cBaseVel_1a = aba.getMedianVelMulti(c_first, (0,900), smoothWinLen = sm)
cBaseVel_1b = aba.getMedianVelMulti(c_first, (900,1800), smoothWinLen = sm)

eBaseVel5_2a = aba.getMedianVelMulti(e_sec, (0,900), smoothWinLen = sm)
eBaseVel5_2b = aba.getMedianVelMulti(e_sec, (900,1800), smoothWinLen = sm)
cBaseVel_2a = aba.getMedianVelMulti(c_sec, (0,900), smoothWinLen = sm)
cBaseVel_2b = aba.getMedianVelMulti(c_sec, (900,1800), smoothWinLen = sm)

eBaseVelW_1a = aba.getMedianVelMulti(e_water_first, (0,900), smoothWinLen = sm)
eBaseVelW_1b = aba.getMedianVelMulti(e_water_first, (900,1800), smoothWinLen = sm)
eBaseVelW_2a = aba.getMedianVelMulti(e_water_sec, (0,900), smoothWinLen = sm)
eBaseVelW_2b = aba.getMedianVelMulti(e_water_sec, (900,1800), smoothWinLen = sm)
eBaseW = aba.getMedianVelMulti(e_water_shock, (0,900), smoothWinLen=sm)
eEndVelW = aba.getMedianVelMulti(e_water_shock, tRange=[-endWinLen,-0], smoothWinLen=sm)

#SW is safe tank with shock water
eBaseVelSW_1a = aba.getMedianVelMulti(e_safe_shockwater_first, (0,900), smoothWinLen = sm)
eBaseVelSW_1b = aba.getMedianVelMulti(e_safe_shockwater_first, (900,1800), smoothWinLen = sm)
eBaseVelSW_2a = aba.getMedianVelMulti(e_safe_shockwater_sec, (0,900), smoothWinLen = sm)
eBaseVelSW_2b = aba.getMedianVelMulti(e_safe_shockwater_sec, (900,1800), smoothWinLen = sm)
eBaseSW = aba.getMedianVelMulti(e_safe_shockwater_shock, (0,900), smoothWinLen=sm)
eEndVelSW = aba.getMedianVelMulti(e_safe_shockwater_shock, tRange=[-endWinLen,-0], smoothWinLen=sm)

#ssw is shock tank with safe water
eBaseVelSSW_1a = aba.getMedianVelMulti(e_shock_safewater_first, (0,900), smoothWinLen = sm)
eBaseVelSSW_1b = aba.getMedianVelMulti(e_shock_safewater_first, (900,1800), smoothWinLen = sm)
eBaseVelSSW_2a = aba.getMedianVelMulti(e_shock_safewater_sec, (0,900), smoothWinLen = sm)
eBaseVelSSW_2b = aba.getMedianVelMulti(e_shock_safewater_sec, (900,1800), smoothWinLen = sm)
eBaseSSW = aba.getMedianVelMulti(e_shock_safewater_shock, (0,900), smoothWinLen=sm)
eEndVelSSW = aba.getMedianVelMulti(e_shock_safewater_shock, tRange=[-endWinLen,-0], smoothWinLen=sm)

eBase5 = aba.getMedianVelMulti(e_shock, (0, 900), smoothWinLen = sm)
cBase = aba.getMedianVelMulti(c_shock, (0, 900), smoothWinLen = sm)
eEndVel5 = aba.getMedianVelMulti(e_shock, tRange=[-endWinLen,-0], smoothWinLen=sm)
cEndVel = aba.getMedianVelMulti(c_shock, tRange=[-endWinLen,-0], smoothWinLen = sm)
eBaseSame_1a = aba.getMedianVelMulti(e_same_first, (0, 900), smoothWinLen = sm)
eBaseSame_1b = aba.getMedianVelMulti(e_same_first, (900, 1800), smoothWinLen = sm)
eBaseShockSame = aba.getMedianVelMulti(e_same_shock, (0, 900), smoothWinLen = sm)
eEndShockSame = aba.getMedianVelMulti(e_same_shock, tRange=[-endWinLen, -0], smoothWinLen = sm)
eBaseSame_2a = aba.getMedianVelMulti(e_same_sec, (0, 900), smoothWinLen = sm)
eBaseSame_2b = aba.getMedianVelMulti(e_same_sec, (900, 1800), smoothWinLen = sm)

#comparisons 
[tv, control_experimental_start] = scipy.stats.ttest_ind(cBaseVel_1a, eBaseVel5_1a)
[tv, control_experimentalsame_start] = scipy.stats.ttest_ind(cBaseVel_1a, eBaseSame_1a)
[tv, experimental_experimentalsame_start] = scipy.stats.ttest_ind(eBaseVel5_1a, eBaseSame_1a)

[tv, control_experimental] = scipy.stats.ttest_ind(cBaseVel_2b, eBaseVel5_2b)
[tv, control_experimentalsame] = scipy.stats.ttest_ind(cBaseVel_2b, eBaseSame_2b)
[tv, experimental_experimentalsame] = scipy.stats.ttest_ind(eBaseVel5_2b, eBaseSame_2b)

[tv, control_experimental_start1b] = scipy.stats.ttest_ind(cBaseVel_1b, eBaseVel5_1b)
[tv, control_experimentalsame_start1b] = scipy.stats.ttest_ind(cBaseVel_1b, eBaseSame_1b)
[tv, experimental_experimentalsame_start1b] = scipy.stats.ttest_ind(eBaseVel5_1b, eBaseSame_1b)

[tv, control_experimental2a] = scipy.stats.ttest_ind(cBaseVel_2a, eBaseVel5_2a)
[tv, control_experimentalsame2a] = scipy.stats.ttest_ind(cBaseVel_2a, eBaseSame_2a)
[tv, experimental_experimentalsame2a] = scipy.stats.ttest_ind(eBaseVel5_2a, eBaseSame_2a)

[tv, control_water] = scipy.stats.ttest_ind(cBaseVel_2b, eBaseVelW_2b)
[tv, waterend_waterfinal] = scipy.stats.ttest_ind(eBaseW, eBaseVelW_2b)
[tv, waterend_experimental] = scipy.stats.ttest_ind(eBaseVelW_2b, eBaseVel5_2b)
[tv, waterend_experimentalsame] =scipy.stats.ttest_ind(eBaseVelW_2b, eBaseSame_2b)

[tv, control_waterrotateS] = scipy.stats.ttest_ind(cBaseVel_2b, eBaseVelSW_2b)
[tv, waterend_waterfinalR] = scipy.stats.ttest_ind(eBaseVelSW_2b, eBaseVel5_2b)
[tv, waterend_experimentalR] = scipy.stats.ttest_ind(eBaseVelSW_2b, eBaseSame_2b)

[tv, control_waterrotateD] = scipy.stats.ttest_ind(cBaseVel_2b, eBaseVelSSW_2b)
[tv, waterend_experimentalD] = scipy.stats.ttest_ind(eBaseVelSSW_2b, eBaseVel5_2b)
[tv, waterend_experimentalsameD] = scipy.stats.ttest_ind(eBaseVelSSW_2b, eBaseSame_2b)

[tv, exper5shock_end] = scipy.stats.ttest_ind(eEndVel5, eBaseVel5_2b)
[tv, experSameshock_end] = scipy.stats.ttest_ind(eEndShockSame, eBaseSame_2b)
[tv, controlshock_end] = scipy.stats.ttest_ind(cEndVel, cBaseVel_2b)
[tv, exper5shock_end_control] = scipy.stats.ttest_ind(eEndVel5, cEndVel)
[tv, experSameshock_end_control] = scipy.stats.ttest_ind(eEndShockSame, cEndVel)
[tv, experimental_control_endshock] = scipy.stats.ttest_ind(eEndVel5, cEndVel)


print 'end shock com', exper5shock_end_control
print 'end vel control/exper, control/same',control_experimental, control_experimentalsame
print 'end vel exper/exper', experimental_experimentalsame

print 'safe tank, shock water',len(eBaseVelSW_1a)
print 'shock tank, safe water',len(eBaseVelSSW_1a)
print 'safe tank, shock water to experimental at end', waterend_waterfinalR
print 'shock tank, safe water to experimental at end',waterend_experimentalD


#fix
#eEndVel25[2]= np.nan

#convert to array
eBV5_1a = np.array([np.array([eBaseVel5_1a[n]]) for n in range(len(eBaseVel5_1a))])
eBV5_1b = np.array([np.array([eBaseVel5_1b[n]]) for n in range(len(eBaseVel5_1b))])
cBV_1a = np.array([np.array([cBaseVel_1a[n]]) for n in range(len(cBaseVel_1a))])
cBV_1b = np.array([np.array([cBaseVel_1b[n]]) for n in range(len(cBaseVel_1b))])

eBV5_2a = np.array([np.array([eBaseVel5_2a[n]]) for n in range(len(eBaseVel5_2a))])
eBV5_2b = np.array([np.array([eBaseVel5_2b[n]]) for n in range(len(eBaseVel5_2b))])
cBV_2a = np.array([np.array([cBaseVel_2a[n]]) for n in range(len(cBaseVel_2a))])
cBV_2b = np.array([np.array([cBaseVel_2b[n]]) for n in range(len(cBaseVel_2b))])

eSV5 = np.array([np.array([eBase5[n]]) for n in range(len(eBase5))])
cSV = np.array([np.array([cBase[n]]) for n in range(len(cBase))])

eEV5 = np.array([np.array([eEndVel5[n]]) for n in range(len(eEndVel5))])
cEV = np.array([np.array([cEndVel[n]]) for n in range(len(cEndVel))])

eBVS_1a = np.array([np.array([eBaseSame_1a[n]]) for n in range(len(eBaseSame_1a))])
eBVS_1b = np.array([np.array([eBaseSame_1b[n]]) for n in range(len(eBaseSame_1b))])
eSVS = np.array([np.array([eBaseShockSame[n]]) for n in range(len(eBaseShockSame))])
eEVS = np.array([np.array([eEndShockSame[n]]) for n in range(len(eEndShockSame))])
eBVS_2a = np.array([np.array([eBaseSame_2a[n]]) for n in range(len(eBaseSame_2a))])
eBVS_2b = np.array([np.array([eBaseSame_2b[n]]) for n in range(len(eBaseSame_2b))])

eBVW_1a = np.array([np.array([eBaseVelW_1a[n]]) for n in range(len(eBaseVelW_1a))])
eBVW_1b = np.array([np.array([eBaseVelW_1b[n]]) for n in range(len(eBaseVelW_1b))])
eBVW_2a = np.array([np.array([eBaseVelW_2a[n]]) for n in range(len(eBaseVelW_2a))])
eBVW_2b = np.array([np.array([eBaseVelW_2b[n]]) for n in range(len(eBaseVelW_2b))])
eSVW = np.array([np.array([eBaseW[n]]) for n in range(len(eBaseW))])
eEVW = np.array([np.array([eEndVelW[n]]) for n in range(len(eEndVelW))])

eBVSW_1a = np.array([np.array([eBaseVelSW_1a[n]]) for n in range(len(eBaseVelSW_1a))])
eBVSW_1b = np.array([np.array([eBaseVelSW_1b[n]]) for n in range(len(eBaseVelSW_1b))])
eBVSW_2a = np.array([np.array([eBaseVelSW_2a[n]]) for n in range(len(eBaseVelSW_2a))])
eBVSW_2b = np.array([np.array([eBaseVelSW_2b[n]]) for n in range(len(eBaseVelSW_2b))])
eSVSW = np.array([np.array([eBaseSW[n]]) for n in range(len(eBaseSW))])
eEVSW = np.array([np.array([eEndVelSW[n]]) for n in range(len(eEndVelSW))])

eBVSSW_1a = np.array([np.array([eBaseVelSSW_1a[n]]) for n in range(len(eBaseVelSSW_1a))])
eBVSSW_1b = np.array([np.array([eBaseVelSSW_1b[n]]) for n in range(len(eBaseVelSSW_1b))])
eBVSSW_2a = np.array([np.array([eBaseVelSSW_2a[n]]) for n in range(len(eBaseVelSSW_2a))])
eBVSSW_2b = np.array([np.array([eBaseVelSSW_2b[n]]) for n in range(len(eBaseVelSSW_2b))])
eSVSSW = np.array([np.array([eBaseSSW[n]]) for n in range(len(eBaseSSW))])
eEVSSW = np.array([np.array([eEndVelSSW[n]]) for n in range(len(eEndVelSSW))])

experimental5 = np.transpose(np.hstack((eBV5_1a, eBV5_1b, eSV5, eEV5, eBV5_2a, eBV5_2b)))
experimentalsame = np.transpose(np.hstack((eBVS_1a, eBVS_1b, eSVS, eEVS, eBVS_2a, eBVS_2b)))
experimentalwater = np.transpose(np.hstack((eBVW_1a, eBVW_1b, eSVW, eEVW, eBVW_2a, eBVW_2b)))
experimentalsafeshockwater = np.transpose(np.hstack((eBVSW_1a, eBVSW_1b, eSVSW, eEVSW, eBVSW_2a, eBVSW_2b)))
experimentalshocksafewater = np.transpose(np.hstack((eBVSSW_1a, eBVSSW_1b, eSVSSW, eEVSSW, eBVSSW_2a, eBVSSW_2b)))
control = np.transpose(np.hstack((cBV_1a, cBV_1b, cSV, cEV, cBV_2a, cBV_2b)))
'''
pylab.figure()
pylab.suptitle('Learned Helplessness Assay at 5V - Safe, Shocking, Safe')
ax = pylab.subplot(1,3,1)
pylab.plot(control)
pylab.plot(0, [cBaseVel_1a], 'r.')
pylab.plot(1, [cBaseVel_1b], 'r.')
pylab.plot(2,[cBase],'r.')
pylab.plot(3, [cEndVel], 'r.')
pylab.plot(4, [cBaseVel_2a], 'r.')
pylab.plot(5, [cBaseVel_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],'o-k',lw=3)
yerr = (2*scipy.stats.sem(cBaseVel_1a), 2*scipy.stats.sem(cBaseVel_1b), 2*scipy.stats.sem(cBase), 2*scipy.stats.sem(cEndVel), 2*scipy.stats.sem(cBaseVel_2a), 2*scipy.stats.sem(cBaseVel_2b))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],fmt='ok',yerr=yerr, lw=3)
#ax.set_xticks((0,1,2,3,4,5))
#ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Speed (mm/s)')
pylab.title('Control fish')
ax.set_yticks([0.0,1.0,2.0,3.0,4.0,5.0])
ax.set_xticklabels([])
pylab.axvline(x=1.5, color = 'k', lw=3, ls='dashed')
pylab.axvline(x=3.5, color = 'k', lw=3, ls='dashed')
patch3 = mpl.patches.Rectangle((2.25,0), .5, 10, color=[1,.5,.5], fill=True)
pyplot.gca().add_patch(patch3)
ax = pylab.subplot(1,3,2)
pylab.plot(experimental5)
pylab.plot(0, [eBaseVel5_1a], 'r.')
pylab.plot(1, [eBaseVel5_1b], 'r.')
pylab.plot(2,[eBase5],'r.')
pylab.plot(3, [eEndVel5], 'r.')
pylab.plot(4, [eBaseVel5_2a], 'r.')
pylab.plot(5, [eBaseVel5_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],'o-k', lw=3)
yerr5 = (2*scipy.stats.sem(eBaseVel5_1a), 2*scipy.stats.sem(eBaseVel5_1b), 2*scipy.stats.sem(eBase5), 2*scipy.stats.sem(eEndVel5), 2*scipy.stats.sem(eBaseVel5_2a), 2*scipy.stats.sem(eBaseVel5_2b))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],fmt='ok', yerr=yerr5, lw=3)
#ax.set_xticks((0,1,2,3,4,5))
#ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.title('Experimental fish')
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Speed (mm/s)')
ax.set_yticks([0.0,1.0,2.0,3.0,4.0,5.0])
ax.set_xticklabels([])
pylab.axvline(x=1.5, color = 'k', lw=3, ls='dashed')
pylab.axvline(x=3.5, color = 'k', lw=3, ls='dashed')
patch4 = mpl.patches.Rectangle((2.25,0), .5, 10, color=[1,.5,.5], fill=True)
pyplot.gca().add_patch(patch4)
ax = pylab.subplot(1,3,3)
pylab.plot(experimentalsame)
pylab.plot(0, [eBaseSame_1a], 'r.')
pylab.plot(1, [eBaseSame_1b], 'r.')
pylab.plot(2,[eBaseShockSame],'r.')
pylab.plot(3, [eEndShockSame], 'r.')
pylab.plot(4, [eBaseSame_2a], 'r.')
pylab.plot(5, [eBaseSame_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)],'o-k', lw=3)
yerrS = (2*scipy.stats.sem(eBaseSame_1a), 2*scipy.stats.sem(eBaseSame_1b), 2*scipy.stats.sem(eBaseShockSame), 2*scipy.stats.sem(eEndShockSame), 2*scipy.stats.sem(eBaseSame_2a), 2*scipy.stats.sem(eBaseSame_2b))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)], lw=3,fmt='ok', yerr=yerrS)
#ax.set_xticks((0,1,2,3,4,5))
#ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Speed (mm/s)')
pylab.title('Experimental fish')
ax.set_yticks([0.0,1.0,2.0,3.0,4.0,5.0])
ax.set_xticklabels([])
pylab.axvline(x=1.5, color = 'k', lw=3, ls='dashed')
pylab.axvline(x=3.5, color = 'k', lw=3, ls='dashed')
patch5 = mpl.patches.Rectangle((2.25,0), .5, 10, color=[1,.5,.5], fill=True)
pyplot.gca().add_patch(patch5)
'''
'''
pylab.figure()
pylab.suptitle('Learned Helplessness Assay at 5V - Safe, Shocking, Safe')
ax = pylab.subplot(1,3,1)
pylab.plot(experimentalwater)
pylab.plot(0, [eBaseVelW_1a], 'r.')
pylab.plot(1, [eBaseVelW_1b], 'r.')
pylab.plot(2,[eBaseW],'r.')
pylab.plot(3, [eEndVelW], 'r.')
pylab.plot(4, [eBaseVelW_2a], 'r.')
pylab.plot(5, [eBaseVelW_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseVelW_1a), np.mean(eBaseVelW_1b), np.mean(eBaseW), np.mean(eEndVelW), np.mean(eBaseVelW_2a), np.mean(eBaseVelW_2b)],'o-k', lw=3)
yerrW = (2*scipy.stats.sem(eBaseVelW_1a), 2*scipy.stats.sem(eBaseVelW_1b), 2*scipy.stats.sem(eBaseW), 2*scipy.stats.sem(eEndVelW), 2*scipy.stats.sem(eBaseVelW_2a), 2*scipy.stats.sem(eBaseVelW_2b))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelW_1a), np.mean(eBaseVelW_1b), np.mean(eBaseW), np.mean(eEndVelW), np.mean(eBaseVelW_2a), np.mean(eBaseVelW_2b)],fmt='ok', yerr=yerrW, lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline\n shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V (new water)')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,3,2)
pylab.plot(experimentalsafeshockwater)
pylab.plot(0, [eBaseVelSW_1a], 'r.')
pylab.plot(1, [eBaseVelSW_1b], 'r.')
pylab.plot(2,[eBaseSW],'r.')
pylab.plot(3, [eEndVelSW], 'r.')
pylab.plot(4, [eBaseVelSW_2a], 'r.')
pylab.plot(5, [eBaseVelSW_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseVelSW_1a), np.mean(eBaseVelSW_1b), np.mean(eBaseSW), np.mean(eEndVelSW), np.mean(eBaseVelSW_2a), np.mean(eBaseVelSW_2b)],'o-k', lw=3)
yerrSW = (2*scipy.stats.sem(eBaseVelSW_1a), 2*scipy.stats.sem(eBaseVelSW_1b), 2*scipy.stats.sem(eBaseSW), 2*scipy.stats.sem(eEndVelSW), 2*scipy.stats.sem(eBaseVelSW_2a), 2*scipy.stats.sem(eBaseVelSW_2b))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelSW_1a), np.mean(eBaseVelSW_1b), np.mean(eBaseSW), np.mean(eEndVelSW), np.mean(eBaseVelSW_2a), np.mean(eBaseVelSW_2b)],fmt='ok', yerr=yerrSW, lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline\n shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V (safe tank/shock water)')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,3,3)
pylab.plot(experimentalshocksafewater)
pylab.plot(0, [eBaseVelSSW_1a], 'r.')
pylab.plot(1, [eBaseVelSSW_1b], 'r.')
pylab.plot(2,[eBaseSSW],'r.')
pylab.plot(3, [eEndVelSSW], 'r.')
pylab.plot(4, [eBaseVelSSW_2a], 'r.')
pylab.plot(5, [eBaseVelSSW_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseVelSSW_1a), np.mean(eBaseVelSSW_1b), np.mean(eBaseSSW), np.mean(eEndVelSSW), np.mean(eBaseVelSSW_2a), np.mean(eBaseVelSSW_2b)],'o-k', lw=3)
yerrSSW = (2*scipy.stats.sem(eBaseVelSSW_1a), 2*scipy.stats.sem(eBaseVelSSW_1b), 2*scipy.stats.sem(eBaseSSW), 2*scipy.stats.sem(eEndVelSSW), 2*scipy.stats.sem(eBaseVelSSW_2a), 2*scipy.stats.sem(eBaseVelSSW_2b))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelSSW_1a), np.mean(eBaseVelSSW_1b), np.mean(eBaseSSW), np.mean(eEndVelSSW), np.mean(eBaseVelSSW_2a), np.mean(eBaseVelSSW_2b)],fmt='ok', yerr=yerrSSW, lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline\n shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V (shock tank/safe water)')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
'''

yerr = (scipy.stats.sem(cBaseVel_1a), scipy.stats.sem(cBaseVel_1b), scipy.stats.sem(cBase), scipy.stats.sem(cEndVel), scipy.stats.sem(cBaseVel_2a), scipy.stats.sem(cBaseVel_2b))
yerr5 = (scipy.stats.sem(eBaseVel5_1a), scipy.stats.sem(eBaseVel5_1b), scipy.stats.sem(eBase5), scipy.stats.sem(eEndVel5), scipy.stats.sem(eBaseVel5_2a), scipy.stats.sem(eBaseVel5_2b))
yerrS = (scipy.stats.sem(eBaseSame_1a), scipy.stats.sem(eBaseSame_1b), scipy.stats.sem(eBaseShockSame), scipy.stats.sem(eEndShockSame), scipy.stats.sem(eBaseSame_2a), scipy.stats.sem(eBaseSame_2b))
yerrW = (scipy.stats.sem(eBaseVelW_1a), scipy.stats.sem(eBaseVelW_1b), scipy.stats.sem(eBaseW), scipy.stats.sem(eEndVelW), scipy.stats.sem(eBaseVelW_2a), scipy.stats.sem(eBaseVelW_2b))
yerrSW = (scipy.stats.sem(eBaseVelSW_1a), scipy.stats.sem(eBaseVelSW_1b), scipy.stats.sem(eBaseSW), scipy.stats.sem(eEndVelSW), scipy.stats.sem(eBaseVelSW_2a), scipy.stats.sem(eBaseVelSW_2b))
yerrSSW = (scipy.stats.sem(eBaseVelSSW_1a), scipy.stats.sem(eBaseVelSSW_1b), scipy.stats.sem(eBaseSSW), scipy.stats.sem(eEndVelSSW), scipy.stats.sem(eBaseVelSSW_2a), scipy.stats.sem(eBaseVelSSW_2b))


fig = pylab.figure(100, figsize=(6,5))
#pylab.suptitle('Summary of Median Velocities (mm/s)')
ax = pylab.subplot(1,1,1)
control = ax.plot([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],'o-k', lw=3, label='Control Fish: No shocking and safe=nonshock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],fmt='ok',yerr=yerr, lw=3)
experimental5 = ax.plot([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],'o-b', lw=3, label='Experimental Fish (5V): Safe=nonshock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],fmt='ob', yerr=yerr5, lw=3)
experimentalsame = ax.plot([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)],'o-r', lw=3, label='Experimental Fish (5V): Safe=shock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)], lw=3,fmt='or', yerr=yerrS)

experimentalsafeshockwater = ax.plot([0,1,2,3,4,5],[np.mean(eBaseVelSW_1a), np.mean(eBaseVelSW_1b), np.mean(eBaseSW), np.mean(eEndVelSW), np.mean(eBaseVelSW_2a), np.mean(eBaseVelSW_2b)],'o-c', lw=3, label='Experimental Fish (5V): Safe=nonshock tank with own shocking water')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelSW_1a), np.mean(eBaseVelSW_1b), np.mean(eBaseSW), np.mean(eEndVelSW), np.mean(eBaseVelSW_2a), np.mean(eBaseVelSW_2b)],fmt='oc', yerr=yerrSW, lw=3)
experimentalshocksafewater = ax.plot([0,1,2,3,4,5],[np.mean(eBaseVelSSW_1a), np.mean(eBaseVelSSW_1b), np.mean(eBaseSSW), np.mean(eEndVelSSW), np.mean(eBaseVelSSW_2a), np.mean(eBaseVelSSW_2b)],'o-y', lw=3, label='Experimental Fish (5V): Safe=shock tank with own safe water')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelSSW_1a), np.mean(eBaseVelSSW_1b), np.mean(eBaseSSW), np.mean(eEndVelSSW), np.mean(eBaseVelSSW_2a), np.mean(eBaseVelSSW_2b)],fmt='oy', yerr=yerrSSW, lw=3)

#handles, labels=ax.get_legend_handles_labels()
#ax.legend(handles, labels)
#ax.set_xticks((0,1,2,3,4,5))
#ax.set_xticklabels(('0-15 min \n neutral tank', '15-30 min \n neutral tank', 'first 15 min \n shock tank', 'last 5 min \n shock tank', '0-15 min \n test tank', '15-30 min \n test tank'))
pylab.xlim((-.25,5.25))
pylab.ylim((0,4))
pylab.ylabel('Median Speed (mm/s)')
ax.set_yticks([0.0,1.0,2.0,3.0,4.0])
ax.set_xticklabels([])
pylab.axvline(x=1.5, color = 'k', lw=3, ls='dashed')
pylab.axvline(x=3.5, color = 'k', lw=3, ls='dashed')
patch3 = mpl.patches.Rectangle((2.25,0), .5, 10, color=[1,.5,.5], fill=True)
pyplot.gca().add_patch(patch3)

fig = pylab.figure(101, figsize=(6,3))
#pylab.suptitle('Summary of Median Velocities (mm/s)')
ax2 = pylab.subplot(1,1,1)
#control = ax2.plot([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],'o-k', lw=3, label='Control Fish: Safe = colored')
#pyplot.errorbar([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],fmt='ok',yerr=yerr, lw=3)
experimental5 = ax2.plot([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],'o-b', lw=3, label='Experimental Fish (5V): Safe=nonshock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],fmt='ob', yerr=yerr5, lw=3)
experimentalsame = ax2.plot([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)],'o-r', lw=3, label='Experimental Fish (5V): Safe=shock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)], lw=3,fmt='or', yerr=yerrS)
#experimentalwater = ax2.plot([0,1,2,3,4,5],[np.mean(eBaseVelW_1a), np.mean(eBaseVelW_1b), np.mean(eBaseW), np.mean(eEndVelW), np.mean(eBaseVelW_2a), np.mean(eBaseVelW_2b)],'o-m', lw=3, label='Experimental Fish (5V): Safe=shock tank with new water')
#pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelW_1a), np.mean(eBaseVelW_1b), np.mean(eBaseW), np.mean(eEndVelW), np.mean(eBaseVelW_2a), np.mean(eBaseVelW_2b)],fmt='om', yerr=yerrW, lw=3)
experimentalsafeshockwater = ax2.plot([0,1,2,3,4,5],[np.mean(eBaseVelSW_1a), np.mean(eBaseVelSW_1b), np.mean(eBaseSW), np.mean(eEndVelSW), np.mean(eBaseVelSW_2a), np.mean(eBaseVelSW_2b)],'o-c', lw=3, label='Experimental Fish (5V): Safe=nonshock tank with own shocking water')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelSW_1a), np.mean(eBaseVelSW_1b), np.mean(eBaseSW), np.mean(eEndVelSW), np.mean(eBaseVelSW_2a), np.mean(eBaseVelSW_2b)],fmt='oc', yerr=yerrSW, lw=3)
experimentalshocksafewater = ax2.plot([0,1,2,3,4,5],[np.mean(eBaseVelSSW_1a), np.mean(eBaseVelSSW_1b), np.mean(eBaseSSW), np.mean(eEndVelSSW), np.mean(eBaseVelSSW_2a), np.mean(eBaseVelSSW_2b)],'o-y', lw=3, label='Experimental Fish (5V): Safe=shock tank with own safe water')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelSSW_1a), np.mean(eBaseVelSSW_1b), np.mean(eBaseSSW), np.mean(eEndVelSSW), np.mean(eBaseVelSSW_2a), np.mean(eBaseVelSSW_2b)],fmt='oy', yerr=yerrSSW, lw=3)
#handles1, labels1 = ax2.get_legend_handles_labels()
#ax2.legend(handles1, labels1)
#ax2.set_xticks([])
#ax2.set_xticklabels(('0-15 min \n neutral tank', '15-30 min \n neutral tank', 'first 15 min \n shock tank', 'last 5 min \n shock tank', '0-15 min \n test tank', '15-30 min \n test tank'))
pylab.xlim((-.25,5.25))
ax2.set_xticklabels([])
pylab.ylim((0,4))
pylab.ylabel('Median Speed (mm/s)')
ax2.set_yticks([0.0,1.0,2.0,3.0,4.0])
pylab.axvline(x=1.5, color = 'k', lw=3, ls='dashed')
pylab.axvline(x=3.5, color = 'k', lw=3, ls='dashed')
patch4 = mpl.patches.Rectangle((2.25,0), .5, 10, color=[1,.5,.5], fill=True)
pyplot.gca().add_patch(patch4)

'''
pylab.figure()
pylab.suptitle('Summary of Median Velocities (mm/s)')
ax3 = pylab.subplot(1,1,1)
experimental5 = ax3.plot([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],'o-b', lw=3, label='Experimental Fish (5V): Safe=nonshock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],fmt='ob', yerr=yerr5, lw=3)
experimentalwater = ax3.plot([0,1,2,3,4,5],[np.mean(eBaseVelW_1a), np.mean(eBaseVelW_1b), np.mean(eBaseW), np.mean(eEndVelW), np.mean(eBaseVelW_2a), np.mean(eBaseVelW_2b)],'o-m', lw=3, label='Experimental Fish (5V): Safe=shock tank with new water')
experimentalsame = ax3.plot([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)],'o-r', lw=3, label='Experimental Fish (5V): Safe=shock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)], lw=3,fmt='or', yerr=yerrS)
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelW_1a), np.mean(eBaseVelW_1b), np.mean(eBaseW), np.mean(eEndVelW), np.mean(eBaseVelW_2a), np.mean(eBaseVelW_2b)],fmt='om', yerr=yerrW, lw=3)
handles1, labels1 = ax3.get_legend_handles_labels()
ax3.legend(handles1, labels1)
ax3.set_xticks((0,1,2,3,4,5))
ax3.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline\n shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
patch5 = mpl.patches.Rectangle((1.5,0), 2, 10, color='g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch5)
'''
pylab.show()

