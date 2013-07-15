import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy


#safe tank, shocking protocol, shocking, safe
e_safe_first= [
'/home/vburns/Dropbox/ConchisData/2013-05-06/f00390/f00390_2013-05-06-10-19-26.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00391/f00391_2013-05-06-10-19-33.json', #current
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00392/f00392_2013-05-06-10-19-39.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00393/f00393_2013-05-06-10-19-47.json', #red color
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00394/f00394_2013-05-06-10-21-26.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00395/f00395_2013-05-06-10-21-17.json', #low velocity
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00396/f00396_2013-05-06-10-21-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00397/f00397_2013-05-06-10-21-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00406/f00406_2013-05-07-14-18-31.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-07/f00407/f00407_2013-05-07-14-18-22.json', #current imbalance
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00408/f00408_2013-05-07-14-18-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00409/f00409_2013-05-07-14-18-18.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-07/f00410/f00410_2013-05-07-14-15-15.json', #tracking
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00411/f00411_2013-05-07-14-15-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00412/f00412_2013-05-07-14-15-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00413/f00413_2013-05-07-14-15-21.json',
'/home/vburns/Dropbox/ConchisData/2013-05-06/f00398/f00398_2013-05-06-14-53-59.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00399/f00399_2013-05-06-14-54-03.json', #current imbalance 
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00400/f00400_2013-05-06-14-54-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00401/f00401_2013-05-06-14-54-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00402/f00402_2013-05-06-14-55-26.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00403/f00403_2013-05-06-14-56-20.json', #tracking
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00404/f00404_2013-05-06-14-55-11.json', #low velocity
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00405/f00405_2013-05-06-14-55-03.json', #low velocity in second 15
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00462/f00462_2013-05-21-12-03-35.json', #low velocity
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00463/f00463_2013-05-21-12-03-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00464/f00464_2013-05-21-12-03-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00465/f00465_2013-05-21-12-03-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00466/f00466_2013-05-21-12-05-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00467/f00467_2013-05-21-12-05-31.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00468/f00468_2013-05-21-12-05-33.json',#low velocity
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00469/f00469_2013-05-21-12-05-35.json',
]
e_safe_first = aba.loadMultipleDataFiles(e_safe_first)

e_safe_shock = [
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00390/f00390_2013-05-06-10-55-27.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00391/f00391_2013-05-06-10-55-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00392/f00392_2013-05-06-10-55-31.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00393/f00393_2013-05-06-10-55-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00394/f00394_2013-05-06-10-56-35.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00395/f00395_2013-05-06-10-56-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00396/f00396_2013-05-06-10-56-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00397/f00397_2013-05-06-10-56-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00406/f00406_2013-05-07-14-49-23.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-07/f00407/f00407_2013-05-07-14-49-29.json',
'/home/vburns/Dropbox/ConchisData/2013-05-07/f00408/f00408_2013-05-07-14-49-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00409/f00409_2013-05-07-14-49-43.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-07/f00410/f00410_2013-05-07-14-46-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00411/f00411_2013-05-07-14-46-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00412/f00412_2013-05-07-14-46-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00413/f00413_2013-05-07-14-46-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00398/f00398_2013-05-06-15-25-03.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00399/f00399_2013-05-06-15-25-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00400/f00400_2013-05-06-15-25-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00401/f00401_2013-05-06-15-25-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00402/f00402_2013-05-06-15-27-52.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00403/f00403_2013-05-06-15-28-02.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00404/f00404_2013-05-06-15-28-06.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00405/f00405_2013-05-06-15-28-10.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00462/f00462_2013-05-21-12-35-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00463/f00463_2013-05-21-12-35-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00464/f00464_2013-05-21-12-35-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00465/f00465_2013-05-21-12-35-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00466/f00466_2013-05-21-12-36-50.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00467/f00467_2013-05-21-12-36-57.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00468/f00468_2013-05-21-12-36-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00469/f00469_2013-05-21-12-36-40.json',
]
e_safe_shock = aba.loadMultipleDataFiles(e_safe_shock)

e_safe_sec = [
'/home/vburns/Dropbox/ConchisData/2013-05-06/f00390/f00390_2013-05-06-11-51-02.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00391/f00391_2013-05-06-11-51-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00392/f00392_2013-05-06-11-51-45.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00393/f00393_2013-05-06-11-51-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00394/f00394_2013-05-06-11-50-14.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00395/f00395_2013-05-06-11-50-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00396/f00396_2013-05-06-11-50-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00397/f00397_2013-05-06-11-49-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00406/f00406_2013-05-07-15-44-22.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-07/f00407/f00407_2013-05-07-15-44-15.json',
'/home/vburns/Dropbox/ConchisData/2013-05-07/f00408/f00408_2013-05-07-15-44-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00409/f00409_2013-05-07-15-43-50.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-07/f00410/f00410_2013-05-07-15-40-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00411/f00411_2013-05-07-15-40-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00412/f00412_2013-05-07-15-39-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00413/f00413_2013-05-07-15-39-49.json',
'/home/vburns/Dropbox/ConchisData/2013-05-06/f00398/f00398_2013-05-06-16-18-18.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00399/f00399_2013-05-06-16-18-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00400/f00400_2013-05-06-16-18-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00401/f00401_2013-05-06-16-17-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00402/f00402_2013-05-06-16-21-54.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00403/f00403_2013-05-06-16-21-48.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00404/f00404_2013-05-06-16-21-41.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00405/f00405_2013-05-06-16-21-33.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00462/f00462_2013-05-21-13-29-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00463/f00463_2013-05-21-13-29-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00464/f00464_2013-05-21-13-29-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00465/f00465_2013-05-21-13-29-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00466/f00466_2013-05-21-13-31-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00467/f00467_2013-05-21-13-31-17.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00468/f00468_2013-05-21-13-31-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00469/f00469_2013-05-21-13-31-38.json',
]
e_safe_sec = aba.loadMultipleDataFiles(e_safe_sec)

e_safe_third = [
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00390/f00390_2013-05-06-12-22-28.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00391/f00391_2013-05-06-12-22-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00392/f00392_2013-05-06-12-22-41.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00393/f00393_2013-05-06-12-22-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00394/f00394_2013-05-06-12-21-01.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00395/f00395_2013-05-06-12-21-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00396/f00396_2013-05-06-12-21-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00397/f00397_2013-05-06-12-21-26.json',
'/home/vburns/Dropbox/ConchisData/2013-05-07/f00406/f00406_2013-05-07-16-16-12.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-07/f00407/f00407_2013-05-07-16-16-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00408/f00408_2013-05-07-16-16-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00409/f00409_2013-05-07-16-15-54.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-07/f00410/f00410_2013-05-07-16-11-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00411/f00411_2013-05-07-16-11-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00412/f00412_2013-05-07-16-11-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-07/f00413/f00413_2013-05-07-16-10-55.json',
'/home/vburns/Dropbox/ConchisData/2013-05-06/f00398/f00398_2013-05-06-16-49-49.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00399/f00399_2013-05-06-16-49-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00400/f00400_2013-05-06-16-50-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00401/f00401_2013-05-06-16-50-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00402/f00402_2013-05-06-16-54-03.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00403/f00403_2013-05-06-16-54-05.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00404/f00404_2013-05-06-16-53-50.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00405/f00405_2013-05-06-16-53-38.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00462/f00462_2013-05-21-14-00-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00463/f00463_2013-05-21-14-00-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00464/f00464_2013-05-21-14-00-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00465/f00465_2013-05-21-14-00-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00466/f00466_2013-05-21-14-02-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00467/f00467_2013-05-21-14-02-24.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00468/f00468_2013-05-21-14-02-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00469/f00469_2013-05-21-14-02-13.json',
]
e_safe_third = aba.loadMultipleDataFiles(e_safe_third)

#safe, shocking protocol, shocking, shocking
e_same_first = [
'/home/vburns/Dropbox/ConchisData/2013-05-06/f00398/f00398_2013-05-06-14-53-59.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00399/f00399_2013-05-06-14-54-03.json', #current imbalance 
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00400/f00400_2013-05-06-14-54-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00401/f00401_2013-05-06-14-54-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00402/f00402_2013-05-06-14-55-26.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00403/f00403_2013-05-06-14-56-20.json', #tracking
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00404/f00404_2013-05-06-14-55-11.json', #low velocity
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00405/f00405_2013-05-06-14-55-03.json', #low velocity in second 15
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00462/f00462_2013-05-21-12-03-35.json', #low velocity
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00463/f00463_2013-05-21-12-03-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00464/f00464_2013-05-21-12-03-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00465/f00465_2013-05-21-12-03-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00466/f00466_2013-05-21-12-05-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00467/f00467_2013-05-21-12-05-31.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00468/f00468_2013-05-21-12-05-33.json',#low velocity
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00469/f00469_2013-05-21-12-05-35.json',
]
e_same_first = aba.loadMultipleDataFiles(e_same_first)

e_same_shock = [
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00398/f00398_2013-05-06-15-25-03.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00399/f00399_2013-05-06-15-25-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00400/f00400_2013-05-06-15-25-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00401/f00401_2013-05-06-15-25-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00402/f00402_2013-05-06-15-27-52.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00403/f00403_2013-05-06-15-28-02.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00404/f00404_2013-05-06-15-28-06.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00405/f00405_2013-05-06-15-28-10.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00462/f00462_2013-05-21-12-35-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00463/f00463_2013-05-21-12-35-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00464/f00464_2013-05-21-12-35-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00465/f00465_2013-05-21-12-35-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00466/f00466_2013-05-21-12-36-50.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00467/f00467_2013-05-21-12-36-57.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00468/f00468_2013-05-21-12-36-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00469/f00469_2013-05-21-12-36-40.json',
]
e_same_shock = aba.loadMultipleDataFiles(e_same_shock)

e_same_sec = [
'/home/vburns/Dropbox/ConchisData/2013-05-06/f00398/f00398_2013-05-06-16-18-18.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00399/f00399_2013-05-06-16-18-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00400/f00400_2013-05-06-16-18-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00401/f00401_2013-05-06-16-17-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00402/f00402_2013-05-06-16-21-54.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00403/f00403_2013-05-06-16-21-48.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00404/f00404_2013-05-06-16-21-41.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00405/f00405_2013-05-06-16-21-33.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00462/f00462_2013-05-21-13-29-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00463/f00463_2013-05-21-13-29-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00464/f00464_2013-05-21-13-29-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00465/f00465_2013-05-21-13-29-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00466/f00466_2013-05-21-13-31-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00467/f00467_2013-05-21-13-31-17.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00468/f00468_2013-05-21-13-31-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00469/f00469_2013-05-21-13-31-38.json',
]
e_same_sec = aba.loadMultipleDataFiles(e_same_sec)

e_same_third = [
'/home/vburns/Dropbox/ConchisData/2013-05-06/f00398/f00398_2013-05-06-16-49-49.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00399/f00399_2013-05-06-16-49-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00400/f00400_2013-05-06-16-50-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00401/f00401_2013-05-06-16-50-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-06/f00402/f00402_2013-05-06-16-54-03.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00403/f00403_2013-05-06-16-54-05.json',
#'/home/vburns/Dropbox/ConchisData/2013-05-06/f00404/f00404_2013-05-06-16-53-50.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-06/f00405/f00405_2013-05-06-16-53-38.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00462/f00462_2013-05-21-14-00-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00463/f00463_2013-05-21-14-00-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00464/f00464_2013-05-21-14-00-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00465/f00465_2013-05-21-14-00-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00466/f00466_2013-05-21-14-02-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00467/f00467_2013-05-21-14-02-24.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-21/f00468/f00468_2013-05-21-14-02-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-21/f00469/f00469_2013-05-21-14-02-13.json',
]
e_same_third = aba.loadMultipleDataFiles(e_same_third)

e_safeshock_first = [
'/home/vburns/Dropbox/ConchisData/2013-05-15/f00414/f00414_2013-05-15-10-17-16.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00415/f00415_2013-05-15-10-17-24.json', #low velocity in second base
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00416/f00416_2013-05-15-10-17-34.json', #tracking
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00417/f00417_2013-05-15-10-17-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00418/f00418_2013-05-15-10-20-55.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00419/f00419_2013-05-15-10-20-58.json', #low starting velocity
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00420/f00420_2013-05-15-10-21-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00421/f00421_2013-05-15-10-21-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00438/f00438_2013-05-16-14-13-03.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-16/f00439/f00439_2013-05-16-14-13-09.json', #low velocity in second base
# '/home/vburns/Dropbox/ConchisData/2013-05-16/f00440/f00440_2013-05-16-14-13-20.json', #tracking
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00441/f00441_2013-05-16-14-13-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00442/f00442_2013-05-16-14-16-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00444/f00444_2013-05-16-14-16-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00445/f00445_2013-05-16-14-15-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00446/f00446_2013-05-17-12-47-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00447/f00447_2013-05-17-12-47-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00448/f00448_2013-05-17-12-47-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00449/f00449_2013-05-17-12-47-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00450/f00450_2013-05-17-12-49-05.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-17/f00451/f00451_2013-05-17-12-49-07.json', #current imbalance and tracking
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00452/f00452_2013-05-17-12-49-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00453/f00453_2013-05-17-12-49-10.json',
]
e_safeshock_first = aba.loadMultipleDataFiles(e_safeshock_first)

e_safeshock_shock = [
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00414/f00414_2013-05-15-10-49-21.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00415/f00415_2013-05-15-10-49-28.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00416/f00416_2013-05-15-10-49-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00417/f00417_2013-05-15-10-49-44.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00418/f00418_2013-05-15-10-52-28.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00419/f00419_2013-05-15-10-52-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00420/f00420_2013-05-15-10-52-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00421/f00421_2013-05-15-10-52-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00438/f00438_2013-05-16-14-44-45.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-16/f00439/f00439_2013-05-16-14-44-52.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-16/f00440/f00440_2013-05-16-14-45-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00441/f00441_2013-05-16-14-45-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00442/f00442_2013-05-16-14-47-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00444/f00444_2013-05-16-14-47-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00445/f00445_2013-05-16-14-47-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00446/f00446_2013-05-17-13-19-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00447/f00447_2013-05-17-13-19-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00448/f00448_2013-05-17-13-19-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00449/f00449_2013-05-17-13-19-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00450/f00450_2013-05-17-13-20-38.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-17/f00451/f00451_2013-05-17-13-20-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00452/f00452_2013-05-17-13-20-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00453/f00453_2013-05-17-13-21-04.json',
]
e_safeshock_shock = aba.loadMultipleDataFiles(e_safeshock_shock)

e_safeshock_sec = [
'/home/vburns/Dropbox/ConchisData/2013-05-15/f00414/f00414_2013-05-15-11-42-17.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00415/f00415_2013-05-15-11-42-23.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00416/f00416_2013-05-15-11-42-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00417/f00417_2013-05-15-11-42-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00418/f00418_2013-05-15-11-45-27.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00419/f00419_2013-05-15-11-45-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00420/f00420_2013-05-15-11-45-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00421/f00421_2013-05-15-11-45-44.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00438/f00438_2013-05-16-15-39-01.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-16/f00439/f00439_2013-05-16-15-39-10.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-16/f00440/f00440_2013-05-16-15-39-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00441/f00441_2013-05-16-15-39-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00442/f00442_2013-05-16-15-40-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00444/f00444_2013-05-16-15-40-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00445/f00445_2013-05-16-15-40-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00446/f00446_2013-05-17-14-12-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00447/f00447_2013-05-17-14-12-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00448/f00448_2013-05-17-14-12-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00449/f00449_2013-05-17-14-12-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00450/f00450_2013-05-17-14-13-30.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-17/f00451/f00451_2013-05-17-14-13-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00452/f00452_2013-05-17-14-13-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00453/f00453_2013-05-17-14-13-55.json',
]
e_safeshock_sec = aba.loadMultipleDataFiles(e_safeshock_sec)

e_safeshock_third = [
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00414/f00414_2013-05-15-12-14-44.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00415/f00415_2013-05-15-12-14-33.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00416/f00416_2013-05-15-12-14-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00417/f00417_2013-05-15-12-14-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00418/f00418_2013-05-15-12-18-10.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-15/f00419/f00419_2013-05-15-12-17-58.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00420/f00420_2013-05-15-12-17-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-15/f00421/f00421_2013-05-15-12-17-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00438/f00438_2013-05-16-16-11-08.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-16/f00439/f00439_2013-05-16-16-11-18.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-16/f00440/f00440_2013-05-16-16-11-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00441/f00441_2013-05-16-16-11-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00442/f00442_2013-05-16-16-13-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00444/f00444_2013-05-16-16-13-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-16/f00445/f00445_2013-05-16-16-13-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00446/f00446_2013-05-17-14-44-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00447/f00447_2013-05-17-14-44-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00448/f00448_2013-05-17-14-44-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00449/f00449_2013-05-17-14-44-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00450/f00450_2013-05-17-14-45-26.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-17/f00451/f00451_2013-05-17-14-45-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00452/f00452_2013-05-17-14-45-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00453/f00453_2013-05-17-14-45-41.json',
]
e_safeshock_third = aba.loadMultipleDataFiles(e_safeshock_third)

e_safesafe_first = [
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00446/f00446_2013-05-17-12-47-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00447/f00447_2013-05-17-12-47-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00448/f00448_2013-05-17-12-47-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00449/f00449_2013-05-17-12-47-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00450/f00450_2013-05-17-12-49-05.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-17/f00451/f00451_2013-05-17-12-49-07.json', #current imbalance and tracking
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00452/f00452_2013-05-17-12-49-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00453/f00453_2013-05-17-12-49-10.json',
]
e_safesafe_first = aba.loadMultipleDataFiles(e_safesafe_first)

e_safesafe_shock = [
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00446/f00446_2013-05-17-13-19-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00447/f00447_2013-05-17-13-19-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00448/f00448_2013-05-17-13-19-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00449/f00449_2013-05-17-13-19-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00450/f00450_2013-05-17-13-20-38.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-17/f00451/f00451_2013-05-17-13-20-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00452/f00452_2013-05-17-13-20-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00453/f00453_2013-05-17-13-21-04.json',
]
e_safesafe_shock = aba.loadMultipleDataFiles(e_safesafe_shock)

e_safesafe_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00446/f00446_2013-05-17-14-12-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00447/f00447_2013-05-17-14-12-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00448/f00448_2013-05-17-14-12-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00449/f00449_2013-05-17-14-12-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00450/f00450_2013-05-17-14-13-30.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-17/f00451/f00451_2013-05-17-14-13-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00452/f00452_2013-05-17-14-13-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00453/f00453_2013-05-17-14-13-55.json',
]
e_safesafe_sec = aba.loadMultipleDataFiles(e_safesafe_sec)

e_safesafe_third = [
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00446/f00446_2013-05-17-14-44-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00447/f00447_2013-05-17-14-44-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00448/f00448_2013-05-17-14-44-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00449/f00449_2013-05-17-14-44-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00450/f00450_2013-05-17-14-45-26.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-17/f00451/f00451_2013-05-17-14-45-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00452/f00452_2013-05-17-14-45-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00453/f00453_2013-05-17-14-45-41.json',
]
e_safesafe_third = aba.loadMultipleDataFiles(e_safesafe_third)

#velocity analysis 
sm = 15; #smooth over 15 frames.
endWinLen = 5 * 60; #seconds

eBaseVelSafe_1a = aba.getMedianVelMulti(e_safe_first, (0,900), smoothWinLen = sm)
eBaseVelSafe_1b = aba.getMedianVelMulti(e_safe_first, (900,1800), smoothWinLen = sm)
eBaseVelSafe_2a = aba.getMedianVelMulti(e_safe_sec, (0,900), smoothWinLen = sm)
eBaseVelSafe_2b = aba.getMedianVelMulti(e_safe_sec, (900,1800), smoothWinLen = sm)
eBaseVelSafe_3a = aba.getMedianVelMulti(e_safe_third, (0,900), smoothWinLen = sm)
eBaseVelSafe_3b = aba.getMedianVelMulti(e_safe_third, (900,1800), smoothWinLen = sm)
eBaseSafe = aba.getMedianVelMulti(e_safe_shock, (0, 900), smoothWinLen = sm)
eEndVelSafe = aba.getMedianVelMulti(e_safe_shock, tRange=[-endWinLen,-0], smoothWinLen=sm)

eBaseVelSafeShock_1a = aba.getMedianVelMulti(e_safeshock_first, (0,900), smoothWinLen = sm)
eBaseVelSafeShock_1b = aba.getMedianVelMulti(e_safeshock_first, (900,1800), smoothWinLen = sm)
eBaseVelSafeShock_2a = aba.getMedianVelMulti(e_safeshock_sec, (0,900), smoothWinLen = sm)
eBaseVelSafeShock_2b = aba.getMedianVelMulti(e_safeshock_sec, (900,1800), smoothWinLen = sm)
eBaseVelSafeShock_3a = aba.getMedianVelMulti(e_safeshock_third, (0,900), smoothWinLen = sm)
eBaseVelSafeShock_3b = aba.getMedianVelMulti(e_safeshock_third, (900,1800), smoothWinLen = sm)
eBaseSafeShock = aba.getMedianVelMulti(e_safeshock_shock, (0, 900), smoothWinLen = sm)
eEndVelSafeShock = aba.getMedianVelMulti(e_safeshock_shock, tRange=[-endWinLen,-0], smoothWinLen=sm)

eBaseVelSafeSafe_1a = aba.getMedianVelMulti(e_safesafe_first, (0,900), smoothWinLen = sm)
eBaseVelSafeSafe_1b = aba.getMedianVelMulti(e_safesafe_first, (900,1800), smoothWinLen = sm)
eBaseVelSafeSafe_2a = aba.getMedianVelMulti(e_safesafe_sec, (0,900), smoothWinLen = sm)
eBaseVelSafeSafe_2b = aba.getMedianVelMulti(e_safesafe_sec, (900,1800), smoothWinLen = sm)
eBaseVelSafeSafe_3a = aba.getMedianVelMulti(e_safesafe_third, (0,900), smoothWinLen = sm)
eBaseVelSafeSafe_3b = aba.getMedianVelMulti(e_safesafe_third, (900,1800), smoothWinLen = sm)
eBaseSafeSafe = aba.getMedianVelMulti(e_safesafe_shock, (0, 900), smoothWinLen = sm)
eEndVelSafeSafe = aba.getMedianVelMulti(e_safesafe_shock, tRange=[-endWinLen,-0], smoothWinLen=sm)

eBaseVelSame_1a = aba.getMedianVelMulti(e_same_first, (0,900), smoothWinLen = sm)
eBaseVelSame_1b = aba.getMedianVelMulti(e_same_first, (900,1800), smoothWinLen = sm)
eBaseVelSame_2a = aba.getMedianVelMulti(e_same_sec, (0,900), smoothWinLen = sm)
eBaseVelSame_2b = aba.getMedianVelMulti(e_same_sec, (900,1800), smoothWinLen = sm)
eBaseVelSame_3a = aba.getMedianVelMulti(e_same_third, (0,900), smoothWinLen = sm)
eBaseVelSame_3b = aba.getMedianVelMulti(e_same_third, (900,1800), smoothWinLen = sm)
eBaseSame = aba.getMedianVelMulti(e_same_shock, (0, 900), smoothWinLen = sm)
eEndVelSame = aba.getMedianVelMulti(e_same_shock, tRange=[-endWinLen,-0], smoothWinLen=sm)

#comparisons 
[tv, safe_shock_end] = scipy.stats.ttest_ind(eBaseVelSafe_2b, eEndVelSafe)
[tv, same_shock_end] = scipy.stats.ttest_ind(eBaseVelSame_3b, eEndVelSame)
[tv, shock_safe_end] = scipy.stats.ttest_ind(eBaseVelSafeShock_3b, eEndVelSafeShock)

[tv, safe_same] = scipy.stats.ttest_ind(eBaseVelSafe_3b, eBaseVelSame_3b)
[tv, safe_shocksafe] =scipy.stats.ttest_ind(eBaseVelSafe_2b, eBaseVelSafeShock_2b)
[tv, same_shocksafe] = scipy.stats.ttest_ind(eBaseVelSame_3b, eBaseVelSafeShock_3b)

[tv, safe_safeshock] = scipy.stats.ttest_ind(eBaseVelSafeSafe_3b, eBaseVelSafeShock_3b)

print 'Statistics comparing end velocity:', safe_shocksafe


#fix
#eEndVel25[2]= np.nan

#convert to array
eSafe_1a = np.array([np.array([eBaseVelSafe_1a[n]]) for n in range(len(eBaseVelSafe_1a))])
eSafe_1b = np.array([np.array([eBaseVelSafe_1b[n]]) for n in range(len(eBaseVelSafe_1b))])
eSafe_2a = np.array([np.array([eBaseVelSafe_2a[n]]) for n in range(len(eBaseVelSafe_2a))])
eSafe_2b = np.array([np.array([eBaseVelSafe_2b[n]]) for n in range(len(eBaseVelSafe_2b))])
eSafe_3a = np.array([np.array([eBaseVelSafe_3a[n]]) for n in range(len(eBaseVelSafe_3a))])
eSafe_3b = np.array([np.array([eBaseVelSafe_3b[n]]) for n in range(len(eBaseVelSafe_3b))])
eSafeBase = np.array([np.array([eBaseSafe[n]]) for n in range(len(eBaseSafe))])
eSafeEnd = np.array([np.array([eEndVelSafe[n]]) for n in range(len(eEndVelSafe))])\

eSafeShock_1a = np.array([np.array([eBaseVelSafeShock_1a[n]]) for n in range(len(eBaseVelSafeShock_1a))])
eSafeShock_1b = np.array([np.array([eBaseVelSafeShock_1b[n]]) for n in range(len(eBaseVelSafeShock_1b))])
eSafeShock_2a = np.array([np.array([eBaseVelSafeShock_2a[n]]) for n in range(len(eBaseVelSafeShock_2a))])
eSafeShock_2b = np.array([np.array([eBaseVelSafeShock_2b[n]]) for n in range(len(eBaseVelSafeShock_2b))])
eSafeShock_3a = np.array([np.array([eBaseVelSafeShock_3a[n]]) for n in range(len(eBaseVelSafeShock_3a))])
eSafeShock_3b = np.array([np.array([eBaseVelSafeShock_3b[n]]) for n in range(len(eBaseVelSafeShock_3b))])
eSafeShockBase = np.array([np.array([eBaseSafeShock[n]]) for n in range(len(eBaseSafeShock))])
eSafeShockEnd = np.array([np.array([eEndVelSafeShock[n]]) for n in range(len(eEndVelSafeShock))])

eSafeSafe_1a = np.array([np.array([eBaseVelSafeSafe_1a[n]]) for n in range(len(eBaseVelSafeSafe_1a))])
eSafeSafe_1b = np.array([np.array([eBaseVelSafeSafe_1b[n]]) for n in range(len(eBaseVelSafeSafe_1b))])
eSafeSafe_2a = np.array([np.array([eBaseVelSafeSafe_2a[n]]) for n in range(len(eBaseVelSafeSafe_2a))])
eSafeSafe_2b = np.array([np.array([eBaseVelSafeSafe_2b[n]]) for n in range(len(eBaseVelSafeSafe_2b))])
eSafeSafe_3a = np.array([np.array([eBaseVelSafeSafe_3a[n]]) for n in range(len(eBaseVelSafeSafe_3a))])
eSafeSafe_3b = np.array([np.array([eBaseVelSafeSafe_3b[n]]) for n in range(len(eBaseVelSafeSafe_3b))])
eSafeSafeBase = np.array([np.array([eBaseSafeSafe[n]]) for n in range(len(eBaseSafeSafe))])
eSafeSafeEnd = np.array([np.array([eEndVelSafeSafe[n]]) for n in range(len(eEndVelSafeSafe))])

eSame_1a = np.array([np.array([eBaseVelSame_1a[n]]) for n in range(len(eBaseVelSame_1a))])
eSame_1b = np.array([np.array([eBaseVelSame_1b[n]]) for n in range(len(eBaseVelSame_1b))])
eSame_2a = np.array([np.array([eBaseVelSame_2a[n]]) for n in range(len(eBaseVelSame_2a))])
eSame_2b = np.array([np.array([eBaseVelSame_2b[n]]) for n in range(len(eBaseVelSame_2b))])
eSame_3a = np.array([np.array([eBaseVelSame_3a[n]]) for n in range(len(eBaseVelSame_3a))])
eSame_3b = np.array([np.array([eBaseVelSame_3b[n]]) for n in range(len(eBaseVelSame_3b))])
eSameBase = np.array([np.array([eBaseSame[n]]) for n in range(len(eBaseSame))])
eSameEnd = np.array([np.array([eEndVelSame[n]]) for n in range(len(eEndVelSame))])

eSafe = np.transpose(np.hstack((eSafe_1a, eSafe_1b, eSafeBase, eSafeEnd, eSafe_2a, eSafe_2b, eSafe_3a, eSafe_3b)))
eSafeShock = np.transpose(np.hstack((eSafeShock_1a, eSafeShock_1b, eSafeShockBase, eSafeShockEnd, eSafeShock_2a, eSafeShock_2b, eSafeShock_3a, eSafeShock_3b)))
eSafeSafe = np.transpose(np.hstack((eSafeSafe_1a, eSafeSafe_1b, eSafeSafeBase, eSafeSafeEnd, eSafeSafe_2a, eSafeSafe_2b, eSafeSafe_3a, eSafeSafe_3b)))
eSame = np.transpose(np.hstack((eSame_1a, eSame_1b, eSameBase, eSameEnd, eSame_2a, eSame_2b, eSame_3a, eSame_3b)))

n=4
pylab.figure(110)
pylab.suptitle('Learned Helplessness Assay at 5V - Safe, Shocking, Safe')
ax = pylab.subplot(1,n,1)
pylab.plot(eSame)
pylab.plot(0, [eBaseVelSame_1a], 'r.')
pylab.plot(1, [eBaseVelSame_1b], 'r.')
pylab.plot(2,[eBaseSame],'r.')
pylab.plot(3, [eEndVelSame], 'r.')
pylab.plot(4, [eBaseVelSame_2a], 'r.')
pylab.plot(5, [eBaseVelSame_2b], 'r.')
#pylab.plot(6, [eBaseVelSame_3a], 'r.')
#pylab.plot(7, [eBaseVelSame_3b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseVelSame_1a), np.mean(eBaseVelSame_1b), np.mean(eBaseSame), np.mean(eEndVelSame), np.mean(eBaseVelSame_2a), np.mean(eBaseVelSame_2b)],'o-k',lw=3)
yerrSame = (2*scipy.stats.sem(eBaseVelSame_1a), 2*scipy.stats.sem(eBaseVelSame_1b), 2*scipy.stats.sem(eBaseSame), 2*scipy.stats.sem(eEndVelSame), 2*scipy.stats.sem(eBaseVelSame_2a), 2*scipy.stats.sem(eBaseVelSame_2b))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelSame_1a), np.mean(eBaseVelSame_1b), np.mean(eBaseSame), np.mean(eEndVelSame), np.mean(eBaseVelSame_2a), np.mean(eBaseVelSame_2b)],fmt='ok',yerr=yerrSame, lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Fish kept in shocking tanks')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,n,2)
pylab.plot(eSafe)
pylab.plot(0, [eBaseVelSafe_1a], 'r.')
pylab.plot(1, [eBaseVelSafe_1b], 'r.')
pylab.plot(2,[eBaseSafe],'r.')
pylab.plot(3, [eEndVelSafe], 'r.')
pylab.plot(4, [eBaseVelSafe_2a], 'r.')
pylab.plot(5, [eBaseVelSafe_2b], 'r.')
#pylab.plot(6, [eBaseVelSafe_3a], 'r.')
#pylab.plot(7, [eBaseVelSafe_3b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseVelSafe_1a), np.mean(eBaseVelSafe_1b), np.mean(eBaseSafe), np.mean(eEndVelSafe), np.mean(eBaseVelSafe_2a), np.mean(eBaseVelSafe_2b)],'o-k',lw=3)
yerrSafe = (2*scipy.stats.sem(eBaseVelSafe_1a), 2*scipy.stats.sem(eBaseVelSafe_1b), 2*scipy.stats.sem(eBaseSafe), 2*scipy.stats.sem(eEndVelSafe), 2*scipy.stats.sem(eBaseVelSafe_2a), 2*scipy.stats.sem(eBaseVelSafe_2b))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelSafe_1a), np.mean(eBaseVelSafe_1b), np.mean(eBaseSafe), np.mean(eEndVelSafe), np.mean(eBaseVelSafe_2a), np.mean(eBaseVelSafe_2b)],fmt='ok',yerr=yerrSafe, lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Fish kept in shocking tanks for 30 min \n and then moved to safe')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,n,3)
pylab.plot(eSafeShock)
pylab.plot(0, [eBaseVelSafeShock_1a], 'r.')
pylab.plot(1, [eBaseVelSafeShock_1b], 'r.')
pylab.plot(2,[eBaseSafeShock],'r.')
pylab.plot(3, [eEndVelSafeShock], 'r.')
pylab.plot(4, [eBaseVelSafeShock_2a], 'r.')
pylab.plot(5, [eBaseVelSafeShock_2b], 'r.')
#pylab.plot(6, [eBaseVelSafeShock_3a], 'r.')
#pylab.plot(7, [eBaseVelSafeShock_3b], 'r.')
#pylab.plot([0,1,2,3,4,5,6,7],[np.mean(eBaseVelSafeShock_1a), np.mean(eBaseVelSafeShock_1b), np.mean(eBaseSafeShock), np.mean(eEndVelSafeShock), np.mean(eBaseVelSafeShock_2a), np.mean(eBaseVelSafeShock_2b), np.mean(eBaseVelSafeShock_3a), np.mean(eBaseVelSafeShock_3b)],'o-k',lw=3)
yerrSafeShock = (2*scipy.stats.sem(eBaseVelSafeShock_1a), 2*scipy.stats.sem(eBaseVelSafeShock_1b), 2*scipy.stats.sem(eBaseSafeShock), 2*scipy.stats.sem(eEndVelSafeShock), 2*scipy.stats.sem(eBaseVelSafeShock_2a), 2*scipy.stats.sem(eBaseVelSafeShock_2b))
#pyplot.errorbar([0,1,2,3,4,5,6,7],[np.mean(eBaseVelSafeShock_1a), np.mean(eBaseVelSafeShock_1b), np.mean(eBaseSafeShock), np.mean(eEndVelSafeShock), np.mean(eBaseVelSafeShock_2a), np.mean(eBaseVelSafeShock_2b), np.mean(eBaseVelSafeShock_3a), np.mean(eBaseVelSafeShock_3b)],fmt='ok',yerr=yerrSafeShock, lw=3)
ax.set_xticks((0,1,2,3,4,5,6,7))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,7.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Fish moved to safe tanks for 30 min \n and then moved back to shocking')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,n,4)
pylab.plot(eSafeSafe)
pylab.plot(0, [eBaseVelSafeSafe_1a], 'r.')
pylab.plot(1, [eBaseVelSafeSafe_1b], 'r.')
pylab.plot(2,[eBaseSafeSafe],'r.')
pylab.plot(3, [eEndVelSafeSafe], 'r.')
pylab.plot(4, [eBaseVelSafeSafe_2a], 'r.')
pylab.plot(5, [eBaseVelSafeSafe_2b], 'r.')
#pylab.plot(6, [eBaseVelSafeSafe_3a], 'r.')
#pylab.plot(7, [eBaseVelSafeSafe_3b], 'r.')
#pylab.plot([0,1,2,3,4,5,6,7],[np.mean(eBaseVelSafeSafe_1a), np.mean(eBaseVelSafeSafe_1b), np.mean(eBaseSafeSafe), np.mean(eEndVelSafeSafe), np.mean(eBaseVelSafeSafe_2a), np.mean(eBaseVelSafeSafe_2b), np.mean(eBaseVelSafeSafe_3a), np.mean(eBaseVelSafeSafe_3b)],'o-k',lw=3)
yerrSafeSafe = (2*scipy.stats.sem(eBaseVelSafeSafe_1a), 2*scipy.stats.sem(eBaseVelSafeSafe_1b), 2*scipy.stats.sem(eBaseSafeSafe), 2*scipy.stats.sem(eEndVelSafeSafe), 2*scipy.stats.sem(eBaseVelSafeSafe_2a), 2*scipy.stats.sem(eBaseVelSafeSafe_2b))
#pyplot.errorbar([0,1,2,3,4,5,6,7],[np.mean(eBaseVelSafeSafe_1a), np.mean(eBaseVelSafeSafe_1b), np.mean(eBaseSafeSafe), np.mean(eEndVelSafeSafe), np.mean(eBaseVelSafeSafe_2a), np.mean(eBaseVelSafeSafe_2b), np.mean(eBaseVelSafeSafe_3a), np.mean(eBaseVelSafeSafe_3b)],fmt='ok',yerr=yerrSafeSafe, lw=3)
ax.set_xticks((0,1,2,3,4,5,6,7))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,7.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Fish moved to safe tanks for 30 min \n and then moved back to shocking')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
"""
ax = pylab.subplot(1,n,4)
pylab.plot(eSafeSafe)
pylab.plot(0, [eBaseVelSafeSafe_1a], 'r.')
pylab.plot(1, [eBaseVelSafeSafe_1b], 'r.')
pylab.plot(2,[eBaseSafeSafe],'r.')
pylab.plot(3, [eEndVelSafeSafe], 'r.')
pylab.plot(4, [eBaseVelSafeSafe_2a], 'r.')
pylab.plot(5, [eBaseVelSafeSafe_2b], 'r.')
pylab.plot(6, [eBaseVelSafeSafe_3a], 'r.')
pylab.plot(7, [eBaseVelSafeSafe_3b], 'r.')
pylab.plot([0,1,2,3,4,5,6,7],[np.mean(eBaseVelSafeSafe_1a), np.mean(eBaseVelSafeSafe_1b), np.mean(eBaseSafeSafe), np.mean(eEndVelSafeSafe), np.mean(eBaseVelSafeSafe_2a), np.mean(eBaseVelSafeSafe_2b), np.mean(eBaseVelSafeSafe_3a), np.mean(eBaseVelSafeSafe_3b)],'o-k',lw=3)
yerrSafeSafe = (2*scipy.stats.sem(eBaseVelSafeSafe_1a), 2*scipy.stats.sem(eBaseVelSafeSafe_1b), 2*scipy.stats.sem(eBaseSafeSafe), 2*scipy.stats.sem(eEndVelSafeSafe), 2*scipy.stats.sem(eBaseVelSafeSafe_2a), 2*scipy.stats.sem(eBaseVelSafeSafe_2b), 2*scipy.stats.sem(eBaseVelSafeSafe_3a), 2*scipy.stats.sem(eBaseVelSafeSafe_3b))
pyplot.errorbar([0,1,2,3,4,5,6,7],[np.mean(eBaseVelSafeSafe_1a), np.mean(eBaseVelSafeSafe_1b), np.mean(eBaseSafeSafe), np.mean(eEndVelSafeSafe), np.mean(eBaseVelSafeSafe_2a), np.mean(eBaseVelSafeSafe_2b), np.mean(eBaseVelSafeSafe_3a), np.mean(eBaseVelSafeSafe_3b)],fmt='ok',yerr=yerrSafeSafe, lw=3)
ax.set_xticks((0,1,2,3,4,5,6,7))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,7.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Fish kept in safe tanks for 30 min and then pipetted back into safe')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
"""

pylab.figure(210)
pylab.suptitle('Summary of Median Velocities (mm/s)')
ax = pylab.subplot(1,1,1)
ESafe = ax.plot([0,1,2,3,4,5],[np.mean(eBaseVelSafe_1a), np.mean(eBaseVelSafe_1b), np.mean(eBaseSafe), np.mean(eEndVelSafe), np.mean(eBaseVelSafe_2a), np.mean(eBaseVelSafe_2b)],'o-b', lw=3, label='Experimental Fish (5V): Safe-Shocking-Shocking-Safe')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelSafe_1a), np.mean(eBaseVelSafe_1b), np.mean(eBaseSafe), np.mean(eEndVelSafe), np.mean(eBaseVelSafe_2a), np.mean(eBaseVelSafe_2b)],fmt='ob',yerr=yerrSafe, lw=3)
#ESame = ax.plot([0,1,2,3,4,5,6,7],[np.mean(eBaseVelSame_1a), np.mean(eBaseVelSame_1b), np.mean(eBaseSame), np.mean(eEndVelSame), np.mean(eBaseVelSame_2a), np.mean(eBaseVelSame_2b), np.mean(eBaseVelSame_3a), np.mean(eBaseVelSame_3b)],'o-r', lw=3, label='Experimental Fish (5V): Safe-Shocking-Shocking-Shocking')
#pyplot.errorbar([0,1,2,3,4,5,6,7],[np.mean(eBaseVelSame_1a), np.mean(eBaseVelSame_1b), np.mean(eBaseSame), np.mean(eEndVelSame), np.mean(eBaseVelSame_2a), np.mean(eBaseVelSame_2b), np.mean(eBaseVelSame_3a), np.mean(eBaseVelSame_3b)],fmt='or',yerr=yerrSame, lw=3)
ESafeShock = ax.plot([0,1,2,3,4,5],[np.mean(eBaseVelSafeShock_1a), np.mean(eBaseVelSafeShock_1b), np.mean(eBaseSafeShock), np.mean(eEndVelSafeShock), np.mean(eBaseVelSafeShock_2a), np.mean(eBaseVelSafeShock_2b)],'o-c',lw=3, label='Experimental Fish (5V): Safe-Shocking-Safe-Shocking')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelSafeShock_1a), np.mean(eBaseVelSafeShock_1b), np.mean(eBaseSafeShock), np.mean(eEndVelSafeShock), np.mean(eBaseVelSafeShock_2a), np.mean(eBaseVelSafeShock_2b)],fmt='oc',yerr=yerrSafeShock, lw=3)
#ESafeSafe = ax.plot([0,1,2,3,4,5,6,7],[np.mean(eBaseVelSafeSafe_1a), np.mean(eBaseVelSafeSafe_1b), np.mean(eBaseSafeSafe), np.mean(eEndVelSafeSafe), np.mean(eBaseVelSafeSafe_2a), np.mean(eBaseVelSafeSafe_2b), np.mean(eBaseVelSafeSafe_3a), np.mean(eBaseVelSafeSafe_3b)],'o-k',lw=3, label='Experimental Fish (5V): Safe-Shocking-Safe-Safe')
#pyplot.errorbar([0,1,2,3,4,5,6,7],[np.mean(eBaseVelSafeSafe_1a), np.mean(eBaseVelSafeSafe_1b), np.mean(eBaseSafeSafe), np.mean(eEndVelSafeSafe), np.mean(eBaseVelSafeSafe_2a), np.mean(eBaseVelSafeSafe_2b), np.mean(eBaseVelSafeSafe_3a), np.mean(eBaseVelSafeSafe_3b)],fmt='ok',yerr=yerrSafeSafe, lw=3)
handles, labels = ax.get_legend_handles_labels()
#ESafeSafe = ax.plot([0,1,2,3,4,5,6,7],[np.mean(eBaseVelSafeSafe_1a), np.mean(eBaseVelSafeSafe_1b), np.mean(eBaseSafeSafe), np.mean(eEndVelSafeSafe), np.mean(eBaseVelSafeSafe_2a), np.mean(eBaseVelSafeSafe_2b), np.mean(eBaseVelSafeSafe_3a), np.mean(eBaseVelSafeSafe_3b)],'o-c',lw=3, label='Experimental Fish (5V): Safe-Shocking-Safe-Safe')
#pyplot.errorbar([0,1,2,3,4,5,6,7],[np.mean(eBaseVelSafeSafe_1a), np.mean(eBaseVelSafeSafe_1b), np.mean(eBaseSafeSafe), np.mean(eEndVelSafeSafe), np.mean(eBaseVelSafeSafe_2a), np.mean(eBaseVelSafeSafe_2b), np.mean(eBaseVelSafeSafe_3a), np.mean(eBaseVelSafeSafe_3b)],fmt='oc',yerr=yerrSafeSafe, lw=3)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline\n shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
patch2 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch2)

pylab.show()

