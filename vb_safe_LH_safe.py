import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

#first is 30 min in safe tank, then standard shocking, then 30 min in safe tank
#note that currents from march were measured at 5ms, giving a lot of variation?
e_safe5_first= [
'/home/vburns/Dropbox/ConchisData/2013-03-29/f00239/f00239_2013-03-29-17-14-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00240/f00240_2013-03-29-17-14-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00241/f00241_2013-03-29-17-14-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00242/f00242_2013-03-29-17-14-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00243/f00243_2013-03-29-17-15-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00244/f00244_2013-03-29-17-15-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00245/f00245_2013-03-29-17-15-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00246/f00246_2013-03-29-17-15-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00366/f00366_2013-04-29-09-53-50.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00367/f00367_2013-04-29-09-53-47.json', #tracking poor (could be used inb)
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00368/f00368_2013-04-29-09-53-44.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00369/f00369_2013-04-29-09-53-42.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00370/f00370_2013-04-29-09-55-08.json', #weird high current readings
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00371/f00371_2013-04-29-09-55-10.json', #current imbalance
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00372/f00372_2013-04-29-09-55-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00373/f00373_2013-04-29-09-55-15.json',
]
e_safe5_first = aba.loadMultipleDataFiles(e_safe5_first)

e_shock5 = [
'/home/vburns/Dropbox/ConchisData/2013-03-29/f00239/f00239_2013-03-29-17-46-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00240/f00240_2013-03-29-17-46-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00241/f00241_2013-03-29-17-46-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00242/f00242_2013-03-29-17-46-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00243/f00243_2013-03-29-17-51-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00244/f00244_2013-03-29-17-51-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00245/f00245_2013-03-29-17-51-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00246/f00246_2013-03-29-17-51-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00366/f00366_2013-04-29-10-26-30.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00367/f00367_2013-04-29-10-26-37.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00368/f00368_2013-04-29-10-26-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00369/f00369_2013-04-29-10-26-53.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00370/f00370_2013-04-29-10-27-41.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00371/f00371_2013-04-29-10-27-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00372/f00372_2013-04-29-10-27-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00373/f00373_2013-04-29-10-27-56.json',
]
e_shock5 = aba.loadMultipleDataFiles(e_shock5)

e_safe5_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00239/f00239_2013-03-29-18-40-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00240/f00240_2013-03-29-18-40-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00241/f00241_2013-03-29-18-40-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00242/f00242_2013-03-29-18-40-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00243/f00243_2013-03-29-18-44-44.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00244/f00244_2013-03-29-18-44-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00245/f00245_2013-03-29-18-44-38.json', 
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00246/f00246_2013-03-29-18-44-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00366/f00366_2013-04-29-11-20-44.json', 
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00367/f00367_2013-04-29-11-20-38.json', 
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00368/f00368_2013-04-29-11-20-29.json', 
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00369/f00369_2013-04-29-11-20-23.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00370/f00370_2013-04-29-11-21-54.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00371/f00371_2013-04-29-11-21-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00372/f00372_2013-04-29-11-21-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00373/f00373_2013-04-29-11-21-37.json',
]
e_safe5_sec = aba.loadMultipleDataFiles(e_safe5_sec)

#fish kept in same tank
#12 has questionable tracking, but probably real
e_safe_same = [
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00358/f00358_2013-04-22-09-50-37.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-22/f00359/f00359_2013-04-22-09-50-23.json', #current imbalance
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00360/f00360_2013-04-22-09-50-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00361/f00361_2013-04-22-09-50-41.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-22/f00362/f00362_2013-04-22-09-48-34.json',#low starting velocity in second base
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00363/f00363_2013-04-22-09-48-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00364/f00364_2013-04-22-09-48-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00365/f00365_2013-04-22-09-48-27.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00374/f00374_2013-04-29-13-23-38.json', #tracking
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00375/f00375_2013-04-29-13-23-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00376/f00376_2013-04-29-13-23-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00377/f00377_2013-04-29-13-26-06.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00378/f00378_2013-04-29-13-27-22.json', #low starting velocity #and weird current #and tracking
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00379/f00379_2013-04-29-13-27-24.json', #current imbalance
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00380/f00380_2013-04-29-13-30-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00381/f00381_2013-04-29-13-30-24.json',
]
e_safe_same = aba.loadMultipleDataFiles(e_safe_same)

e_shock_same = [
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00358/f00358_2013-04-22-10-25-26.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-22/f00359/f00359_2013-04-22-10-25-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00360/f00360_2013-04-22-10-25-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00361/f00361_2013-04-22-10-25-41.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-22/f00362/f00362_2013-04-22-10-24-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00363/f00363_2013-04-22-10-24-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00364/f00364_2013-04-22-10-24-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00365/f00365_2013-04-22-10-24-52.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00374/f00374_2013-04-29-13-57-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00375/f00375_2013-04-29-13-57-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00376/f00376_2013-04-29-13-57-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00377/f00377_2013-04-29-13-57-36.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00378/f00378_2013-04-29-14-01-03.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00379/f00379_2013-04-29-14-01-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00380/f00380_2013-04-29-14-01-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00381/f00381_2013-04-29-14-01-23.json',
]
e_shock_same = aba.loadMultipleDataFiles(e_shock_same)

e_safe_same_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00358/f00358_2013-04-22-11-19-00.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-22/f00359/f00359_2013-04-22-11-19-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00360/f00360_2013-04-22-11-19-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00361/f00361_2013-04-22-11-19-25.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-22/f00362/f00362_2013-04-22-11-17-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00363/f00363_2013-04-22-11-17-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00364/f00364_2013-04-22-11-17-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00365/f00365_2013-04-22-11-18-03.json', 
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00374/f00374_2013-04-29-14-51-38.json', 
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00375/f00375_2013-04-29-14-51-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00376/f00376_2013-04-29-14-51-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00377/f00377_2013-04-29-14-50-50.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00378/f00378_2013-04-29-14-54-59.json', 
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00379/f00379_2013-04-29-14-54-03.json', 
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00380/f00380_2013-04-29-14-54-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00381/f00381_2013-04-29-14-54-36.json',
]
e_safe_same_sec = aba.loadMultipleDataFiles(e_safe_same_sec)

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

#note: fish 0, 1, 2, 3,4 seem to have current readings? not sure. They are very high 3A? Could be a measurement issue, including them but need to test if measureing 5ms after arduino on has some residual thing? nothing else wrong
c_safe_first = [
'/home/vburns/Dropbox/ConchisData/2013-03-30/f00255/f00255_2013-03-30-09-13-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00256/f00256_2013-03-30-09-13-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00257/f00257_2013-03-30-09-13-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00258/f00258_2013-03-30-09-13-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00259/f00259_2013-03-30-09-15-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00260/f00260_2013-03-30-09-15-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00261/f00261_2013-03-30-09-15-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00262/f00262_2013-03-30-09-15-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00382/f00382_2013-04-29-15-53-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00383/f00383_2013-04-29-15-53-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00384/f00384_2013-04-29-15-53-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00385/f00385_2013-04-29-15-53-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00386/f00386_2013-04-29-15-54-54.json', #has current when not supposed to? nothing else wrong
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00387/f00387_2013-04-29-15-54-52.json', #low starting velocity
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00388/f00388_2013-04-29-15-54-50.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00389/f00389_2013-04-29-15-54-47.json', #lost tracking
]
c_safe_first = aba.loadMultipleDataFiles(c_safe_first)

c_shock = [
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00255/f00255_2013-03-30-09-44-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00256/f00256_2013-03-30-09-44-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00257/f00257_2013-03-30-09-44-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00258/f00258_2013-03-30-09-44-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00259/f00259_2013-03-30-09-47-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00260/f00260_2013-03-30-09-47-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00261/f00261_2013-03-30-09-47-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00262/f00262_2013-03-30-09-47-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00382/f00382_2013-04-29-16-30-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00383/f00383_2013-04-29-16-30-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00384/f00384_2013-04-29-16-30-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00385/f00385_2013-04-29-16-30-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00386/f00386_2013-04-29-16-31-35.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00387/f00387_2013-04-29-16-31-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00388/f00388_2013-04-29-16-31-50.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00389/f00389_2013-04-29-16-32-03.json',
]
c_shock = aba.loadMultipleDataFiles(c_shock)
 
c_safe_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00255/f00255_2013-03-30-10-38-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00256/f00256_2013-03-30-10-38-23.json', 
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00257/f00257_2013-03-30-10-38-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00258/f00258_2013-03-30-10-38-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00259/f00259_2013-03-30-10-41-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00260/f00260_2013-03-30-10-41-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00261/f00261_2013-03-30-10-41-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00262/f00262_2013-03-30-10-41-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00382/f00382_2013-04-29-17-24-03.json', 
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00383/f00383_2013-04-29-17-23-55.json', 
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00384/f00384_2013-04-29-17-23-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00385/f00385_2013-04-29-17-23-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00386/f00386_2013-04-29-17-25-16.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00387/f00387_2013-04-29-17-25-08.json', 
 '/home/vburns/Dropbox/ConchisData/2013-04-29/f00388/f00388_2013-04-29-17-25-00.json',  
# '/home/vburns/Dropbox/ConchisData/2013-04-29/f00389/f00389_2013-04-29-17-24-54.json', 
]
c_safe_sec = aba.loadMultipleDataFiles(c_safe_sec)

#velocity analysis 
sm = 15; #smooth over 15 frames.

endWinLen = 5 * 60; #seconds

eBaseVel5_1a = aba.getMedianVelMulti(e_safe5_first, (0,900), smoothWinLen = sm)
eBaseVel5_1b = aba.getMedianVelMulti(e_safe5_first, (900,1800), smoothWinLen = sm)
cBaseVel_1a = aba.getMedianVelMulti(c_safe_first, (0,900), smoothWinLen = sm)
cBaseVel_1b = aba.getMedianVelMulti(c_safe_first, (900,1800), smoothWinLen = sm)

eBaseVel5_2a = aba.getMedianVelMulti(e_safe5_sec, (0,900), smoothWinLen = sm)
eBaseVel5_2b = aba.getMedianVelMulti(e_safe5_sec, (900,1800), smoothWinLen = sm)
cBaseVel_2a = aba.getMedianVelMulti(c_safe_sec, (0,900), smoothWinLen = sm)
cBaseVel_2b = aba.getMedianVelMulti(c_safe_sec, (900,1800), smoothWinLen = sm)

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

eBase5 = aba.getMedianVelMulti(e_shock5, (0, 900), smoothWinLen = sm)
cBase = aba.getMedianVelMulti(c_shock, (0, 900), smoothWinLen = sm)
eEndVel5 = aba.getMedianVelMulti(e_shock5, tRange=[-endWinLen,-0], smoothWinLen=sm)
cEndVel = aba.getMedianVelMulti(c_shock, tRange=[-endWinLen,-0], smoothWinLen = sm)
eBaseSame_1a = aba.getMedianVelMulti(e_safe_same, (0, 900), smoothWinLen = sm)
eBaseSame_1b = aba.getMedianVelMulti(e_safe_same, (900, 1800), smoothWinLen = sm)
eBaseShockSame = aba.getMedianVelMulti(e_shock_same, (0, 900), smoothWinLen = sm)
eEndShockSame = aba.getMedianVelMulti(e_shock_same, tRange=[-endWinLen, -0], smoothWinLen = sm)
eBaseSame_2a = aba.getMedianVelMulti(e_safe_same_sec, (0, 900), smoothWinLen = sm)
eBaseSame_2b = aba.getMedianVelMulti(e_safe_same_sec, (900, 1800), smoothWinLen = sm)

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


print 'Statistics comparing velocity between control and experimental (rec), control and experimental (same), and experimental (rec) and experimental (same) for first 15 min and last 15 min:', control_experimental_start, control_experimentalsame_start, experimental_experimentalsame_start, control_experimental, control_experimentalsame, experimental_experimentalsame
print 'Statistics comparing end shock to final velocity, 5V and same, control:', exper5shock_end, experSameshock_end, controlshock_end
print 'Statistics comparing control to new water at end, water end vel to water shock, water to experimental 5V at end, water to experimental same tank at end:', control_water, waterend_waterfinal, waterend_experimental, waterend_experimentalsame
print 'Statistics comparing experimental5 safe tank shocking water at end, experimental 5 to shock tank with safe water end:', waterend_waterfinalR, waterend_experimentalD
print 'Statistics comparing experimental5 same tank to safe tank shocking water at end, experimental 5 same tank to shock tank with safe water end:', waterend_experimentalR, waterend_experimentalsameD
print 'Statistic acclimation second  15 control to 5v:',control_experimental_start1b
print 'Statistic end of shock velocity control to experimental5v:', experimental_control_endshock


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
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Control Fish in Rec Tanks')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
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
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V (all rec tanks)')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
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
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V (stay in shocking tank)')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)

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

pylab.figure()
pylab.suptitle('Summary of Median Velocities (mm/s)')
ax = pylab.subplot(1,1,1)
control = ax.plot([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],'o-k', lw=3, label='Control Fish: No shocking and safe=nonshock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],fmt='ok',yerr=yerr, lw=3)
experimental5 = ax.plot([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],'o-b', lw=3, label='Experimental Fish (5V): Safe=nonshock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],fmt='ob', yerr=yerr5, lw=3)
experimentalsame = ax.plot([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)],'o-r', lw=3, label='Experimental Fish (5V): Safe=shock tank')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)], lw=3,fmt='or', yerr=yerrS)
handles, labels=ax.get_legend_handles_labels()
ax.legend(handles, labels)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline\n shock', 'last 5 min\n of shock', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
patch3 = mpl.patches.Rectangle((1.5,0), 2, 10, color='g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch3)

pylab.figure()
pylab.suptitle('Summary of Median Velocities (mm/s)')
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
handles1, labels1 = ax2.get_legend_handles_labels()
ax2.legend(handles1, labels1)
ax2.set_xticks((0,1,2,3,4,5))
ax2.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline\n shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
patch4 = mpl.patches.Rectangle((1.5,0), 2, 10, color='g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch4)

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
pylab.show()

