# Powered by Etherscan.io APIs
#
# Written by AtLeastSignificant | @Tomshwom on Steemit

from functions import *

def main():
    clearScreen()
    printMenu()
    
    while True:
        command = input("\n: ")
        
        if command.lower() == "help" or command.lower() == "commands":
            clearScreen()
            printHelp()
        
        elif command.lower() == "1":
            clearScreen()
            print(bcolors.HEADER + "\nBalances:\n" + bcolors.ENDC)
            getWalletBalances()
            response = input("\n" + bcolors.WARNING + "1 - Check token balance\t\t2 - Create snapshot" + bcolors.ENDC + "\n\n: ")
            
            if response.lower() == "1":
                getTokenBalance()
            elif response.lower() == "2":
                print(bcolors.WARNING + "Saving..." + bcolors.ENDC)
                snapshot()
            else:
                clearScreen()
                printMenu()

        elif command.lower() == "2":
            clearScreen()
            print(bcolors.HEADER + "\nStored addresses:\n" + bcolors.ENDC)
            getWalletAddresses()
            response = input("\n" + bcolors.WARNING + "1 - Add address\t\t2 - Remove address" + bcolors.ENDC + "\n\n: ")
            
            if response.lower() == "1":
                addNewWalletAddress() 
            elif response.lower() == "2":
                removeWalletAddress()
            else:
                clearScreen()
                printMenu()
                
        elif command.lower() == "3":
            clearScreen()
            displayKnownTokens()
            response = input("\n" + bcolors.WARNING + "1 - Add contract\t2 - Remove contract" + bcolors.ENDC + "\n\n: ")
            
            if response.lower() == "1":
                addTokenContract() 
            elif response.lower() == "2":
                removeTokenContract()
            else:
                clearScreen()
                printMenu()
        
        elif command.lower() == "4":
            clearScreen()
            print(bcolors.HEADER + "\nAPI-Key info:\n" + bcolors.ENDC)
            changeApiKey()
        
        elif command.lower()== "exit" or command.lower() == "close":
            print("\n" + bcolors.WARNING + "Exiting..." + bcolors.ENDC)
            exit()
            
        else:
            clearScreen()
            print("\nType 'help' to see command details and more info.")
            printMenu()

if __name__ == "__main__":
    try:
        initFiles()
        main()
    except KeyboardInterrupt:
        print("\n" + bcolors.WARNING + "Exiting..." + bcolors.ENDC)
        exit()