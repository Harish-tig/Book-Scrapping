import pymongo as pm
import datetime
from colorama import init, Fore, Style
init()

client = pm.MongoClient('mongodb://localhost:27017') # running on local host
db = client.get_database('mydatabase')               # gets if exists else creates a new one.
books = db.get_collection('books')                   # gets if exists else creates a new one.

#add book to fav #UPDATE
def fav(df, collection): #a data_frame and a collection
    try:
        idx = int(input('Enter Sr. Number of Book: '))
        fav_book = df.iloc[idx].to_dict()
        fav_book['Date']= str(datetime.date.today())
        collection.insert_one(fav_book)
        print(Fore.GREEN + Style.BRIGHT + "\nBook Added to Wishlist Successfully\n")
    except Exception as e:
        print(Fore.RED + f"\nCouldn't Add, {e}\n")


#Show added books #READ
def show_collection(a_collection):
    print(Fore.RED + "\nStart of the List")
    print(Fore.WHITE)
    for book in a_collection.find({},{'_id': 0,'Stock':0}):
        print(book)

    print(Fore.RED + Style.BRIGHT+"\nEND of the List\n")
    print(Fore.RESET)

#REMOVE BOOK FROM FAVORITES #DELETE
def delete_fav(collection):
    show_collection(collection)
    Book = str(input(Fore.RED + Style.BRIGHT+ "Enter the Name book you want to Remove:\n "))
    check = collection.find_one_and_delete({"Name": Book})
    if check:
        print(Fore.RED+ "\nBook Removed from Wishlist\n")
    else:
        print(Fore.RED + Style.BRIGHT+ "Coudnt find book!Try to enter exact name of the book")
        delete_fav(collection)