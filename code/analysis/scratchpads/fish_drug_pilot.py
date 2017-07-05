import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy
import os

five_fluox_first = [
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00889/f00889_2014-02-12-09-55-46.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00890/f00890_2014-02-12-09-55-49.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00891/f00891_2014-02-12-09-55-51.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00892/f00892_2014-02-12-09-55-54.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00893/f00893_2014-02-12-09-55-57.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00894/f00894_2014-02-12-09-56-00.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00895/f00895_2014-02-12-09-56-02.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00896/f00896_2014-02-12-09-56-05.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00897/f00897_2014-02-12-09-57-24.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00898/f00898_2014-02-12-09-57-29.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00899/f00899_2014-02-12-09-57-32.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00900/f00900_2014-02-12-09-57-35.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00901/f00901_2014-02-12-09-57-38.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00902/f00902_2014-02-12-09-57-41.json',
]
five_fluox_first = aba.loadMultipleDataFiles(five_fluox_first)

five_fluox_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00889/f00889_2014-02-12-10-51-36.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00890/f00890_2014-02-12-10-51-31.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00891/f00891_2014-02-12-10-51-25.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00892/f00892_2014-02-12-10-51-20.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00893/f00893_2014-02-12-10-51-14.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00894/f00894_2014-02-12-10-51-07.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00895/f00895_2014-02-12-10-50-59.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00896/f00896_2014-02-12-10-50-55.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00897/f00897_2014-02-12-10-53-20.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00898/f00898_2014-02-12-10-53-07.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00899/f00899_2014-02-12-10-52-53.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00900/f00900_2014-02-12-10-52-35.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00901/f00901_2014-02-12-10-52-25.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00902/f00902_2014-02-12-10-52-14.json']
five_fluox_sec = aba.loadMultipleDataFiles(five_fluox_sec)

five_imip_first = [
'/home/vburns/Dropbox/ConchisData/2014-02-12/f00905/f00905_2014-02-12-11-28-03.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00906/f00906_2014-02-12-11-28-05.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00907/f00907_2014-02-12-11-28-08.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00908/f00908_2014-02-12-11-28-12.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00909/f00909_2014-02-12-11-28-14.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00910/f00910_2014-02-12-11-28-17.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00911/f00911_2014-02-12-11-28-20.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00912/f00912_2014-02-12-11-28-22.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00913/f00913_2014-02-12-11-35-44.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00914/f00914_2014-02-12-11-35-38.json',
]
five_imip_first = aba.loadMultipleDataFiles(five_imip_first)

five_imip_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00905/f00905_2014-02-12-12-25-09.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00906/f00906_2014-02-12-12-25-01.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00907/f00907_2014-02-12-12-24-57.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00908/f00908_2014-02-12-12-24-50.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00909/f00909_2014-02-12-12-24-36.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00910/f00910_2014-02-12-12-24-30.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00911/f00911_2014-02-12-12-24-24.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00912/f00912_2014-02-12-12-24-16.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00913/f00913_2014-02-12-12-29-58.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00914/f00914_2014-02-12-12-29-51.json',
]
five_imip_sec = aba.loadMultipleDataFiles(five_imip_sec)

five_bupro_first = [
'/home/vburns/Dropbox/ConchisData/2014-02-13/f00921/f00921_2014-02-13-12-43-54.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00922/f00922_2014-02-13-12-43-47.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00923/f00923_2014-02-13-12-43-39.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00924/f00924_2014-02-13-12-43-32.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00925/f00925_2014-02-13-12-43-23.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00926/f00926_2014-02-13-12-43-17.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00927/f00927_2014-02-13-12-43-08.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00928/f00928_2014-02-13-12-43-02.json',
]
five_bupro_first = aba.loadMultipleDataFiles(five_bupro_first)

five_bupro_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00921/f00921_2014-02-13-13-39-48.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00922/f00922_2014-02-13-13-39-43.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00923/f00923_2014-02-13-13-39-37.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00924/f00924_2014-02-13-13-39-32.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00925/f00925_2014-02-13-13-39-26.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00926/f00926_2014-02-13-13-39-18.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00927/f00927_2014-02-13-13-39-08.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00928/f00928_2014-02-13-13-38-55.json',
]
five_bupro_sec = aba.loadMultipleDataFiles(five_bupro_sec)

five_traz_first = [
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00929/f00929_2014-02-13-12-47-22.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00930/f00930_2014-02-13-12-47-14.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00931/f00931_2014-02-13-12-47-06.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00932/f00932_2014-02-13-12-47-01.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00933/f00933_2014-02-13-12-46-54.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00934/f00934_2014-02-13-12-46-47.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00935/f00935_2014-02-13-12-46-39.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00936/f00936_2014-02-13-12-46-29.json',
]
five_traz_first = aba.loadMultipleDataFiles(five_traz_first)

five_traz_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00929/f00929_2014-02-13-13-42-03.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00930/f00930_2014-02-13-13-42-18.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00931/f00931_2014-02-13-13-42-24.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00932/f00932_2014-02-13-13-42-27.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00933/f00933_2014-02-13-13-42-31.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00934/f00934_2014-02-13-13-42-38.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00935/f00935_2014-02-13-13-42-43.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-13/f00936/f00936_2014-02-13-13-42-47.json',
]
five_traz_sec = aba.loadMultipleDataFiles(five_traz_sec)

twenty_fluox_first = [
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00903/f00903_2014-02-12-09-57-45.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00904/f00904_2014-02-12-09-57-48.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00915/f00915_2014-02-12-11-35-31.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00916/f00916_2014-02-12-11-35-26.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00917/f00917_2014-02-12-11-35-18.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00918/f00918_2014-02-12-11-35-05.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00919/f00919_2014-02-12-11-35-02.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00920/f00920_2014-02-12-11-34-54.json',
]
twenty_fluox_first = aba.loadMultipleDataFiles(twenty_fluox_first)

twenty_fluox_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00903/f00903_2014-02-12-10-52-02.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00904/f00904_2014-02-12-10-51-52.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00915/f00915_2014-02-12-12-29-44.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00916/f00916_2014-02-12-12-29-39.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00917/f00917_2014-02-12-12-29-33.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00918/f00918_2014-02-12-12-29-26.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00919/f00919_2014-02-12-12-29-22.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-12/f00920/f00920_2014-02-12-12-29-15.json',
]
twenty_fluox_sec = aba.loadMultipleDataFiles(twenty_fluox_sec)

twenty_bupro_first = [
'/home/vburns/Dropbox/ConchisData/2014-02-14/f00937/f00937_2014-02-14-09-23-09.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00938/f00938_2014-02-14-09-23-00.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00939/f00939_2014-02-14-09-22-51.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00940/f00940_2014-02-14-09-22-43.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00941/f00941_2014-02-14-09-22-34.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00942/f00942_2014-02-14-09-22-26.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00943/f00943_2014-02-14-09-22-11.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00952/f00943_2014-02-14-09-22-18.json',
]
twenty_bupro_first = aba.loadMultipleDataFiles(twenty_bupro_first)

twenty_bupro_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00937/f00937_2014-02-14-10-17-38.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00938/f00938_2014-02-14-10-17-34.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00939/f00939_2014-02-14-10-17-28.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00940/f00940_2014-02-14-10-17-21.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00941/f00941_2014-02-14-10-17-14.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00942/f00942_2014-02-14-10-17-09.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00943/f00943_2014-02-14-10-16-55.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00952/f00943_2014-02-14-10-17-03.json',
]
twenty_bupro_sec = aba.loadMultipleDataFiles(twenty_bupro_sec)

five_bupro_overnight_first = [
'/home/vburns/Dropbox/ConchisData/2014-02-14/f00944/f00944_2014-02-14-09-29-36.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00945/f00945_2014-02-14-09-29-28.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00946/f00946_2014-02-14-09-29-18.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00947/f00947_2014-02-14-09-29-09.json',
]
five_bupro_overnight_first = aba.loadMultipleDataFiles(five_bupro_overnight_first)

five_bupro_overnight_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00944/f00944_2014-02-14-10-22-50.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00945/f00945_2014-02-14-10-22-54.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00946/f00946_2014-02-14-10-23-02.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00947/f00947_2014-02-14-10-23-09.json',
]
five_bupro_overnight_sec = aba.loadMultipleDataFiles(five_bupro_overnight_sec)

five_traz_overnight_first = [
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00948/f00948_2014-02-14-09-28-58.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00949/f00949_2014-02-14-09-28-13.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00950/f00950_2014-02-14-09-27-59.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00951/f00951_2014-02-14-09-27-51.json',
]
five_traz_overnight_first = aba.loadMultipleDataFiles(five_traz_overnight_first)

five_traz_overnight_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00948/f00948_2014-02-14-10-23-15.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00949/f00949_2014-02-14-10-23-19.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00950/f00950_2014-02-14-10-23-24.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-14/f00951/f00951_2014-02-14-10-23-27.json',
]
five_traz_overnight_sec = aba.loadMultipleDataFiles(five_traz_overnight_sec)

fifty_bupro_first = [
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00953/f00953_2014-02-18-10-19-56.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00954/f00954_2014-02-18-10-20-02.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00955/f00955_2014-02-18-10-20-09.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00956/f00956_2014-02-18-10-20-18.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00957/f00957_2014-02-18-10-20-24.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00958/f00958_2014-02-18-10-20-31.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00959/f00959_2014-02-18-10-20-42.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00960/f00960_2014-02-18-10-20-49.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01089/f01089_2014-03-05-16-41-22.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01090/f01090_2014-03-05-16-41-28.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01091/f01091_2014-03-05-16-41-32.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01092/f01092_2014-03-05-16-41-35.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01093/f01093_2014-03-05-16-41-38.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01094/f01094_2014-03-05-16-41-42.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01095/f01095_2014-03-05-16-41-47.json',
]
fifty_bupro_first = aba.loadMultipleDataFiles(fifty_bupro_first)

fifty_bupro_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00953/f00953_2014-02-18-11-16-05.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00954/f00954_2014-02-18-11-16-12.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00955/f00955_2014-02-18-11-16-18.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00956/f00956_2014-02-18-11-16-24.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00957/f00957_2014-02-18-11-16-31.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00958/f00958_2014-02-18-11-16-39.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00959/f00959_2014-02-18-11-16-51.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00960/f00960_2014-02-18-11-16-59.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01089/f01089_2014-03-05-17-39-18.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01090/f01090_2014-03-05-17-39-24.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01091/f01091_2014-03-05-17-39-34.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01092/f01092_2014-03-05-17-39-56.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01093/f01093_2014-03-05-17-40-11.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01094/f01094_2014-03-05-17-40-20.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01095/f01095_2014-03-05-17-40-50.json',
]
fifty_bupro_sec = aba.loadMultipleDataFiles(fifty_bupro_sec)

hundred_bupro_first = [
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00961/f00961_2014-02-18-10-22-05.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00962/f00962_2014-02-18-10-21-52.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00963/f00963_2014-02-18-10-21-44.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00964/f00964_2014-02-18-10-21-38.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00965/f00965_2014-02-18-10-21-28.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00966/f00966_2014-02-18-10-21-20.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00967/f00967_2014-02-18-10-21-09.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00968/f00968_2014-02-18-10-20-59.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01057/f01057_2014-02-25-14-17-25.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01058/f01058_2014-02-25-14-17-34.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01059/f01059_2014-02-25-14-17-48.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01060/f01060_2014-02-25-14-17-57.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01061/f01061_2014-02-25-14-18-03.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01062/f01062_2014-02-25-14-18-13.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01063/f01063_2014-02-25-14-18-23.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01064/f01064_2014-02-25-14-18-29.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01096/f01096_2014-03-05-16-41-51.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01097/f01097_2014-03-05-16-41-56.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01098/f01098_2014-03-05-16-42-00.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01099/f01099_2014-03-05-16-42-03.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01100/f01100_2014-03-05-16-42-06.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01101/f01101_2014-03-05-16-42-11.json',
]
hundred_bupro_first = aba.loadMultipleDataFiles(hundred_bupro_first)

hundred_bupro_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00961/f00961_2014-02-18-11-17-53.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00962/f00962_2014-02-18-11-17-48.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00963/f00963_2014-02-18-11-17-41.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00964/f00964_2014-02-18-11-17-35.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00965/f00965_2014-02-18-11-17-28.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00966/f00966_2014-02-18-11-17-21.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00967/f00967_2014-02-18-11-17-13.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-18/f00968/f00968_2014-02-18-11-17-04.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01057/f01057_2014-02-25-15-15-16.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01058/f01058_2014-02-25-15-15-22.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01059/f01059_2014-02-25-15-15-30.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01060/f01060_2014-02-25-15-15-37.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01061/f01061_2014-02-25-15-15-42.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01062/f01062_2014-02-25-15-15-48.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01063/f01063_2014-02-25-15-15-53.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01064/f01064_2014-02-25-15-16-00.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01096/f01096_2014-03-05-17-41-11.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01097/f01097_2014-03-05-17-42-57.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01098/f01098_2014-03-05-17-43-11.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01099/f01099_2014-03-05-17-43-21.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01100/f01100_2014-03-05-17-43-31.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01101/f01101_2014-03-05-17-43-38.json',
]
hundred_bupro_sec = aba.loadMultipleDataFiles(hundred_bupro_sec)

hundred_bupro_first_1 = [hundred_bupro_first[x] for x in np.arange(7)]
hundred_bupro_sec_1 = [hundred_bupro_sec[x] for x in np.arange(7)]
hundred_bupro_first_2 = [hundred_bupro_first[x] for x in np.arange(8,16)]
hundred_bupro_sec_2 = [hundred_bupro_sec[x] for x in np.arange(8,16)]

pt1_imapramine_first= [
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01041/f01041_2014-02-25-12-24-11.json',
# '/home/vburns/Dropbox/ConchisData/2014-02-25/f01042/f01042_2014-02-25-12-24-17.json', #random error
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01043/f01043_2014-02-25-12-24-25.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01044/f01044_2014-02-25-12-24-34.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01045/f01045_2014-02-25-12-24-44.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01046/f01046_2014-02-25-12-24-53.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01047/f01047_2014-02-25-12-25-06.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01048/f01048_2014-02-25-12-25-14.json',
]
pt1_imapramine_first = aba.loadMultipleDataFiles(pt1_imapramine_first)

pt1_imapramine_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01041/f01041_2014-02-25-13-26-57.json',
# '/home/vburns/Dropbox/ConchisData/2014-02-25/f01042/f01042_2014-02-25-13-26-51.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01043/f01043_2014-02-25-13-26-44.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01044/f01044_2014-02-25-13-26-38.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01045/f01045_2014-02-25-13-26-29.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01046/f01046_2014-02-25-13-26-22.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01047/f01047_2014-02-25-13-26-13.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01048/f01048_2014-02-25-13-26-15.json',
]
pt1_imapramine_sec = aba.loadMultipleDataFiles(pt1_imapramine_sec)

pt01_imapramine_first= [
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01049/f01049_2014-02-25-12-23-32.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01050/f01050_2014-02-25-12-23-35.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01051/f01051_2014-02-25-12-23-38.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01052/f01052_2014-02-25-12-23-40.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01053/f01053_2014-02-25-12-23-51.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01054/f01054_2014-02-25-12-23-55.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01055/f01055_2014-02-25-12-23-58.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01056/f01056_2014-02-25-12-24-00.json',
]
pt01_imapramine_first = aba.loadMultipleDataFiles(pt01_imapramine_first)

pt01_imapramine_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01049/f01049_2014-02-25-13-27-38.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01050/f01050_2014-02-25-13-27-33.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01051/f01051_2014-02-25-13-27-28.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01052/f01052_2014-02-25-13-27-24.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01053/f01053_2014-02-25-13-27-19.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01054/f01054_2014-02-25-13-27-14.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01055/f01055_2014-02-25-13-27-09.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01056/f01056_2014-02-25-13-27-04.json',
]
pt01_imapramine_sec = aba.loadMultipleDataFiles(pt01_imapramine_sec)

twoum_imapramine_first = [
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01073/f01073_2014-03-05-14-35-37.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01074/f01074_2014-03-05-14-35-40.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01075/f01075_2014-03-05-14-35-44.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01076/f01076_2014-03-05-14-35-47.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01077/f01077_2014-03-05-14-35-50.json',
]
twoum_imapramine_first = aba.loadMultipleDataFiles(twoum_imapramine_first)

twoum_imapramine_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01073/f01073_2014-03-05-15-32-41.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01074/f01074_2014-03-05-15-32-44.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01075/f01075_2014-03-05-15-32-47.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01076/f01076_2014-03-05-15-32-57.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01077/f01077_2014-03-05-15-33-05.json',
]
twoum_imapramine_sec = aba.loadMultipleDataFiles(twoum_imapramine_sec)

pt05_imapramine_first = [
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01081/f01081_2014-03-05-14-37-15.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01082/f01082_2014-03-05-14-37-12.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01083/f01083_2014-03-05-14-37-07.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01084/f01084_2014-03-05-14-37-04.json',
# '/home/vburns/Dropbox/ConchisData/2014-03-05/f01085/f01085_2014-03-05-14-37-02.json',
# '/home/vburns/Dropbox/ConchisData/2014-03-05/f01086/f01086_2014-03-05-14-36-37.json',
]
pt05_imapramine_first = aba.loadMultipleDataFiles(pt05_imapramine_first)

pt05_imapramine_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01081/f01081_2014-03-05-15-34-28.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01082/f01082_2014-03-05-15-34-20.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01083/f01083_2014-03-05-15-34-02.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-05/f01084/f01084_2014-03-05-15-33-57.json',
# '/home/vburns/Dropbox/ConchisData/2014-03-05/f01085/f01085_2014-03-05-15-33-48.json',
# '/home/vburns/Dropbox/ConchisData/2014-03-05/f01086/f01086_2014-03-05-15-33-43.json',
]
pt05_imapramine_sec = aba.loadMultipleDataFiles(pt05_imapramine_sec)


twohundred_burpo_first = [
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01065/f01065_2014-02-25-14-19-47.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01066/f01066_2014-02-25-14-19-39.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01067/f01067_2014-02-25-14-19-31.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01068/f01068_2014-02-25-14-19-23.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01069/f01069_2014-02-25-14-19-00.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01070/f01070_2014-02-25-14-18-52.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01071/f01071_2014-02-25-14-18-45.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01072/f01072_2014-02-25-14-18-36.json',
]
twohundred_burpo_first = aba.loadMultipleDataFiles(twohundred_burpo_first)

twohundred_burpo_sec = [
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01065/f01065_2014-02-25-15-16-54.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01066/f01066_2014-02-25-15-16-50.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01067/f01067_2014-02-25-15-16-40.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01068/f01068_2014-02-25-15-16-34.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01069/f01069_2014-02-25-15-16-26.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01070/f01070_2014-02-25-15-16-18.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01071/f01071_2014-02-25-15-16-12.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-25/f01072/f01072_2014-02-25-15-16-06.json',
]
twohundred_burpo_sec = aba.loadMultipleDataFiles(twohundred_burpo_sec)

print "Done loading fish."

#data available: 
alldat = [five_fluox_first, five_imip_first, five_bupro_first, five_traz_first, twenty_fluox_first, twenty_bupro_first, five_bupro_overnight_first, five_traz_overnight_first, fifty_bupro_first, hundred_bupro_first,pt1_imapramine_first,pt01_imapramine_first, twoum_imapramine_first, pt05_imapramine_first, twohundred_burpo_first]  

bupdata = [five_bupro_first, five_bupro_sec,twenty_bupro_first, twenty_bupro_sec, fifty_bupro_first, fifty_bupro_sec, hundred_bupro_first, hundred_bupro_sec, twohundred_burpo_first, twohundred_burpo_sec]
print len(bupdata)

imadata = [pt01_imapramine_first, pt01_imapramine_sec, pt05_imapramine_first, pt05_imapramine_sec, pt1_imapramine_first, pt1_imapramine_sec, twoum_imapramine_first, twoum_imapramine_sec, five_imip_first, five_imip_sec]
print len(imadata)

