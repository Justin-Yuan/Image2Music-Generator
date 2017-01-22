import numpy

fi = open('copy.txt', 'wb')

with open('data.txt', 'rb') as fp:
    for x in fp:
        print x
        fi.write(x + '\n')

fi.close()
