from classes.classMaps import createMaps
from classes.classPostalData import postalCodeData
from classes.classCantonalData import cantonalData
from classes.classFederalData import federalData
from classes.classDBOperations import DBOperations
from scraper.moduleScraperPart1 import scraper1
from scraper.moduleScraperPart2 import scraper2
from functions.babyScraper import babyScraper
import subprocess
import traceback


def userInterface():
    while True:
        print("____________________________________________________\n")
        print("Path: Home\n")
        menu_items = ["[1] Federal", "[2] Cantonal", "[3] Communal", "[4] Compare listing", "[5] Comparis Webscraper", "[99] Exit\n"]
        print("Type in number to navigate")
        print(*menu_items, sep='\n')
        choiceGL = int(input('Choice: '))

        # FEDERAL
        if (choiceGL == 1):
            while True:
                print("____________________________________________________\n")
                print("Path: Home/Federal\n")
                federalObject = federalData(DBOperations("kezenihi_srmidb3"))
                menu_items = ["[0] Go Back", "[1] General Statistics", "[2] Visual Statistics", "[99] Exit\n"]
                print(*menu_items, sep='\n')
                choice = int(input('Choice: '))
                if (choice == 0):
                    break
                elif (choice == 1):
                    print("Preparing General Statistics...")
                    try:
                        federalObject.averageFederal("price", "size")
                    except Exception as e:
                        print("There was an error, please make sure that postal code exists. \n")
                        print(traceback.format_exc())
                        print(e)
                elif (choice == 2):
                    menu_items = ["[0] Go Back", "[1] Histogramm", "[2] Scatter Plot", "[3] Map","[99] Exit\n"]
                    print(*menu_items, sep='\n')
                    choice = int(input('Choice: '))
                    # HISTOGRAMM
                    if (choice == 1):
                        menu_items = ["[1] Price", "[2] Size", "[3] Rooms", "[99] Exit\n"]
                        print(*menu_items, sep='\n')
                        choiceHG = int(input('Choose variable to be plotted: '))
                        choices = ["price", "size", "rooms", "age"]
                        try:
                            federalObject.distribFederal(choices[choiceHG-1])
                        except Exception as e:
                            print("There was an error, please make sure that postal code exists. \n")
                            print(traceback.format_exc())
                            print(e)
                    # SCATTER PLOT
                    if (choice == 2):
                        menu_items = ["[1] Price", "[2] Size", "[3] Rooms", "[99] Exit\n"]
                        print(*menu_items, sep='\n')
                        choiceX = int(input('Choose variable X to be plotted: '))
                        choiceY = int(input('Choose variable Y to be plotted: '))
                        choiceSize = int(input('Choose variable Scatter Size to be plotted: '))
                        choices = ["price", "size", "rooms", "age"]
                        try:
                            federalObject.priceMeterFederal(choices[choiceX-1], choices[choiceY-1], choices[choiceSize-1])
                        except Exception as e:
                            print("There was an error, please make sure that postal code exists. \n")
                            print(traceback.format_exc())
                            print(e)
                    # MAP
                    elif (choice == 3):
                        print("Preparing Visual Map...")
                        try:
                            federalObject.mapAllListingsFederal()
                        except Exception as e:
                            print("There was an error, please make sure that postal code exists. \n")
                            print(traceback.format_exc())
                            print(e)

        # CANTONAL
        if (choiceGL == 2):
            while True:
                print("____________________________________________________\n")
                print("Path: Home/Cantonal\n")
                canton = input("Type in name of canton (in German): ")
                cantonObject = cantonalData(DBOperations("kezenihi_srmidb3"))
                menu_items = ["[0] Go Back", "[1] General Statistics", "[2] Visual Statistics", "[99] Exit\n"]
                print(*menu_items, sep='\n')
                choice = int(input('Choice: '))
                if (choice == 0):
                    break
                elif (choice == 1):
                    print("Preparing General Statistics...")
                    try:
                        cantonObject.averageCanton(canton, "price", "size")
                    except Exception as e:
                        print("There was an error, please make sure that postal code exists.\n")
                        print(e)
                elif (choice == 2):
                    menu_items = ["[0] Go Back", "[1] Histogramm", "[2] Scatter Plot", "[3] Map", "[99] Exit\n"]
                    print(*menu_items, sep='\n')
                    choice = int(input('Choice: '))
                    # HISTOGRAMM
                    if (choice == 1):
                        menu_items = ["[1] Price", "[2] Size", "[3] Rooms", "[99] Exit\n"]
                        print(*menu_items, sep='\n')
                        choiceHG = int(input('Choose variable to be plotted: '))
                        choices = ["price", "size", "rooms", "age"]
                        try:
                            cantonObject.distribCanton(canton, choices[choiceHG-1])
                        except:
                            print("There was an error, please make sure that postal code exists. \n")
                    # SCATTER PLOT
                    if (choice == 2):
                        menu_items = ["[1] Price", "[2] Size", "[3] Rooms", "[99] Exit\n"]
                        print(*menu_items, sep='\n')
                        choiceX = int(input('Choose variable X to be plotted: '))
                        choiceY = int(input('Choose variable Y to be plotted: '))
                        choiceSize = int(input('Choose variable Scatter Size to be plotted: '))
                        choices = ["price", "size", "rooms", "age"]
                        try:
                            cantonObject.priceMeterCanton(canton, choices[choiceX-1], choices[choiceY-1], choices[choiceSize-1])
                        except Exception as e:
                            print("There was an error, please make sure that postal code exists. \n")
                            print(traceback.format_exc())
                            print(e)
                    # MAP
                    elif (choice == 3):
                        print("Preparing Visual Map...")
                        try:
                            cantonObject.mapAllListingsCanton(canton=canton)
                        except Exception as e:
                            print("There was an error, please make sure that postal code exists. \n")
                            print(traceback.format_exc())
                            print(e)

        # COMMUNAL
        if (choiceGL == 3):
            while True:
                print("____________________________________________________\n")
                print("Path: Home/Communal\n")
                postal = int(input("Type in Postal Code: "))
                postalObject = postalCodeData(DBOperations("kezenihi_srmidb3"))
                menu_items = ["[0] Go Back", "[1] General Statistics", "[2] Visual Statistics", "[99] Exit\n"]
                print(*menu_items, sep='\n')
                choice = int(input('Choice: '))
                if (choice == 0):
                    break
                elif (choice == 1):
                    print("Preparing General Statistics...")
                    try:
                        postalObject.average(postal, "price", "size")
                    except:
                        print("There was an error, please make sure that postal code exists.\n")
                elif (choice == 2):
                    menu_items = ["[0] Go Back", "[1] Histogramm", "[2] Scatter Plot", "[3] Weather Data", "[4] Map", "[99] Exit\n"]
                    print(*menu_items, sep='\n')
                    choice = int(input('Choice: '))
                    # HISTOGRAMM
                    if (choice == 1):
                        menu_items = ["[1] Price", "[2] Size", "[3] Rooms", "[99] Exit\n"]
                        print(*menu_items, sep='\n')
                        choiceHG = int(input('Choose variable to be plotted: '))
                        choices = ["price", "size", "rooms", "age"]
                        try:
                            postalObject.distrib(postal, choices[choiceHG-1])
                        except:
                            print("There was an error, please make sure that postal code exists. \n")
                    # SCATTER PLOT
                    if (choice == 2):
                        menu_items = ["[1] Price", "[2] Size", "[3] Rooms", "[99] Exit\n"]
                        print(*menu_items, sep='\n')
                        choiceX = int(input('Choose variable X to be plotted: '))
                        choiceY = int(input('Choose variable Y to be plotted: '))
                        choiceSize = int(input('Choose variable Scatter Size to be plotted: '))
                        choices = ["price", "size", "rooms", "age"]
                        try:
                            postalObject.priceMeter(postal, choices[choiceX-1], choices[choiceY-1], choices[choiceSize-1])
                        except Exception as e:
                            print("There was an error, please make sure that postal code exists. \n")
                            print(e)
                    # WEATHER DATA
                    if (choice == 3):
                        try:
                            postalObject.weather(postal)
                        except:
                            print("There was an error, please make sure that postal code exists. \n")
                    # MAP
                    elif (choice == 4):
                        print("Preparing Visual Map...")
                        try:
                            postalObject.mapAllListingsPostal(postalCode=postal)
                        except:
                            print("There was an error, please make sure that postal code exists. \n")

        # COMPARE LISTING
        if (choiceGL == 4):
            print("____________________________________________________\n")
            print("Path: Home/Compare Listing\n")
            url = input('Enter a comparis Listing URL to compare: ')
            try:
                babyScraper(url)
            except Exception as e:
                print("There was an error, please make sure that postal code exists. \n")
                print(traceback.format_exc())
                print(e)

        # RUN SCRAPER
        if (choiceGL == 5):
            print("____________________________________________________\n")
            print("Path: Home/Comparis Webscraper\n")
            menu_items = ["[0] Go Back", "[1] Scrape New URLS", "[2] Scrape New Listings from URLS", "[99] Exit\n"]
            print(*menu_items, sep='\n')
            choice = int(input('Choice: '))
            if (choice == 0):
                break
            if (choice == 1):
                try:
                    scraper1()
                except Exception as e:
                    print("There was an error")
                    print(e)
            if (choice == 2):
                try:
                    scraper2()
                except Exception as e:
                    print("There was an error")
                    print(e)
