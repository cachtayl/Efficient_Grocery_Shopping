import json
import os.path
from typing import OrderedDict
from unicodedata import category

def main():
    # if json db does not exist create one
    if os.path.exists('stores.json') == False: 
        file = open("stores.json", "w")
        file.write('[]')
        file.close()
    
    options = input("Welcome to the Main Menu!\nPress 0 if you want to create an efficient grocery list\nPress 1 if you want to register a store\n")
    if(options == '0'):
        makeList()
    else:
        registerStore()
        
def registerStore():
    store_name = input("Enter the name of the store: ")
    new_store = {"store_name": store_name}
   
    print("Great! Now please enter all of the aisle names and the corresponding row number")

    file = open("stores.json", "r")
    content = file.read()
    stores = json.loads(content)
    
    aisle_name = ''
    while(True):
        aisle_name = input("Aisle name: ")
        if(aisle_name == "Done"):
            break
        number = input("Aisle number: ")
        new_store[number] = aisle_name
    print(new_store)

    stores.append(new_store)
    
    json_obj = json.dumps(stores, indent=4)

    file = open("stores.json", "w")
    file.write(json_obj)

    file.close()

def makeList():
    file = open("stores.json", "r")

    content = file.read()
    stores = json.loads(content)
    print("\nRegistered Stores")
    for idx,store in enumerate(stores):
        print(idx , ":" , store['store_name'])
    choice = input("Please select the store you are going to: ")

    store = stores[int(choice)]
    
    print(store['store_name'] + " has aisles: ")
    aisles = ""
    for aisle in sorted(store.keys()):
        num = store[aisle]
        if(aisle != "store_name"):
            aisles += "\n"+ aisle + ": "+ num
    print(aisles)
    print("Now enter your future items and their matching aisle number")
    print("Enter 'Done' when you are finished")
    shopping_list = {}
    while(True):
        item_name = input("Item name: ")
        if(item_name == "Done"):
            break
        number = input("Associated aisle: ")
        if number in shopping_list:
            shopping_list[number].append(item_name)
        else:
            shopping_list[number] = [item_name]
    
    orderedList = "Shopping with efficiency!\n"
    for row in sorted(shopping_list.keys()):
        for item in shopping_list[row]:
            orderedList += item + "\n"

    file_name = input("Name your file: ") + ".txt"
    file = open(file_name, "w")
    file.write(orderedList)
    file.close()
if __name__ == "__main__":
    main()




