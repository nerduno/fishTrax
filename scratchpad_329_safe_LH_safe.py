import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy


#first is 30 min in safe tank, then standard shocking, then 30 min in safe tank
e_shock5 = [
'/home/vburns/Dropbox/ConchisData/2013-03-29/f00239/f00239_2013-03-29-17-46-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00240/f00240_2013-03-29-17-46-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00241/f00241_2013-03-29-17-46-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00242/f00242_2013-03-29-17-46-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00243/f00243_2013-03-29-17-51-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00244/f00244_2013-03-29-17-51-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00245/f00245_2013-03-29-17-51-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00246/f00246_2013-03-29-17-51-35.json',
]
e_shock5 = aba.loadMultipleDataFiles(e_shock5)

e_shock8 = [
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00247/f00247_2013-03-29-19-52-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00248/f00248_2013-03-29-19-52-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00249/f00249_2013-03-29-19-52-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00250/f00250_2013-03-29-19-52-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00251/f00251_2013-03-29-19-53-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00252/f00252_2013-03-29-19-53-37.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00253/f00253_2013-03-29-19-53-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00254/f00254_2013-03-29-19-53-32.json',
]
e_shock8= aba.loadMultipleDataFiles(e_shock8)

e_safe5_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00239/f00239_2013-03-29-18-40-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00240/f00240_2013-03-29-18-40-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00241/f00241_2013-03-29-18-40-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00242/f00242_2013-03-29-18-40-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00243/f00243_2013-03-29-18-44-44.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00244/f00244_2013-03-29-18-44-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00245/f00245_2013-03-29-18-44-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00246/f00246_2013-03-29-18-44-35.json'
]
e_safe5_sec = aba.loadMultipleDataFiles(e_safe5_sec)

e_safe5_first= [
'/home/vburns/Dropbox/ConchisData/2013-03-29/f00239/f00239_2013-03-29-17-14-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00240/f00240_2013-03-29-17-14-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00241/f00241_2013-03-29-17-14-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00242/f00242_2013-03-29-17-14-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00243/f00243_2013-03-29-17-15-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00244/f00244_2013-03-29-17-15-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00245/f00245_2013-03-29-17-15-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00246/f00246_2013-03-29-17-15-47.json',
]
e_safe5_first = aba.loadMultipleDataFiles(e_safe5_first)

e_safe8_first = [
'/home/vburns/Dropbox/ConchisData/2013-03-29/f00247/f00247_2013-03-29-19-18-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00248/f00248_2013-03-29-19-18-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00249/f00249_2013-03-29-19-18-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00250/f00250_2013-03-29-19-18-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00251/f00251_2013-03-29-19-20-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00252/f00252_2013-03-29-19-20-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00253/f00253_2013-03-29-19-20-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00254/f00254_2013-03-29-19-20-06.json'
]
e_safe8_first = aba.loadMultipleDataFiles(e_safe8_first)

e_safe8_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00247/f00247_2013-03-29-20-46-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00248/f00248_2013-03-29-20-46-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00249/f00249_2013-03-29-20-46-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00250/f00250_2013-03-29-20-46-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00251/f00251_2013-03-29-20-47-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00252/f00252_2013-03-29-20-47-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00253/f00253_2013-03-29-20-47-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-29/f00254/f00254_2013-03-29-20-47-10.json'
]
e_safe8_sec = aba.loadMultipleDataFiles(e_safe8_sec)

e_safe25_first = [
'/home/vburns/Dropbox/ConchisData/2013-03-30/f00279/f00279_2013-03-30-17-05-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00280/f00280_2013-03-30-17-05-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00281/f00281_2013-03-30-17-05-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00282/f00282_2013-03-30-17-05-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00283/f00283_2013-03-30-17-07-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00284/f00284_2013-03-30-17-07-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00285/f00285_2013-03-30-17-07-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00286/f00286_2013-03-30-17-07-26.json'
]
e_safe25_first = aba.loadMultipleDataFiles(e_safe25_first)

e_shock25 = [
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00279/f00279_2013-03-30-17-38-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00280/f00280_2013-03-30-17-38-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00281/f00281_2013-03-30-17-38-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00282/f00282_2013-03-30-17-38-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00283/f00283_2013-03-30-17-39-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00284/f00284_2013-03-30-17-39-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00285/f00285_2013-03-30-17-39-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00286/f00286_2013-03-30-17-39-29.json',
]
e_shock25 = aba.loadMultipleDataFiles(e_shock25)

e_safe25_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00279/f00279_2013-03-30-18-31-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00280/f00280_2013-03-30-18-31-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00281/f00281_2013-03-30-18-32-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00282/f00282_2013-03-30-18-32-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00283/f00283_2013-03-30-18-32-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00284/f00284_2013-03-30-18-32-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00285/f00285_2013-03-30-18-32-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00286/f00286_2013-03-30-18-32-44.json'
]
e_safe25_sec = aba.loadMultipleDataFiles(e_safe25_sec)

e_round = [
#'/home/vburns/Dropbox/ConchisData/2013-04-19/f00326/f00326_2013-04-19-14-00-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00327/f00327_2013-04-19-14-00-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00328/f00328_2013-04-19-14-00-06.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-19/f00329/f00329_2013-04-19-14-00-14.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-19/f00330/f00330_2013-04-19-14-01-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00331/f00331_2013-04-19-14-01-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00332/f00332_2013-04-19-14-02-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00333/f00333_2013-04-19-14-02-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00366/f00366_2013-04-22-14-49-45.json',
'/home/vburns/Dropbox/ConchisData/2013-04-22/f00367/f00367_2013-04-22-14-49-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00368/f00368_2013-04-22-14-49-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00369/f00369_2013-04-22-14-50-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00370/f00370_2013-04-22-14-47-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00371/f00371_2013-04-22-14-47-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00372/f00372_2013-04-22-14-46-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00373/f00373_2013-04-22-14-46-47.json',
]
e_round = aba.loadMultipleDataFiles(e_round)

e_roundshock = [
#'/home/vburns/Dropbox/ConchisData/2013-04-19/f00326/f00326_2013-04-19-14-33-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00327/f00327_2013-04-19-14-33-11.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00328/f00328_2013-04-19-14-33-04.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-19/f00329/f00329_2013-04-19-14-32-59.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-19/f00330/f00330_2013-04-19-14-35-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00331/f00331_2013-04-19-14-35-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00332/f00332_2013-04-19-14-35-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00333/f00333_2013-04-19-14-35-20.json',
'/home/vburns/Dropbox/ConchisData/2013-04-22/f00366/f00366_2013-04-22-15-22-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00367/f00367_2013-04-22-15-22-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00368/f00368_2013-04-22-15-21-58.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00369/f00369_2013-04-22-15-21-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00370/f00370_2013-04-22-15-20-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00371/f00371_2013-04-22-15-20-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00372/f00372_2013-04-22-15-20-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00373/f00373_2013-04-22-15-20-11.json',
]
e_roundshock = aba.loadMultipleDataFiles(e_roundshock)

e_round_sec = [
#'/home/vburns/Dropbox/ConchisData/2013-04-19/f00326/f00326_2013-04-19-15-28-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00327/f00327_2013-04-19-15-28-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00328/f00328_2013-04-19-15-28-45.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-19/f00329/f00329_2013-04-19-15-28-52.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-19/f00330/f00330_2013-04-19-15-32-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00331/f00331_2013-04-19-15-32-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00332/f00332_2013-04-19-15-32-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00333/f00333_2013-04-19-15-32-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00366/f00366_2013-04-22-16-14-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00367/f00367_2013-04-22-16-15-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00368/f00368_2013-04-22-16-15-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00369/f00369_2013-04-22-16-15-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00370/f00370_2013-04-22-16-13-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00371/f00371_2013-04-22-16-13-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00372/f00372_2013-04-22-16-13-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00373/f00373_2013-04-22-16-13-32.json'
]
e_round_sec = aba.loadMultipleDataFiles(e_round_sec)

e_safe_same = [
'/home/vburns/Dropbox/ConchisData/2013-04-21/f00342/f00342_2013-04-21-12-30-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00343/f00343_2013-04-21-12-30-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00344/f00344_2013-04-21-12-30-17.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-21/f00345/f00345_2013-04-21-12-30-15.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-21/f00346/f00346_2013-04-21-12-32-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00347/f00347_2013-04-21-12-32-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00348/f00348_2013-04-21-12-32-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00358/f00358_2013-04-22-09-50-37.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00359/f00359_2013-04-22-09-50-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00360/f00360_2013-04-22-09-50-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00361/f00361_2013-04-22-09-50-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00362/f00362_2013-04-22-09-48-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00363/f00363_2013-04-22-09-48-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00364/f00364_2013-04-22-09-48-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00365/f00365_2013-04-22-09-48-27.json',
]
e_safe_same = aba.loadMultipleDataFiles(e_safe_same)

e_shock_same = [
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00342/f00342_2013-04-21-13-01-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00343/f00343_2013-04-21-13-01-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00344/f00344_2013-04-21-13-01-31.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-21/f00345/f00345_2013-04-21-13-01-35.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-21/f00346/f00346_2013-04-21-13-06-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00347/f00347_2013-04-21-13-06-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00348/f00348_2013-04-21-13-06-24.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00358/f00358_2013-04-22-10-25-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00359/f00359_2013-04-22-10-25-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00360/f00360_2013-04-22-10-25-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00361/f00361_2013-04-22-10-25-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00362/f00362_2013-04-22-10-24-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00363/f00363_2013-04-22-10-24-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00364/f00364_2013-04-22-10-24-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00365/f00365_2013-04-22-10-24-52.json',
]
e_shock_same = aba.loadMultipleDataFiles(e_shock_same)

e_safe_same_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00342/f00342_2013-04-21-13-55-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00343/f00343_2013-04-21-13-55-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00344/f00344_2013-04-21-13-55-08.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-21/f00345/f00345_2013-04-21-13-55-02.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-21/f00346/f00346_2013-04-21-14-00-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00347/f00347_2013-04-21-14-00-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-21/f00348/f00348_2013-04-21-14-00-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00358/f00358_2013-04-22-11-19-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00359/f00359_2013-04-22-11-19-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00360/f00360_2013-04-22-11-19-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00361/f00361_2013-04-22-11-19-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00362/f00362_2013-04-22-11-17-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00363/f00363_2013-04-22-11-17-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00364/f00364_2013-04-22-11-17-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-22/f00365/f00365_2013-04-22-11-18-03.json'
]
e_safe_same_sec = aba.loadMultipleDataFiles(e_safe_same_sec)

c_shock = [
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00255/f00255_2013-03-30-09-44-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00256/f00256_2013-03-30-09-44-40.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00257/f00257_2013-03-30-09-44-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00258/f00258_2013-03-30-09-44-36.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00259/f00259_2013-03-30-09-47-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00260/f00260_2013-03-30-09-47-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00261/f00261_2013-03-30-09-47-12.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00262/f00262_2013-03-30-09-47-10.json',
]
c_shock = aba.loadMultipleDataFiles(c_shock)
 
c_safe_first = [
'/home/vburns/Dropbox/ConchisData/2013-03-30/f00255/f00255_2013-03-30-09-13-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00256/f00256_2013-03-30-09-13-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00257/f00257_2013-03-30-09-13-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00258/f00258_2013-03-30-09-13-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00259/f00259_2013-03-30-09-15-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00260/f00260_2013-03-30-09-15-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00261/f00261_2013-03-30-09-15-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00262/f00262_2013-03-30-09-15-49.json',
]
c_safe_first = aba.loadMultipleDataFiles(c_safe_first)

c_safe_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00255/f00255_2013-03-30-10-38-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00256/f00256_2013-03-30-10-38-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00257/f00257_2013-03-30-10-38-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00258/f00258_2013-03-30-10-38-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00259/f00259_2013-03-30-10-41-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00260/f00260_2013-03-30-10-41-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00261/f00261_2013-03-30-10-41-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-03-30/f00262/f00262_2013-03-30-10-41-26.json'
]
c_safe_sec = aba.loadMultipleDataFiles(c_safe_sec)

c_shock_round = [
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00334/f00334_2013-04-19-15-35-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00335/f00335_2013-04-19-15-35-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00336/f00336_2013-04-19-15-35-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00337/f00337_2013-04-19-15-36-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00338/f00338_2013-04-19-15-38-52.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-19/f00339/f00339_2013-04-19-15-38-44.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00340/f00340_2013-04-19-15-38-36.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-19/f00341/f00341_2013-04-19-15-38-29.json',
]
c_shock_round = aba.loadMultipleDataFiles(c_shock_round)

c_round_safe = [
'/home/vburns/Dropbox/ConchisData/2013-04-19/f00334/f00334_2013-04-19-14-47-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00335/f00335_2013-04-19-14-48-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00336/f00336_2013-04-19-14-48-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00337/f00337_2013-04-19-14-48-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00338/f00338_2013-04-19-14-51-48.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-19/f00339/f00339_2013-04-19-14-51-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00340/f00340_2013-04-19-14-52-02.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-19/f00341/f00341_2013-04-19-14-51-29.json',
]
c_round_safe = aba.loadMultipleDataFiles(c_round_safe)

c_round_safe_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00334/f00334_2013-04-19-16-29-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00335/f00335_2013-04-19-16-29-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00336/f00336_2013-04-19-16-29-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00337/f00337_2013-04-19-16-29-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00338/f00338_2013-04-19-16-32-46.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-19/f00339/f00339_2013-04-19-16-32-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-04-19/f00340/f00340_2013-04-19-16-32-59.json',
# '/home/vburns/Dropbox/ConchisData/2013-04-19/f00341/f00341_2013-04-19-16-33-07.json',
]
c_round_safe_sec = aba.loadMultipleDataFiles(c_round_safe_sec)

#velocity analysis 
sm = 15; #smooth over 15 frames.

endWinLen = 5 * 60; #seconds
eEndVel5 = aba.getMedianVelMulti(e_shock5, tRange=[-endWinLen,-0], smoothWinLen=sm)
eEndVel25 = aba.getMedianVelMulti(e_shock25, tRange=[-endWinLen,-0], smoothWinLen=sm)
eEndVel8 = aba.getMedianVelMulti(e_shock8, tRange=[-endWinLen,-0], smoothWinLen=sm)
cEndVel = aba.getMedianVelMulti(c_shock, tRange=[-endWinLen,-0], smoothWinLen = sm)

eBaseVel25_1a = aba.getMedianVelMulti(e_safe25_first, (0,900), smoothWinLen = sm)
eBaseVel25_1b = aba.getMedianVelMulti(e_safe25_first, (900,1800), smoothWinLen = sm)
eBaseVel5_1a = aba.getMedianVelMulti(e_safe5_first, (0,900), smoothWinLen = sm)
eBaseVel5_1b = aba.getMedianVelMulti(e_safe5_first, (900,1800), smoothWinLen = sm)
eBaseVel8_1a = aba.getMedianVelMulti(e_safe8_first, (0,900), smoothWinLen = sm)
eBaseVel8_1b = aba.getMedianVelMulti(e_safe8_first, (900,1800), smoothWinLen = sm)
cBaseVel_1a = aba.getMedianVelMulti(c_safe_first, (0,900), smoothWinLen = sm)
cBaseVel_1b = aba.getMedianVelMulti(c_safe_first, (900,1800), smoothWinLen = sm)

eBaseVel25_2a = aba.getMedianVelMulti(e_safe25_sec, (0,900), smoothWinLen = sm)
eBaseVel25_2b = aba.getMedianVelMulti(e_safe25_sec, (900,1800), smoothWinLen = sm)
eBaseVel5_2a = aba.getMedianVelMulti(e_safe5_sec, (0,900), smoothWinLen = sm)
eBaseVel5_2b = aba.getMedianVelMulti(e_safe5_sec, (900,1800), smoothWinLen = sm)
eBaseVel8_2a = aba.getMedianVelMulti(e_safe8_sec, (0,900), smoothWinLen = sm)
eBaseVel8_2b = aba.getMedianVelMulti(e_safe8_sec, (900,1800), smoothWinLen = sm)
cBaseVel_2a = aba.getMedianVelMulti(c_safe_sec, (0,900), smoothWinLen = sm)
cBaseVel_2b = aba.getMedianVelMulti(c_safe_sec, (900,1800), smoothWinLen = sm)

eBase25 = aba.getMedianVelMulti(e_shock25, (0, 900), smoothWinLen = sm)
eBase5 = aba.getMedianVelMulti(e_shock5, (0, 900), smoothWinLen = sm)
eBase8 = aba.getMedianVelMulti(e_shock8, (0, 900), smoothWinLen = sm)
cBase = aba.getMedianVelMulti(c_shock, (0, 900), smoothWinLen = sm)

eBaseSame_1a = aba.getMedianVelMulti(e_safe_same, (0, 900), smoothWinLen = sm)
eBaseSame_1b = aba.getMedianVelMulti(e_safe_same, (900, 1800), smoothWinLen = sm)
eBaseShockSame = aba.getMedianVelMulti(e_shock_same, (0, 900), smoothWinLen = sm)
eEndShockSame = aba.getMedianVelMulti(e_shock_same, tRange=[-endWinLen, -0], smoothWinLen = sm)
eBaseSame_2a = aba.getMedianVelMulti(e_safe_same_sec, (0, 900), smoothWinLen = sm)
eBaseSame_2b = aba.getMedianVelMulti(e_safe_same_sec, (900, 1800), smoothWinLen = sm)

eBaseRound_1a = aba.getMedianVelMulti(e_round, (0, 900), smoothWinLen = sm)
eBaseRound_1b = aba.getMedianVelMulti(e_round, (900, 1800), smoothWinLen = sm)
eBaseShockRound = aba.getMedianVelMulti(e_roundshock, (0, 900), smoothWinLen = sm)
eEndShockRound = aba.getMedianVelMulti(e_roundshock, tRange=[-endWinLen, -0], smoothWinLen = sm)
eBaseRound_2a = aba.getMedianVelMulti(e_round_sec, (0,900), smoothWinLen =sm)
eBaseRound_2b = aba.getMedianVelMulti(e_round_sec, (900, 1800), smoothWinLen = sm)

cBaseRound_1a = aba.getMedianVelMulti(c_round_safe, (0, 900), smoothWinLen = sm)
cBaseRound_1b = aba.getMedianVelMulti(c_round_safe, (900, 1800), smoothWinLen = sm)
cBaseShockRound = aba.getMedianVelMulti(c_shock_round, (0, 900), smoothWinLen = sm)
cEndShockRound = aba.getMedianVelMulti(c_shock_round, tRange=[-endWinLen, -0], smoothWinLen = sm)
cBaseRound_2a = aba.getMedianVelMulti(c_round_safe_sec, (0,900), smoothWinLen =sm)
cBaseRound_2b = aba.getMedianVelMulti(c_round_safe_sec, (900, 1800), smoothWinLen = sm)

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

print 'Statistics comparing velocity between control and experimental (rec), control and experimental (same), and experimental (rec) and experimental (same) for first 15 min and last 15 min:', control_experimental_start, control_experimentalsame_start, experimental_experimentalsame_start, control_experimental, control_experimentalsame, experimental_experimentalsame

print 'Statistics comparing velocity between control and experimental (rec), control and experimental (same), and experimental (rec) and experimental (same) for second 15 min and first 15 min:', control_experimental_start1b, control_experimentalsame_start1b, experimental_experimentalsame_start1b, control_experimental2a, control_experimentalsame2a, experimental_experimentalsame2a

#fix
eEndVel25[2]= np.nan

#convert to array
eBV25_1a = np.array([np.array([eBaseVel25_1a[n]]) for n in range(len(eBaseVel25_1a))])
eBV25_1b = np.array([np.array([eBaseVel25_1b[n]]) for n in range(len(eBaseVel25_1b))])
eBV5_1a = np.array([np.array([eBaseVel5_1a[n]]) for n in range(len(eBaseVel5_1a))])
eBV5_1b = np.array([np.array([eBaseVel5_1b[n]]) for n in range(len(eBaseVel5_1b))])
eBV8_1a = np.array([np.array([eBaseVel8_1a[n]]) for n in range(len(eBaseVel8_1a))])
eBV8_1b = np.array([np.array([eBaseVel8_1b[n]]) for n in range(len(eBaseVel8_1b))])
cBV_1a = np.array([np.array([cBaseVel_1a[n]]) for n in range(len(cBaseVel_1a))])
cBV_1b = np.array([np.array([cBaseVel_1b[n]]) for n in range(len(cBaseVel_1b))])

eBV25_2a = np.array([np.array([eBaseVel25_2a[n]]) for n in range(len(eBaseVel25_2a))])
eBV25_2b = np.array([np.array([eBaseVel25_2b[n]]) for n in range(len(eBaseVel25_2b))])
eBV5_2a = np.array([np.array([eBaseVel5_2a[n]]) for n in range(len(eBaseVel5_2a))])
eBV5_2b = np.array([np.array([eBaseVel5_2b[n]]) for n in range(len(eBaseVel5_2b))])
eBV8_2a = np.array([np.array([eBaseVel8_2a[n]]) for n in range(len(eBaseVel8_2a))])
eBV8_2b = np.array([np.array([eBaseVel8_2b[n]]) for n in range(len(eBaseVel8_2b))])
cBV_2a = np.array([np.array([cBaseVel_2a[n]]) for n in range(len(cBaseVel_2a))])
cBV_2b = np.array([np.array([cBaseVel_2b[n]]) for n in range(len(cBaseVel_2b))])

eSV25 = np.array([np.array([eBase25[n]]) for n in range(len(eBase25))])
eSV5 = np.array([np.array([eBase5[n]]) for n in range(len(eBase5))])
eSV8 = np.array([np.array([eBase8[n]]) for n in range(len(eBase8))])
cSV = np.array([np.array([cBase[n]]) for n in range(len(cBase))])

eEV25 = np.array([np.array([eEndVel25[n]]) for n in range(len(eEndVel25))])
eEV5 = np.array([np.array([eEndVel5[n]]) for n in range(len(eEndVel5))])
eEV8 = np.array([np.array([eEndVel8[n]]) for n in range(len(eEndVel8))])
cEV = np.array([np.array([cEndVel[n]]) for n in range(len(cEndVel))])

eBVS_1a = np.array([np.array([eBaseSame_1a[n]]) for n in range(len(eBaseSame_1a))])
eBVS_1b = np.array([np.array([eBaseSame_1b[n]]) for n in range(len(eBaseSame_1b))])
eSVS = np.array([np.array([eBaseShockSame[n]]) for n in range(len(eBaseShockSame))])
eEVS = np.array([np.array([eEndShockSame[n]]) for n in range(len(eEndShockSame))])
eBVS_2a = np.array([np.array([eBaseSame_2a[n]]) for n in range(len(eBaseSame_2a))])
eBVS_2b = np.array([np.array([eBaseSame_2b[n]]) for n in range(len(eBaseSame_2b))])

eBVRT_1a = np.array([np.array([eBaseRound_1a[n]]) for n in range(len(eBaseRound_1a))])
eBVRT_1b = np.array([np.array([eBaseRound_1b[n]]) for n in range(len(eBaseRound_1b))])
eSRT = np.array([np.array([eBaseShockRound[n]]) for n in range(len(eBaseShockRound))])
eESRT = np.array([np.array([eEndShockRound[n]]) for n in range(len(eEndShockRound))])
eBVRT_2a = np.array([np.array([eBaseRound_2a[n]]) for n in range(len(eBaseRound_2a))])
eBVRT_2b = np.array([np.array([eBaseRound_2b[n]]) for n in range(len(eBaseRound_2b))])

cBVRT_1a = np.array([np.array([cBaseRound_1a[n]]) for n in range(len(cBaseRound_1a))])
cBVRT_1b = np.array([np.array([cBaseRound_1b[n]]) for n in range(len(cBaseRound_1b))])
cSRT = np.array([np.array([cBaseShockRound[n]]) for n in range(len(cBaseShockRound))])
cESRT = np.array([np.array([cEndShockRound[n]]) for n in range(len(cEndShockRound))])
cBVRT_2a = np.array([np.array([cBaseRound_2a[n]]) for n in range(len(cBaseRound_2a))])
cBVRT_2b = np.array([np.array([cBaseRound_2b[n]]) for n in range(len(cBaseRound_2b))])

experimental25 = np.transpose(np.hstack((eBV25_1a, eBV25_1b, eSV25, eEV25, eBV25_2a, eBV25_2b)))
experimental5 = np.transpose(np.hstack((eBV5_1a, eBV5_1b, eSV5, eEV5, eBV5_2a, eBV5_2b)))
experimental8 = np.transpose(np.hstack((eBV8_1a, eBV8_1b, eSV8, eEV8, eBV8_2a, eBV8_2b)))
experimentalsame = np.transpose(np.hstack((eBVS_1a, eBVS_1b, eSVS, eEVS, eBVS_2a, eBVS_2b)))
experimentalround = np.transpose(np.hstack((eBVRT_1a, eBVRT_1b, eSRT, eESRT, eBVRT_2a, eBVRT_2b)))
control = np.transpose(np.hstack((cBV_1a, cBV_1b, cSV, cEV, cBV_2a, cBV_2b)))
controlround = np.transpose(np.hstack((cBVRT_1a, cBVRT_1b, cSRT, cESRT, cBVRT_2a, cBVRT_2b)))

pylab.figure(100)
pylab.suptitle('Learned Helplessness Assay, Safe-Shocking-Safe, Multiple Voltages')
ax = pylab.subplot(2,2,1)
pylab.plot(experimental25)
pylab.plot(0, [eBaseVel25_1a], 'r.')
pylab.plot(1, [eBaseVel25_1b], 'r.')
pylab.plot(2,[eBase25],'r.')
pylab.plot(3, [eEndVel25], 'r.')
pylab.plot(4, [eBaseVel25_2a], 'r.')
pylab.plot(5, [eBaseVel25_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseVel25_1a), np.mean(eBaseVel25_1b), np.mean(eBase25), scipy.stats.nanmean(eEndVel25), np.mean(eBaseVel25_2a), np.mean(eBaseVel25_2b)],'o-k', lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 2.5V')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(2,2,2)
pylab.plot(experimental5)
pylab.plot(0, [eBaseVel5_1a], 'r.')
pylab.plot(1, [eBaseVel5_1b], 'r.')
pylab.plot(2,[eBase5],'r.')
pylab.plot(3, [eEndVel5], 'r.')
pylab.plot(4, [eBaseVel5_2a], 'r.')
pylab.plot(5, [eBaseVel5_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],'o-k', lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(2,2,3)
pylab.plot(experimental8)
pylab.plot(0, [eBaseVel8_1a], 'r.')
pylab.plot(1, [eBaseVel8_1b], 'r.')
pylab.plot(2,[eBase8],'r.')
pylab.plot(3, [eEndVel8], 'r.')
pylab.plot(4, [eBaseVel8_2a], 'r.')
pylab.plot(5, [eBaseVel8_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseVel8_1a), np.mean(eBaseVel8_1b), np.mean(eBase8), np.mean(eEndVel8), np.mean(eBaseVel8_2a), np.mean(eBaseVel8_2b)],'o-k', lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 8V')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(2,2,4)
pylab.plot(control)
pylab.plot(0, [cBaseVel_1a], 'r.')
pylab.plot(1, [cBaseVel_1b], 'r.')
pylab.plot(2,[cBase],'r.')
pylab.plot(3, [cEndVel], 'r.')
pylab.plot(4, [cBaseVel_2a], 'r.')
pylab.plot(5, [cBaseVel_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],'o-k', lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Control Fish')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)



pylab.figure(200)
pylab.suptitle('Learned Helplessness Assay at 5V - Safe, Shocking, Safe')
ax = pylab.subplot(2,3,1)
pylab.plot(control)
pylab.plot(0, [cBaseVel_1a], 'r.')
pylab.plot(1, [cBaseVel_1b], 'r.')
pylab.plot(2,[cBase],'r.')
pylab.plot(3, [cEndVel], 'r.')
pylab.plot(4, [cBaseVel_2a], 'r.')
pylab.plot(5, [cBaseVel_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],'o-k', lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Control Fish in Rec Tanks')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(2,3,4)
pylab.plot(controlround)
pylab.plot(0, [cBaseRound_1a], 'r.')
pylab.plot(1, [cBaseRound_1b], 'r.')
pylab.plot(2,[cBaseShockRound],'r.')
pylab.plot(3, [cEndShockRound], 'r.')
pylab.plot(4, [cBaseRound_2a], 'r.')
pylab.plot(5, [cBaseRound_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(cBaseRound_1a), np.mean(cBaseRound_1b), np.mean(cBaseShockRound), scipy.stats.nanmean(cEndShockRound), np.mean(cBaseRound_2a), np.mean(cBaseRound_2b)],'o-k', lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Control Fish in Round Tanks')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(2,3,2)
pylab.plot(experimental5)
pylab.plot(0, [eBaseVel5_1a], 'r.')
pylab.plot(1, [eBaseVel5_1b], 'r.')
pylab.plot(2,[eBase5],'r.')
pylab.plot(3, [eEndVel5], 'r.')
pylab.plot(4, [eBaseVel5_2a], 'r.')
pylab.plot(5, [eBaseVel5_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],'o-k', lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V (all rec tanks)')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(2,3,3)
pylab.plot(experimentalsame)
pylab.plot(0, [eBaseSame_1a], 'r.')
pylab.plot(1, [eBaseSame_1b], 'r.')
pylab.plot(2,[eBaseShockSame],'r.')
pylab.plot(3, [eEndShockSame], 'r.')
pylab.plot(4, [eBaseSame_2a], 'r.')
pylab.plot(5, [eBaseSame_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)],'o-k', lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V (stay in shocking tank)')
patch1 = mpl.patches.Rectangle((1.5,0), 2,5, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(2,3,5)
pylab.plot(experimentalround)
pylab.plot(0, [eBaseRound_1a], 'r.')
pylab.plot(1, [eBaseRound_1b], 'r.')
pylab.plot(2,[eBaseShockRound],'r.')
pylab.plot(3, [eEndShockRound], 'r.')
pylab.plot(4, [eBaseRound_2a], 'r.')
pylab.plot(5, [eBaseRound_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseRound_1a), np.mean(eBaseRound_1b), np.mean(eBaseShockRound), scipy.stats.nanmean(eEndShockRound), np.mean(eBaseRound_2a), np.mean(eBaseRound_2b)],'o-k', lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental Fish at 5V (Round Tanks = safe)')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)


pylab.figure(400)
pylab.suptitle('Summary of Median Velocities (mm/s)')
ax = pylab.subplot(1,1,1)
control = ax.plot([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],'o-k', lw=3, label='Control Fish: Safe = colored')
experimental5 = ax.plot([0,1,2,3,4,5],[np.mean(eBaseVel5_1a), np.mean(eBaseVel5_1b), np.mean(eBase5), np.mean(eEndVel5), np.mean(eBaseVel5_2a), np.mean(eBaseVel5_2b)],'o-b', lw=3, label='Experimental Fish (5V): Safe = colored')
experimentalsame = ax.plot([0,1,2,3,4,5],[np.mean(eBaseSame_1a), np.mean(eBaseSame_1b), np.mean(eBaseShockSame), np.mean(eEndShockSame), np.mean(eBaseSame_2a), np.mean(eBaseSame_2b)],'o-g', lw=3, label='Experimental Fish (5V): Safe = shocking tank')
control_round = ax.plot([0,1,2,3,4,5],[np.mean(cBaseRound_1a), np.mean(cBaseRound_1b), np.mean(cBaseShockRound), scipy.stats.nanmean(cEndShockRound), np.mean(cBaseRound_2a), np.mean(cBaseRound_2b)],'o--k', lw=3, label='Control Fish: Safe = round')
experimentalround = ax.plot([0,1,2,3,4,5],[np.mean(eBaseRound_1a), np.mean(eBaseRound_1b), np.mean(eBaseShockRound), scipy.stats.nanmean(eEndShockRound), np.mean(eBaseRound_2a), np.mean(eBaseRound_2b)],'o--m', lw=3, label='Experimental Fish (5V): Safe = round')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline\n shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')


pylab.show()

