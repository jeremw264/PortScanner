from model.Scanner import Scanner
import sys

if len(sys.argv) == 2:
    scanner = Scanner(15,sys.argv[1],65000)
    scanner.displayDescription()
    scanner.scanner()
    print('\nFinish no work more...')


else:
    print('Invalid argument')






    
    