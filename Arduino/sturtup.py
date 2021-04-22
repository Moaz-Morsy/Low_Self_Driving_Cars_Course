from os.path import expanduser
import datetime

file = open(expanduser("~")+'/Desktop/Here.txt','w')


file.write("It worked !! \n" + str(datetime.datetime.now()))


file.close()
