# Powered by Etherscan.io APIs
#
# Written by AtLeastSignificant

import json
import sys
import os
import datetime
from urllib.request import urlopen
from decimal import *

class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def clearScreen():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        return
    except:
        print(sys.exc_info())
    return

def loadTokenContracts():
    try:
        with open('token_contracts.json', 'r') as contracts:
            data = json.load(contracts)
        return data
    except:
        print(sys.exc_info())
    return

def initFiles():
    try:
        l = ['app_info.json', 'wallet_addresses.json', 'token_contracts.json']
        for file in l:
            if not os.path.isfile(file):
                f = open(file, 'w')
                if file == 'app_info.json':
                    info = {'API_KEY':'YourApiKey'}
                else:
                    info = {}
                with open(file, 'w') as outfile:
                    json.dump(info, outfile)
        return
    except:
        print(sys.exc_info())
    return
    
def displayKnownTokens():
    try:
        contracts = loadTokenContracts()
        print(bcolors.HEADER + "\nToken database contains " + bcolors.FAIL + str(len(contracts)) + bcolors.HEADER + " contracts:\n" + bcolors.ENDC)
        for contract in contracts:
            print("  " + bcolors.OKGREEN + contract + bcolors.ENDC)
            print("   " + \
            bcolors.FAIL + " Address: " + bcolors.ENDC + str(contracts[contract]['contract_address']) + \
            bcolors.FAIL + " Symbol: " + bcolors.ENDC + str(contracts[contract]['symbol']) + \
            bcolors.FAIL + " Decimals: " + bcolors.ENDC + str(contracts[contract]['decimals']))
        return
    except:
        print(sys.exc_info())
    return        

def addTokenContract():
    try:
        print("\nTo find contract information about tokens, go to" + bcolors.WARNING + " https://etherscan.io/tokens" + bcolors.ENDC)
        address = input("\nNew token contract address: ")
        if address[:2] == "0x" and len(address) == 42:
            contracts = loadTokenContracts()
            for contract in contracts:
                if address == contracts[contract]['contract_address']:
                    print("\n" + bcolors.OKGREEN + contract + bcolors.WARNING + " token already in database:" + bcolors.ENDC)
                    print("  " + str(contracts[contract]))
                    
                    check = input("\nIs this correct? [Y/N]\n\n: ")
                    if check.lower() == 'n' or check.lower() == 'no':
                        name = input("\nNew token name: ")
                        symbol = input("New token symbol: ")
                        decimals = int(input("New token decimals: "))
                        
                        newToken = {}
                        newToken[name] = {'symbol':symbol, 'contract_address':address, 'decimals':decimals}
                        print("\n", newToken)
                        check2 = input("\nIs this correct? [Y/N]\n\n: ")
                        if check2.lower() == 'y' or check2.lower() == 'yes':
                            print(bcolors.WARNING + "\nRemoving old token info..." + bcolors.ENDC)
                            del contracts[contract]
                            print(bcolors.WARNING + "Adding " + bcolors.OKGREEN + name + bcolors.WARNING + " to token database..." + bcolors.ENDC)
                            contracts[name] = {'symbol':symbol, 'contract_address':address, 'decimals':decimals}
                            with open('token_contracts.json', 'w') as outfile:
                                json.dump(contracts, outfile)
                            print(bcolors.OKGREEN + "Done." + bcolors.ENDC)
                            return
                        else:
                            print(bcolors.WARNING + "Leaving token database unchanged." + bcolors.ENDC)
                            return
                    else:
                        print(bcolors.WARNING + "Leaving token database unchanged." + bcolors.ENDC)
                        return
            
            name = input("New token name: ")
            symbol = input("New token symbol: ")
            decimals = input("New token decimals: ")
            
            newToken = {}
            newToken[name] = {'symbol':symbol, 'contract_address':address, 'decimals':decimals}
            print("\n", newToken)
            check2 = input("\nIs this correct? [Y/N]\n\n: ")
            if check2.lower() == 'y' or check2.lower() == 'yes':
                print(bcolors.WARNING + "Adding " + bcolors.OKGREEN + name + bcolors.WARNING + " to token database..." + bcolors.ENDC)
                contracts[name] = {'symbol':symbol, 'contract_address':address, 'decimals':decimals}
                with open('token_contracts.json', 'w') as outfile:
                    json.dump(contracts, outfile)
                print(bcolors.OKGREEN + "Done." + bcolors.ENDC)
                return
            else:
                print(bcolors.WARNING + "Leaving token database unchanged." + bcolors.ENDC)
                return
        else:
            print(bcolors.FAIL + "Incorrect address value.\nAction cancelled." + bcolors.ENDC)
            return
        return
    except:
        print(sys.exc_info())
    return
    
def removeTokenContract():
    try:
        address = input("\nEnter token to remove (symbol/address): ")
        contracts = loadTokenContracts()
        for contract in contracts:
            if (address[:2] == "0x" and len(address) == 42 and address == contracts[contract]['contract_address']) or \
            address == contracts[contract]['symbol']:
                print(bcolors.OKGREEN + "\nContract found:\n  " + bcolors.ENDC + str(contracts[contract]))
                check = input(bcolors.WARNING + "\nRemove " + bcolors.OKGREEN + contract + bcolors.WARNING + " from database? [Y/N]\n\n: " + bcolors.ENDC)
                if check.lower() == 'y' or check.lower() == 'yes':
                    print(bcolors.WARNING + "\nRemoving old token info..." + bcolors.ENDC)
                    del contracts[contract]
                    with open('token_contracts.json', 'w') as outfile:
                        json.dump(contracts, outfile)
                    print(bcolors.OKGREEN + "Done." + bcolors.ENDC)
                    return
                else:
                    print(bcolors.WARNING + "\nLeaving token database unchanged." + bcolors.ENDC)
                    return
        print(bcolors.WARNING + "\nContract not found.\nLeaving token database unchanged." + bcolors.ENDC)
        return
    except:
        print(sys.exc_info())
    return
    
def getDecimalBalance(balance, dec):
    try:
        if len(balance) < dec:
            diff = dec - len(balance)
            for i in range(diff):
                balance = "0" + balance
        ret = balance[:len(balance)-dec] + "." + balance[len(balance)-dec:]
        return Decimal(ret)
    except:
        print(sys.exc_info())
    return
    
def queryTokenBalance(address, contract, decimals, api_key):
    try:
        query = "https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=" \
                + contract + "&address=" + address + "&tag=latest&apikey=" + api_key

        request = urlopen(query)
        response = request.read()
        jsonObj = json.loads(response.decode('utf-8'))
        request.close()
        balance = getDecimalBalance(jsonObj['result'], decimals)
        return balance
    except:
        print(sys.exc_info())
    return

def querySingleAddressBalance(address):
    try:
        with open('app_info.json', 'r') as settings:
            info = json.load(settings)
        api_key = info['API_KEY']
        
        query = "https://api.etherscan.io/api?module=account&action=balance&address=" \
                + address + "&tag=latest&apikey=" + api_key
        
        request = urlopen(query)
        response = request.read()
        jsonObj = json.loads(response.decode('utf-8'))
        request.close()
        balance = getDecimalBalance(jsonObj['result'], 18)
        return balance
    except:
        print(sys.exc_info())
    return

def queryAllAddressBalances():
    try:
        with open('app_info.json', 'r') as settings:
            info = json.load(settings)
        api_key = info['API_KEY']
        
        query = "https://api.etherscan.io/api?module=account&action=balancemulti&address="
        with open('wallet_addresses.json', 'r') as wallet:
            addresses = json.load(wallet)
        for label, address in addresses.items():
            query += (address + ",")
        query = query[:-1]
        query += "&tag=latest&apikey=" + api_key
        
        request = urlopen(query)
        response = request.read()
        jsonObj = json.loads(response.decode('utf-8'))
        request.close()
        
        print(jsonObj)
        return
    except:
        print(sys.exc_info())
    return
    
def getWalletBalances():
    try:
        query = "https://api.coinmarketcap.com/v1/ticker/ethereum/"
        request = urlopen(query)
        response = request.read()
        jsonObj = json.loads(response.decode('utf-8'))
        request.close()
        value = float(jsonObj[0]['price_usd'])
    
        with open('wallet_addresses.json', 'r') as wallet:
            addresses = json.load(wallet)
        for label, address in addresses.items():
            balance = float(querySingleAddressBalance(address))
            print("  " + address + bcolors.FAIL + " :: " + bcolors.OKGREEN + label + bcolors.FAIL + " :: " \
                    + bcolors.ENDC + str(balance) + bcolors.OKGREEN + " ETH" + bcolors.FAIL + " :: " \
                    + bcolors.WARNING + "$" + str(round(value * balance, 2)) + bcolors.ENDC)
    except:
        print(sys.exc_info())
    return

def getTokenBalance():
    try:
        with open('app_info.json', 'r') as settings:
            info = json.load(settings)
        api_key = info['API_KEY']

        addressList1 = []
        addressList2 = []
        with open('wallet_addresses.json', 'r') as wallet:
            addresses = json.load(wallet)
        for label, address in addresses.items():
            addressList1.append((address + bcolors.FAIL + " :: " + bcolors.OKGREEN + label + bcolors.ENDC))
            addressList2.append(address)
        print("")
        count = 1
        for address in addressList1:
            print("  " + bcolors.OKGREEN + str(count) + bcolors.ENDC + ". " + address)
            count += 1
        
        selection = int(input("\nSelect address\n\n: "))
        if selection <= int(len(addressList2)) and selection > 0:
            address = addressList2[selection-1]
            contracts = loadTokenContracts()
            for contract in contracts:
                balance = queryTokenBalance(address, contracts[contract]['contract_address'], int(contracts[contract]['decimals']), api_key)

                print("  " + bcolors.OKGREEN + contract + bcolors.FAIL + " :: " + bcolors.ENDC + str(balance) + bcolors.OKGREEN \
                        + " " + contracts[contract]['symbol'] + bcolors.ENDC)
        else:
            print(bcolors.WARNING + "\nInvalid selection." + bcolors.ENDC)
            return
    except:
        print(sys.exc_info())
    return

def snapshot():
    try:
        query = "https://api.coinmarketcap.com/v1/ticker/ethereum/"
        request = urlopen(query)
        response = request.read()
        jsonObj = json.loads(response.decode('utf-8'))
        request.close()
        value = float(jsonObj[0]['price_usd'])
        
        filename = datetime.datetime.now().strftime("%m-%d-%Y %I-%M-%S%p") + ".txt"
        if not os.path.isdir("snapshots"):
            os.mkdir("snapshots")
            
        snapshot = open("snapshots/" + filename, "w")
        snapshot.write("Balance snapshot for " + datetime.datetime.now().strftime("%m-%d-%Y %I:%M:%S%p") + "\n\n")
        with open('wallet_addresses.json', 'r') as wallet:
            addresses = json.load(wallet)
        for label, address in addresses.items():
            balance = float(querySingleAddressBalance(address))
            snapshot.write(address + " :: " + label + " :: " + str(balance) + " ETH" + " :: $" + str(round(value * balance, 2)) + "\n")
        snapshot.close()
        print(bcolors.OKGREEN + "Done." + bcolors.ENDC)
    except:
        print(sys.exc_info())
    return
    
def getAllWalletBalances():
    try:
        queryAllAddressBalances()
    except:
        print(sys.exc_info())
    return
    
def getWalletAddresses():
    try:
        with open('wallet_addresses.json', 'r') as wallet:
            addresses = json.load(wallet)
        for label, address in addresses.items():
            print("  " + address + bcolors.FAIL + " :: " + bcolors.OKGREEN + label + bcolors.ENDC)
        return
    except:
        print(sys.exc_info())
    return
    
def addNewWalletAddress():
    try:
        address = input("\nEnter public address (starts with \'0x\')\n\n: ")
        if address[:2] == "0x" and len(address) == 42:
            label = input("\nEnter a name for this address\n\n: ")
            addToWallet = input("\nAdd \"" + label + "\": " + address + " to wallet? [Y/N]\n\n: ")
            if addToWallet.lower() == 'y' or addToWallet.lower() == 'yes':
                with open('wallet_addresses.json', 'r') as wallet:
                    addresses = json.load(wallet)
                addresses[label] = address
                with open('wallet_addresses.json', 'w') as newWallet:
                    json.dump(addresses, newWallet)
            
                print(bcolors.OKGREEN + "Done." + bcolors.ENDC)
            else:
                print(bcolors.FAIL + "Action cancelled." + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "Incorrect address value.\nAction cancelled." + bcolors.ENDC)
        return
    except:
        print(sys.exc_info())
    return
    
def removeWalletAddress():
    try:
        with open('wallet_addresses.json', 'r') as wallet:
            addresses = json.load(wallet)
        notDone = True
        
        while notDone:
            name = input("\nEnter name of address to remove\n\n: ")
            if name in addresses.keys():
                check = input("\nDelete \'" + name + "\' from wallet? [Y/N]\n\n: ")
                if check.lower() == 'y' or check.lower() == 'yes':
                    del addresses[name]
                    with open('wallet_addresses.json', 'w') as newWallet:
                        json.dump(addresses, newWallet)
                        print(bcolors.OKGREEN + "Done." + bcolors.ENDC)
                        notDone = False
                else:
                    print(bcolors.FAIL + "Action cancelled." + bcolors.ENDC)
                    notDone = False
            else:
                print(bcolors.WARNING + "\n\'" + name + "\' not found." + bcolors.ENDC)
                tryAgain = input("Try another? [Y/N]\n\n: ")
                if tryAgain.lower() == 'n' or tryAgain.lower() == 'no':
                    notDone = False
                    clearScreen()
                    printMenu()
                else:
                    notDone = True
        return
    except:
        print(sys.exc_info())
    return
    
def changeApiKey():
    try:
        with open('app_info.json', 'r') as settings:
            info = json.load(settings)
        key = info['API_KEY']
        print("  Current API key: \'" + bcolors.OKGREEN + key + bcolors.ENDC + "\'")
        print("\n  Visit https://etherscan.io/myapikey to generate a new one.\n")
        change = input(bcolors.WARNING + "1 - Change API key" + bcolors.ENDC + "\n\n: ")
        if change.lower() == '1':
            newKey = input("\nEnter new API key\n\n: ")
            print("\nNew API key: \'" + bcolors.WARNING + newKey + bcolors.ENDC + "\'")
            check = input("Is this correct? [Y/N]\n\n: ")
            if check.lower() == 'y' or check.lower() == 'yes':
                info['API_KEY'] = newKey
                with open('app_info.json', 'w') as outfile:
                    json.dump(info, outfile)
                print(bcolors.OKGREEN + "Done." + bcolors.ENDC)
            else:
                print(bcolors.FAIL + "Action cancelled." + bcolors.ENDC)
        else:
            clearScreen()
            printMenu()
        return
    except:
        print(sys.exc_info())
    return
    
def printMenu():
    menu = bcolors.HEADER + "\nCommands:" + bcolors.ENDC + "\n\n\
    1 - " + bcolors.OKGREEN + "Check balances\n" + bcolors.ENDC + "\
    2 - " + bcolors.OKGREEN + "View wallet info\n" + bcolors.ENDC + "\
    3 - " + bcolors.OKGREEN + "View tracked ERC20 tokens\n" + bcolors.ENDC + "\
    4 - " + bcolors.OKGREEN + "Change API key" + bcolors.FAIL + "\n\
    Exit" + bcolors.ENDC + " - close the application"
    print(menu)
    return
    
def printHelp():
    print(bcolors.OKGREEN + "\nThank you for using " + bcolors.FAIL + "AlertEth" + bcolors.OKGREEN + " by " + bcolors.HEADER + \
        "/u/AtLeastSignificant" + bcolors.OKGREEN + " | " + bcolors.HEADER + "@Tomshwom" + bcolors.OKGREEN + " on Steemit" + \
        ".\n\nPlease send feedback and any bug reports to me via Reddit private message." + \
        "\n\nIf you want to contribute to the development of this app or my other work, consider donating to " + \
        bcolors.HEADER + "AtLeastSignificant.eth" + bcolors.OKGREEN + "." + \
        "\n\nThis app is powered by " + bcolors.WARNING + "Etherscan.io" + bcolors.OKGREEN +  " APIs." + bcolors.ENDC)
    
    help = bcolors.HEADER + "\nCommands info:" + bcolors.ENDC + "\n\n\
    1 - " + bcolors.OKGREEN + "Check balances" + bcolors.FAIL + " :: " + bcolors.ENDC + "view current Ether and token balances on all addresses in your wallet\n\
    2 - " + bcolors.OKGREEN + "View wallet info" + bcolors.FAIL + " :: " + bcolors.ENDC + "view/add/remove addresses from your wallet\n\
    3 - " + bcolors.OKGREEN + "View tracked ERC20 tokens" + bcolors.FAIL + " :: " + bcolors.ENDC + "view/add/remove token contracts that are used when finding wallet balances\n\
    4 - " + bcolors.OKGREEN + "Change API key" + bcolors.FAIL + " :: " + bcolors.ENDC + "view/change Etherscan API key" + bcolors.FAIL + "\n\
    Exit" + bcolors.ENDC + " - close the application"
    print(help)
    return