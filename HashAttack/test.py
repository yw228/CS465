import time
from hash import Hash

for i in range(1 ,25):
    print('*********************************************************************')
    print(str(i) + " bits")
    startTime = time.time()

    HashTest = Hash('cs465_Project2', i)
    HashTest.startAttacks()
    print('=========================================================')
    endTime = time.time()
    print('Run time (IN SECOND) : ' + str(endTime - startTime))
    print('*********************************************************************')
    print('\n\n')

