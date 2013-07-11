import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

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

#this is rotating tanks with different water, same color
e_waterrotateS_first = [
'/home/vburns/Dropbox/ConchisData/2013-05-17/f00454/f00454_2013-05-17-15-23-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00455/f00455_2013-05-17-15-23-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00456/f00456_2013-05-17-15-23-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00457/f00457_2013-05-17-15-23-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00460/f00460_2013-05-17-15-26-44.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00461/f00461_2013-05-17-15-26-49.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00478/f00478_2013-05-28-12-58-40.json', #tracking
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00479/f00479_2013-05-28-12-58-42.json', #low velocity in start of SHOCK
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00480/f00480_2013-05-28-12-58-44.json', #tracking
 '/home/vburns/Dropbox/ConchisData/2013-05-28/f00481/f00481_2013-05-28-12-58-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-28/f00482/f00482_2013-05-28-13-00-49.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00483/f00483_2013-05-28-13-00-47.json', #current imbalance
 '/home/vburns/Dropbox/ConchisData/2013-05-28/f00484/f00484_2013-05-28-13-00-46.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00485/f00485_2013-05-28-13-00-43.json', #tracking
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00538/f00538_2013-06-15-13-09-58.json', 
# '/home/vburns/Dropbox/ConchisData/2013-06-15/f00539/f00539_2013-06-15-13-09-56.json',# low starting velocity
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00540/f00540_2013-06-15-13-09-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00541/f00541_2013-06-15-13-09-51.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-15/f00542/f00542_2013-06-15-13-11-47.json', #tracking
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00543/f00543_2013-06-15-13-11-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00544/f00544_2013-06-15-13-11-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00545/f00545_2013-06-15-13-11-40.json',
]
e_waterrotateS_first = aba.loadMultipleDataFiles(e_waterrotateS_first)

e_waterrotateS_shock = [
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00454/f00454_2013-05-17-15-54-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00455/f00455_2013-05-17-15-54-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00456/f00456_2013-05-17-15-54-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00457/f00457_2013-05-17-15-54-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00460/f00460_2013-05-17-15-58-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00461/f00461_2013-05-17-15-58-06.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00478/f00478_2013-05-28-13-30-03.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00479/f00479_2013-05-28-13-29-56.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00480/f00480_2013-05-28-13-29-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-28/f00481/f00481_2013-05-28-13-29-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-28/f00482/f00482_2013-05-28-13-31-56.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00483/f00483_2013-05-28-13-32-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-28/f00484/f00484_2013-05-28-13-32-10.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00485/f00485_2013-05-28-13-32-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00538/f00538_2013-06-15-13-42-34.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-15/f00539/f00539_2013-06-15-13-42-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00540/f00540_2013-06-15-13-42-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00541/f00541_2013-06-15-13-42-27.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-15/f00542/f00542_2013-06-15-13-45-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00543/f00543_2013-06-15-13-44-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00544/f00544_2013-06-15-13-44-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00545/f00545_2013-06-15-13-44-22.json',
]
e_waterrotateS_shock = aba.loadMultipleDataFiles(e_waterrotateS_shock)

e_waterrotateS_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00454/f00454_2013-05-17-16-48-22.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00455/f00455_2013-05-17-16-48-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00456/f00456_2013-05-17-16-48-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00457/f00457_2013-05-17-16-48-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00460/f00460_2013-05-17-16-51-37.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00461/f00461_2013-05-17-16-51-33.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00478/f00478_2013-05-28-14-24-44.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00479/f00479_2013-05-28-14-24-46.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00480/f00480_2013-05-28-14-24-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-28/f00481/f00481_2013-05-28-14-24-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-28/f00482/f00482_2013-05-28-14-26-40.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00483/f00483_2013-05-28-14-26-42.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-28/f00484/f00484_2013-05-28-14-26-44.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-28/f00485/f00485_2013-05-28-14-26-46.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00538/f00538_2013-06-15-14-37-17.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-15/f00539/f00539_2013-06-15-14-37-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00540/f00540_2013-06-15-14-37-25.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00541/f00541_2013-06-15-14-37-32.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-15/f00542/f00542_2013-06-15-14-40-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00543/f00543_2013-06-15-14-40-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00544/f00544_2013-06-15-14-40-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00545/f00545_2013-06-15-14-40-03.json',
]
e_waterrotateS_sec = aba.loadMultipleDataFiles(e_waterrotateS_sec)

#rotating tanks, different water, different color
e_waterrotateD_first = [
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00458/f00458_2013-05-17-15-26-34.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-17/f00459/f00459_2013-05-17-15-26-38.json', #current imbalance
# '/home/vburns/Dropbox/ConchisData/2013-05-29/f00486/f00486_2013-05-29-09-35-06.json', #current imbalance
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00487/f00487_2013-05-29-09-35-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00488/f00488_2013-05-29-09-35-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00489/f00489_2013-05-29-09-35-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00490/f00490_2013-05-29-09-33-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00491/f00491_2013-05-29-09-33-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00492/f00492_2013-05-29-09-33-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00493/f00493_2013-05-29-09-32-58.json',
#'/home/vburns/Dropbox/ConchisData/2013-06-15/f00546/f00546_2013-06-15-15-21-37.json', #current imbalance
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00547/f00547_2013-06-15-15-21-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00548/f00548_2013-06-15-15-21-24.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-15/f00550/f00550_2013-06-15-15-22-39.json', #tracking in shock
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00551/f00551_2013-06-15-15-22-47.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-15/f00552/f00552_2013-06-15-15-22-53.json', #tracking
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00553/f00553_2013-06-15-15-23-00.json',
]
e_waterrotateD_first = aba.loadMultipleDataFiles(e_waterrotateD_first)

e_waterrotateD_shock = [
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00458/f00458_2013-05-17-15-58-12.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-17/f00459/f00459_2013-05-17-15-57-51.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-29/f00486/f00486_2013-05-29-10-06-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00487/f00487_2013-05-29-10-07-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00488/f00488_2013-05-29-10-07-10.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00489/f00489_2013-05-29-10-07-15.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00490/f00490_2013-05-29-10-04-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00491/f00491_2013-05-29-10-04-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00492/f00492_2013-05-29-10-04-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00493/f00493_2013-05-29-10-04-54.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-15/f00546/f00546_2013-06-15-15-53-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00547/f00547_2013-06-15-15-53-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00548/f00548_2013-06-15-15-53-27.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-15/f00550/f00550_2013-06-15-15-54-38.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00551/f00551_2013-06-15-15-54-48.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-15/f00552/f00552_2013-06-15-15-54-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00553/f00553_2013-06-15-15-55-08.json',
]
e_waterrotateD_shock = aba.loadMultipleDataFiles(e_waterrotateD_shock)

e_waterrotateD_sec = [
 '/home/vburns/Dropbox/ConchisData/2013-05-17/f00458/f00458_2013-05-17-16-51-29.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-17/f00459/f00459_2013-05-17-16-51-26.json',
# '/home/vburns/Dropbox/ConchisData/2013-05-29/f00486/f00486_2013-05-29-11-07-54.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00487/f00487_2013-05-29-11-07-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00488/f00488_2013-05-29-11-08-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00489/f00489_2013-05-29-11-08-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00490/f00490_2013-05-29-11-07-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00491/f00491_2013-05-29-11-07-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00492/f00492_2013-05-29-11-07-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-05-29/f00493/f00493_2013-05-29-11-07-41.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-15/f00546/f00546_2013-06-15-16-47-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00547/f00547_2013-06-15-16-48-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00548/f00548_2013-06-15-16-48-11.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-15/f00550/f00550_2013-06-15-16-50-29.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00551/f00551_2013-06-15-16-50-22.json',
# '/home/vburns/Dropbox/ConchisData/2013-06-15/f00552/f00552_2013-06-15-16-50-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-06-15/f00553/f00553_2013-06-15-16-50-10.json'
]
e_waterrotateD_sec = aba.loadMultipleDataFiles(e_waterrotateD_sec)

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

cBaseVel_1a = aba.getMedianVelMulti(c_safe_first, (0,900), smoothWinLen = sm)
cBaseVel_1b = aba.getMedianVelMulti(c_safe_first, (900,1800), smoothWinLen = sm)
cBaseVel_2a = aba.getMedianVelMulti(c_safe_sec, (0,900), smoothWinLen = sm)
cBaseVel_2b = aba.getMedianVelMulti(c_safe_sec, (900,1800), smoothWinLen = sm)

eBaseVelW_1a = aba.getMedianVelMulti(e_water_first, (0,900), smoothWinLen = sm)
eBaseVelW_1b = aba.getMedianVelMulti(e_water_first, (900,1800), smoothWinLen = sm)
eBaseVelW_2a = aba.getMedianVelMulti(e_water_sec, (0,900), smoothWinLen = sm)
eBaseVelW_2b = aba.getMedianVelMulti(e_water_sec, (900,1800), smoothWinLen = sm)
eBaseW = aba.getMedianVelMulti(e_water_shock, (0,900), smoothWinLen=sm)
eEndVelW = aba.getMedianVelMulti(e_water_shock, tRange=[-endWinLen,-0], smoothWinLen=sm)

eBaseVelWR_1a = aba.getMedianVelMulti(e_waterrotateS_first, (0,900), smoothWinLen = sm)
eBaseVelWR_1b = aba.getMedianVelMulti(e_waterrotateS_first, (900,1800), smoothWinLen = sm)
eBaseVelWR_2a = aba.getMedianVelMulti(e_waterrotateS_sec, (0,900), smoothWinLen = sm)
eBaseVelWR_2b = aba.getMedianVelMulti(e_waterrotateS_sec, (900,1800), smoothWinLen = sm)
eBaseWR = aba.getMedianVelMulti(e_waterrotateS_shock, (0,900), smoothWinLen=sm)
eEndVelWR = aba.getMedianVelMulti(e_waterrotateS_shock, tRange=[-endWinLen,-0], smoothWinLen=sm)

eBaseVelWRD_1a = aba.getMedianVelMulti(e_waterrotateD_first, (0,900), smoothWinLen = sm)
eBaseVelWRD_1b = aba.getMedianVelMulti(e_waterrotateD_first, (900,1800), smoothWinLen = sm)
eBaseVelWRD_2a = aba.getMedianVelMulti(e_waterrotateD_sec, (0,900), smoothWinLen = sm)
eBaseVelWRD_2b = aba.getMedianVelMulti(e_waterrotateD_sec, (900,1800), smoothWinLen = sm)
eBaseWRD = aba.getMedianVelMulti(e_waterrotateD_shock, (0,900), smoothWinLen=sm)
eEndVelWRD = aba.getMedianVelMulti(e_waterrotateD_shock, tRange=[-endWinLen,-0], smoothWinLen=sm)

cBase = aba.getMedianVelMulti(c_shock, (0, 900), smoothWinLen = sm)
cEndVel = aba.getMedianVelMulti(c_shock, tRange=[-endWinLen,-0], smoothWinLen = sm)

#comparisons 
[tv, control_water] = scipy.stats.ttest_ind(cBaseVel_2b, eBaseVelW_2b)
[tv, waterend_waterfinal] = scipy.stats.ttest_ind(eBaseW, eBaseVelW_2b)

[tv, control_waterrotateS] = scipy.stats.ttest_ind(cBaseVel_2b, eBaseVelWR_2b)
[tv, waterend_waterfinalR] = scipy.stats.ttest_ind(eBaseWR, eBaseVelWR_2b)

[tv, control_waterrotateD] = scipy.stats.ttest_ind(cBaseVel_2b, eBaseVelWRD_2b)
[tv, waterend_waterfinalD] = scipy.stats.ttest_ind(eBaseWRD, eBaseVelWRD_2b)

print 'Statistics comparing control to new water at end, water end shock to water final, and water to experimental at end different color tanks:', control_waterrotateD, waterend_waterfinalD, waterend_experimentalD 

#fix
#eEndVel25[2]= np.nan

#convert to array
cBV_1a = np.array([np.array([cBaseVel_1a[n]]) for n in range(len(cBaseVel_1a))])
cBV_1b = np.array([np.array([cBaseVel_1b[n]]) for n in range(len(cBaseVel_1b))])

cBV_2a = np.array([np.array([cBaseVel_2a[n]]) for n in range(len(cBaseVel_2a))])
cBV_2b = np.array([np.array([cBaseVel_2b[n]]) for n in range(len(cBaseVel_2b))])

cSV = np.array([np.array([cBase[n]]) for n in range(len(cBase))])

cEV = np.array([np.array([cEndVel[n]]) for n in range(len(cEndVel))])

eBVW_1a = np.array([np.array([eBaseVelW_1a[n]]) for n in range(len(eBaseVelW_1a))])
eBVW_1b = np.array([np.array([eBaseVelW_1b[n]]) for n in range(len(eBaseVelW_1b))])
eBVW_2a = np.array([np.array([eBaseVelW_2a[n]]) for n in range(len(eBaseVelW_2a))])
eBVW_2b = np.array([np.array([eBaseVelW_2b[n]]) for n in range(len(eBaseVelW_2b))])
eSVW = np.array([np.array([eBaseW[n]]) for n in range(len(eBaseW))])
eEVW = np.array([np.array([eEndVelW[n]]) for n in range(len(eEndVelW))])

eBVWR_1a = np.array([np.array([eBaseVelWR_1a[n]]) for n in range(len(eBaseVelWR_1a))])
eBVWR_1b = np.array([np.array([eBaseVelWR_1b[n]]) for n in range(len(eBaseVelWR_1b))])
eBVWR_2a = np.array([np.array([eBaseVelWR_2a[n]]) for n in range(len(eBaseVelWR_2a))])
eBVWR_2b = np.array([np.array([eBaseVelWR_2b[n]]) for n in range(len(eBaseVelWR_2b))])
eSVWR = np.array([np.array([eBaseWR[n]]) for n in range(len(eBaseWR))])
eEVWR = np.array([np.array([eEndVelWR[n]]) for n in range(len(eEndVelWR))])

eBVWRD_1a = np.array([np.array([eBaseVelWRD_1a[n]]) for n in range(len(eBaseVelWRD_1a))])
eBVWRD_1b = np.array([np.array([eBaseVelWRD_1b[n]]) for n in range(len(eBaseVelWRD_1b))])
eBVWRD_2a = np.array([np.array([eBaseVelWRD_2a[n]]) for n in range(len(eBaseVelWRD_2a))])
eBVWRD_2b = np.array([np.array([eBaseVelWRD_2b[n]]) for n in range(len(eBaseVelWRD_2b))])
eSVWRD = np.array([np.array([eBaseWRD[n]]) for n in range(len(eBaseWRD))])
eEVWRD = np.array([np.array([eEndVelWRD[n]]) for n in range(len(eEndVelWRD))])

experimentalwater = np.transpose(np.hstack((eBVW_1a, eBVW_1b, eSVW, eEVW, eBVW_2a, eBVW_2b)))
experimentalwaterrotateSame = np.transpose(np.hstack((eBVWR_1a, eBVWR_1b, eSVWR, eEVWR, eBVWR_2a, eBVWR_2b)))
experimentalwaterrotateDiff = np.transpose(np.hstack((eBVWRD_1a, eBVWRD_1b, eSVWRD, eEVWRD, eBVWRD_2a, eBVWRD_2b)))
control = np.transpose(np.hstack((cBV_1a, cBV_1b, cSV, cEV, cBV_2a, cBV_2b)))


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
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V (new water)')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,3,2)
pylab.plot(experimentalwaterrotateSame)
pylab.plot(0, [eBaseVelWR_1a], 'r.')
pylab.plot(1, [eBaseVelWR_1b], 'r.')
pylab.plot(2,[eBaseWR],'r.')
pylab.plot(3, [eEndVelWR], 'r.')
pylab.plot(4, [eBaseVelWR_2a], 'r.')
pylab.plot(5, [eBaseVelWR_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseVelWR_1a), np.mean(eBaseVelWR_1b), np.mean(eBaseWR), np.mean(eEndVelWR), np.mean(eBaseVelWR_2a), np.mean(eBaseVelWR_2b)],'o-k', lw=3)
yerrWR = (2*scipy.stats.sem(eBaseVelWR_1a), 2*scipy.stats.sem(eBaseVelWR_1b), 2*scipy.stats.sem(eBaseWR), 2*scipy.stats.sem(eEndVelWR), 2*scipy.stats.sem(eBaseVelWR_2a), 2*scipy.stats.sem(eBaseVelWR_2b))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelWR_1a), np.mean(eBaseVelWR_1b), np.mean(eBaseWR), np.mean(eEndVelWR), np.mean(eBaseVelWR_2a), np.mean(eBaseVelWR_2b)],fmt='ok', yerr=yerrWR, lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V (rotated water/same color tanks)')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax = pylab.subplot(1,3,3)
pylab.plot(experimentalwaterrotateDiff)
pylab.plot(0, [eBaseVelWRD_1a], 'r.')
pylab.plot(1, [eBaseVelWRD_1b], 'r.')
pylab.plot(2,[eBaseWRD],'r.')
pylab.plot(3, [eEndVelWRD], 'r.')
pylab.plot(4, [eBaseVelWRD_2a], 'r.')
pylab.plot(5, [eBaseVelWRD_2b], 'r.')
pylab.plot([0,1,2,3,4,5],[np.mean(eBaseVelWRD_1a), np.mean(eBaseVelWRD_1b), np.mean(eBaseWRD), np.mean(eEndVelWRD), np.mean(eBaseVelWRD_2a), np.mean(eBaseVelWRD_2b)],'o-k', lw=3)
yerrWRD = (2*scipy.stats.sem(eBaseVelWRD_1a), 2*scipy.stats.sem(eBaseVelWRD_1b), 2*scipy.stats.sem(eBaseWRD), 2*scipy.stats.sem(eEndVelWRD), 2*scipy.stats.sem(eBaseVelWRD_2a), 2*scipy.stats.sem(eBaseVelWRD_2b))
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelWRD_1a), np.mean(eBaseVelWRD_1b), np.mean(eBaseWRD), np.mean(eEndVelWRD), np.mean(eBaseVelWRD_2a), np.mean(eBaseVelWRD_2b)],fmt='ok', yerr=yerrWRD, lw=3)
ax.set_xticks((0,1,2,3,4,5))
ax.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental fish at 5V (rotated water/diff color tanks)')
patch1 = mpl.patches.Rectangle((1.5,0), 2,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)

pylab.figure()
pylab.suptitle('Summary of Median Velocities (mm/s)')
ax2 = pylab.subplot(1,1,1)
control = ax2.plot([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],'o-k', lw=3, label='Control Fish: Safe = colored')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(cBaseVel_1a), np.mean(cBaseVel_1b), np.mean(cBase), np.mean(cEndVel), np.mean(cBaseVel_2a), np.mean(cBaseVel_2b)],fmt='ok',yerr=yerr, lw=3)
experimentalwater = ax2.plot([0,1,2,3,4,5],[np.mean(eBaseVelW_1a), np.mean(eBaseVelW_1b), np.mean(eBaseW), np.mean(eEndVelW), np.mean(eBaseVelW_2a), np.mean(eBaseVelW_2b)],'o-m', lw=3, label='Experimental Fish (5V): Safe=Shocking with new water')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelW_1a), np.mean(eBaseVelW_1b), np.mean(eBaseW), np.mean(eEndVelW), np.mean(eBaseVelW_2a), np.mean(eBaseVelW_2b)],fmt='om', yerr=yerrW, lw=3)
experimentalwaterrotateSame = ax2.plot([0,1,2,3,4,5],[np.mean(eBaseVelWR_1a), np.mean(eBaseVelWR_1b), np.mean(eBaseWR), np.mean(eEndVelWR), np.mean(eBaseVelWR_2a), np.mean(eBaseVelWR_2b)],'o-c', lw=3, label='Experimental Fish (5V): Safe=Same color tank, different shock water')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelWR_1a), np.mean(eBaseVelWR_1b), np.mean(eBaseWR), np.mean(eEndVelWR), np.mean(eBaseVelWR_2a), np.mean(eBaseVelWR_2b)],fmt='oc', yerr=yerrWR, lw=3)
experimentalwaterrotateDiff = ax2.plot([0,1,2,3,4,5],[np.mean(eBaseVelWRD_1a), np.mean(eBaseVelWRD_1b), np.mean(eBaseWRD), np.mean(eEndVelWRD), np.mean(eBaseVelWRD_2a), np.mean(eBaseVelWRD_2b)],'o-r', lw=3, label='Experimental Fish (5V): Safe=Different color tank, different shock water')
pyplot.errorbar([0,1,2,3,4,5],[np.mean(eBaseVelWRD_1a), np.mean(eBaseVelWRD_1b), np.mean(eBaseWRD), np.mean(eEndVelWRD), np.mean(eBaseVelWRD_2a), np.mean(eBaseVelWRD_2b)],fmt='or', yerr=yerrWRD, lw=3)
handles1, labels1 = ax2.get_legend_handles_labels()
ax2.legend(handles1, labels1)
ax2.set_xticks((0,1,2,3,4,5))
ax2.set_xticklabels(('baseline\n first 15', 'baseline\n second 15', 'baseline\n shock', 'last 5 min\n(shock)', 'baseline\n first 15', 'baseline\n second 15'))
pylab.xlim((-.25,5.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')

pylab.show()

