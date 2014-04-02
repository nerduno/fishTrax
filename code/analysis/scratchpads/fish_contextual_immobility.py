import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy
import os

#first is 30 min in safe tank, then standard shocking, then 30 min in safe tank
e_first= [
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
os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00414/f00414_2013-05-15-10-17-16.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00415/f00415_2013-05-15-10-17-24.json'), #low velocity in second base
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00416/f00416_2013-05-15-10-17-34.json'), #tracking
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00417/f00417_2013-05-15-10-17-43.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00418/f00418_2013-05-15-10-20-55.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00419/f00419_2013-05-15-10-20-58.json'), #low starting velocity
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00420/f00420_2013-05-15-10-21-03.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00421/f00421_2013-05-15-10-21-07.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00438/f00438_2013-05-16-14-13-03.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00439/f00439_2013-05-16-14-13-09.json'), #low velocity in second base
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00440/f00440_2013-05-16-14-13-20.json'), #tracking
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00441/f00441_2013-05-16-14-13-27.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00442/f00442_2013-05-16-14-16-16.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00444/f00444_2013-05-16-14-16-04.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00445/f00445_2013-05-16-14-15-59.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00446/f00446_2013-05-17-12-47-21.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00447/f00447_2013-05-17-12-47-23.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00448/f00448_2013-05-17-12-47-25.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00449/f00449_2013-05-17-12-47-27.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00450/f00450_2013-05-17-12-49-05.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00451/f00451_2013-05-17-12-49-07.json'), #current imbalance and tracking
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00452/f00452_2013-05-17-12-49-08.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00453/f00453_2013-05-17-12-49-10.json'),
]
e_first = aba.loadMultipleDataFiles(e_first)

e_shock = [
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
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00414/f00414_2013-05-15-10-49-21.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00415/f00415_2013-05-15-10-49-28.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00416/f00416_2013-05-15-10-49-35.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00417/f00417_2013-05-15-10-49-44.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00418/f00418_2013-05-15-10-52-28.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00419/f00419_2013-05-15-10-52-38.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00420/f00420_2013-05-15-10-52-49.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00421/f00421_2013-05-15-10-52-55.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00438/f00438_2013-05-16-14-44-45.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00439/f00439_2013-05-16-14-44-52.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00440/f00440_2013-05-16-14-45-06.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00441/f00441_2013-05-16-14-45-12.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00442/f00442_2013-05-16-14-47-01.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00444/f00444_2013-05-16-14-47-14.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00445/f00445_2013-05-16-14-47-19.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00446/f00446_2013-05-17-13-19-35.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00447/f00447_2013-05-17-13-19-41.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00448/f00448_2013-05-17-13-19-48.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00449/f00449_2013-05-17-13-19-56.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00450/f00450_2013-05-17-13-20-38.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00451/f00451_2013-05-17-13-20-42.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00452/f00452_2013-05-17-13-20-48.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00453/f00453_2013-05-17-13-21-04.json'),

]
e_shock = aba.loadMultipleDataFiles(e_shock)

e_sec = [
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
os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00414/f00414_2013-05-15-11-42-17.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00415/f00415_2013-05-15-11-42-23.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00416/f00416_2013-05-15-11-42-27.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00417/f00417_2013-05-15-11-42-33.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00418/f00418_2013-05-15-11-45-27.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00419/f00419_2013-05-15-11-45-32.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00420/f00420_2013-05-15-11-45-38.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-15/f00421/f00421_2013-05-15-11-45-44.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00438/f00438_2013-05-16-15-39-01.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00439/f00439_2013-05-16-15-39-10.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00440/f00440_2013-05-16-15-39-32.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00441/f00441_2013-05-16-15-39-28.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00442/f00442_2013-05-16-15-40-39.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00444/f00444_2013-05-16-15-40-51.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-16/f00445/f00445_2013-05-16-15-40-57.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00446/f00446_2013-05-17-14-12-34.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00447/f00447_2013-05-17-14-12-40.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00448/f00448_2013-05-17-14-12-45.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00449/f00449_2013-05-17-14-12-49.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00450/f00450_2013-05-17-14-13-30.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00451/f00451_2013-05-17-14-13-46.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00452/f00452_2013-05-17-14-13-49.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-17/f00453/f00453_2013-05-17-14-13-55.json'),
]
e_sec = aba.loadMultipleDataFiles(e_sec)

#fish kept in same tank after shocking
#12 has questionable tracking, but probably real
e_same_first = [
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
os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00390/f00390_2013-05-06-10-19-26.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00391/f00391_2013-05-06-10-19-33.json'), #current
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00392/f00392_2013-05-06-10-19-39.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00393/f00393_2013-05-06-10-19-47.json'), #red color
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00394/f00394_2013-05-06-10-21-26.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00395/f00395_2013-05-06-10-21-17.json'), #low velocity
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00396/f00396_2013-05-06-10-21-06.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00397/f00397_2013-05-06-10-21-03.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00406/f00406_2013-05-07-14-18-31.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00407/f00407_2013-05-07-14-18-22.json'), #current imbalance
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00408/f00408_2013-05-07-14-18-20.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00409/f00409_2013-05-07-14-18-18.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00410/f00410_2013-05-07-14-15-15.json'), #tracking
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00411/f00411_2013-05-07-14-15-17.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00412/f00412_2013-05-07-14-15-19.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00413/f00413_2013-05-07-14-15-21.json'),
os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00398/f00398_2013-05-06-14-53-59.json'),
#os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00399/f00399_2013-05-06-14-54-03.json'), #current imbalance 
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00400/f00400_2013-05-06-14-54-06.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00401/f00401_2013-05-06-14-54-09.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00402/f00402_2013-05-06-14-55-26.json'),
#os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00403/f00403_2013-05-06-14-56-20.json'), #tracking
#os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00404/f00404_2013-05-06-14-55-11.json'), #low velocity
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00405/f00405_2013-05-06-14-55-03.json'), #low velocity in second 15
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00462/f00462_2013-05-21-12-03-35.json'), #low velocity
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00463/f00463_2013-05-21-12-03-42.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00464/f00464_2013-05-21-12-03-49.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00465/f00465_2013-05-21-12-03-55.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00466/f00466_2013-05-21-12-05-29.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00467/f00467_2013-05-21-12-05-31.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00468/f00468_2013-05-21-12-05-33.json'),#low velocity
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00469/f00469_2013-05-21-12-05-35.json'),

]
e_same_first = aba.loadMultipleDataFiles(e_same_first)

e_same_shock = [
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
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00390/f00390_2013-05-06-10-55-27.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00391/f00391_2013-05-06-10-55-29.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00392/f00392_2013-05-06-10-55-31.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00393/f00393_2013-05-06-10-55-33.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00394/f00394_2013-05-06-10-56-35.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00395/f00395_2013-05-06-10-56-33.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00396/f00396_2013-05-06-10-56-31.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00397/f00397_2013-05-06-10-56-29.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00406/f00406_2013-05-07-14-49-23.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00407/f00407_2013-05-07-14-49-29.json'),
os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00408/f00408_2013-05-07-14-49-35.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00409/f00409_2013-05-07-14-49-43.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00410/f00410_2013-05-07-14-46-49.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00411/f00411_2013-05-07-14-46-43.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00412/f00412_2013-05-07-14-46-41.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00413/f00413_2013-05-07-14-46-38.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00398/f00398_2013-05-06-15-25-03.json'),
#os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00399/f00399_2013-05-06-15-25-06.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00400/f00400_2013-05-06-15-25-12.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00401/f00401_2013-05-06-15-25-19.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00402/f00402_2013-05-06-15-27-52.json'),
#os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00403/f00403_2013-05-06-15-28-02.json'),
#os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00404/f00404_2013-05-06-15-28-06.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00405/f00405_2013-05-06-15-28-10.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00462/f00462_2013-05-21-12-35-41.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00463/f00463_2013-05-21-12-35-35.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00464/f00464_2013-05-21-12-35-26.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00465/f00465_2013-05-21-12-35-21.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00466/f00466_2013-05-21-12-36-50.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00467/f00467_2013-05-21-12-36-57.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00468/f00468_2013-05-21-12-36-46.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00469/f00469_2013-05-21-12-36-40.json'),
]
e_same_shock = aba.loadMultipleDataFiles(e_same_shock)

e_same_sec = [
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
os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00390/f00390_2013-05-06-11-51-02.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00391/f00391_2013-05-06-11-51-19.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00392/f00392_2013-05-06-11-51-45.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00393/f00393_2013-05-06-11-51-39.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00394/f00394_2013-05-06-11-50-14.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00395/f00395_2013-05-06-11-50-08.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00396/f00396_2013-05-06-11-50-01.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00397/f00397_2013-05-06-11-49-53.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00406/f00406_2013-05-07-15-44-22.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00407/f00407_2013-05-07-15-44-15.json'),
os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00408/f00408_2013-05-07-15-44-02.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00409/f00409_2013-05-07-15-43-50.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00410/f00410_2013-05-07-15-40-09.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00411/f00411_2013-05-07-15-40-02.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00412/f00412_2013-05-07-15-39-55.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-07/f00413/f00413_2013-05-07-15-39-49.json'),
os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00398/f00398_2013-05-06-16-18-18.json'),
#os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00399/f00399_2013-05-06-16-18-11.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00400/f00400_2013-05-06-16-18-05.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00401/f00401_2013-05-06-16-17-59.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00402/f00402_2013-05-06-16-21-54.json'),
#os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00403/f00403_2013-05-06-16-21-48.json'),
#os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00404/f00404_2013-05-06-16-21-41.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-06/f00405/f00405_2013-05-06-16-21-33.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00462/f00462_2013-05-21-13-29-00.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00463/f00463_2013-05-21-13-29-08.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00464/f00464_2013-05-21-13-29-15.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00465/f00465_2013-05-21-13-29-25.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00466/f00466_2013-05-21-13-31-08.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00467/f00467_2013-05-21-13-31-17.json'),
# os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00468/f00468_2013-05-21-13-31-28.json'),
 os.path.expanduser('~/Dropbox/ConchisData/2013-05-21/f00469/f00469_2013-05-21-13-31-38.json'),
]
e_same_sec = aba.loadMultipleDataFiles(e_same_sec)

c_first = [
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
c_first = aba.loadMultipleDataFiles(c_first)

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
 
c_sec = [
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
c_sec = aba.loadMultipleDataFiles(c_sec)

print "Done loading fish."
