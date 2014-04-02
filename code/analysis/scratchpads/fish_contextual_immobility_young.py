import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy
import os

#first is 30 min in safe tank, then standard shocking, then 30 min in safe tank
e_shock = [
'/home/vburns/Dropbox/ConchisData/2013-11-21/f00881/f00881_2013-11-21-16-15-27.json',
# '/home/vburns/Dropbox/ConchisData/2013-11-21/f00882/f00882_2013-11-21-16-15-30.json', #tracking in sec
 '/home/vburns/Dropbox/ConchisData/2013-11-21/f00883/f00883_2013-11-21-16-15-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-21/f00884/f00884_2013-11-21-16-15-37.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-21/f00885/f00885_2013-11-21-16-15-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-21/f00886/f00886_2013-11-21-16-15-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-21/f00887/f00887_2013-11-21-16-16-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-21/f00888/f00888_2013-11-21-16-16-09.json',
]
e_shock = aba.loadMultipleDataFiles(e_shock)

e_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-11-21/f00881/f00881_2013-11-21-17-10-04.json',
# '/home/vburns/Dropbox/ConchisData/2013-11-21/f00882/f00882_2013-11-21-17-10-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-21/f00883/f00883_2013-11-21-17-10-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-21/f00884/f00884_2013-11-21-17-10-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-21/f00885/f00885_2013-11-21-17-10-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-21/f00886/f00886_2013-11-21-17-10-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-21/f00887/f00887_2013-11-21-17-10-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-21/f00888/f00888_2013-11-21-17-10-56.json',
]
e_sec = aba.loadMultipleDataFiles(e_sec)

#fish kept in same tank after shocking
e_same_shock = [
'/home/vburns/Dropbox/ConchisData/2013-11-20/f00865/f00865_2013-11-20-17-16-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00866/f00866_2013-11-20-17-16-39.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00867/f00867_2013-11-20-17-16-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00868/f00868_2013-11-20-17-17-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00869/f00869_2013-11-20-17-17-09.json',
# '/home/vburns/Dropbox/ConchisData/2013-11-20/f00870/f00870_2013-11-20-17-17-17.json', #tracking in sec
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00871/f00871_2013-11-20-17-17-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00872/f00872_2013-11-20-17-17-29.json',

]
e_same_shock = aba.loadMultipleDataFiles(e_same_shock)

e_same_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00865/f00865_2013-11-20-18-12-58.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00866/f00866_2013-11-20-18-12-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00867/f00867_2013-11-20-18-12-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00868/f00868_2013-11-20-18-12-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00869/f00869_2013-11-20-18-12-42.json',
# '/home/vburns/Dropbox/ConchisData/2013-11-20/f00870/f00870_2013-11-20-18-12-37.json', 
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00871/f00871_2013-11-20-18-12-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00872/f00872_2013-11-20-18-12-26.json'
]
e_same_sec = aba.loadMultipleDataFiles(e_same_sec)

c_shock = [
'/home/vburns/Dropbox/ConchisData/2013-11-20/f00873/f00873_2013-11-20-17-17-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00874/f00874_2013-11-20-17-17-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00875/f00875_2013-11-20-17-17-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00876/f00876_2013-11-20-17-18-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00877/f00877_2013-11-20-17-18-28.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00878/f00878_2013-11-20-17-18-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00879/f00879_2013-11-20-17-18-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00880/f00880_2013-11-20-17-18-52.json',
]
c_shock = aba.loadMultipleDataFiles(c_shock)
 
c_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00873/f00873_2013-11-20-18-14-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00874/f00874_2013-11-20-18-14-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00875/f00875_2013-11-20-18-14-27.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00876/f00876_2013-11-20-18-14-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00877/f00877_2013-11-20-18-14-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00878/f00878_2013-11-20-18-15-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00879/f00879_2013-11-20-18-15-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-11-20/f00880/f00880_2013-11-20-18-15-37.json'
]
c_sec = aba.loadMultipleDataFiles(c_sec)

print "Done loading fish."
