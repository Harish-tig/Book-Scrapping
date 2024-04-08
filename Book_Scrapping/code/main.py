# project path "C:\HARISH\College\sbl\sbl_project\webscrapping"
# home_url = "https://books.toscrape.com/catalogue/page-{}.html" ------> link

# imports
import requests
import bs4
import re
import pandas as pd
import backend as bk
from colorama import init, Fore, Style
init()

# ignore
pd.set_option('display.width', 250)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# till here

# basic home_url {} for looping #this web page is ment to be scraped
dict_rating = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five'}  # at max 5 star rated book
next_page = 1


# by observation there are only 50 page in web
# search by rating or by name or show all books
# by genre function will allow you to view book by your genre
def scrape(rate=None, all=False, page_by_page=False):
    home_url = "https://books.toscrape.com/catalogue/page-{}.html"
    book_title = []

    global next_page
    if page_by_page and not all:  # if user wants result by pages -----> 1st page then 2nd page so on..
        try:
            res = requests.get(url=home_url.format(next_page))
            soup = bs4.BeautifulSoup(res.text, "lxml")
            Class = soup.select('.product_pod')
            if Class:
                for book in Class:
                    price = str(book.select('div')[1].select('.price_color'))
                    cost = re.search(r'£\d+.\d+', price).group()  # Simplified extraction
                    title = str(book.select('div a')[1]['title'])
                    stock = book.select('div')[1].select('.instock.availability')[0].getText().strip()
                    book_title.append({'Name': title, 'Price': cost, 'Stock': stock})
            df = pd.DataFrame(book_title)
            return df

        except Exception as e:
            print(f"Something went wrong --> {e}")
            exit(2)

    if all and (rate is None):  # if all = True ... iterates whole 50 pages #gives all books from whole site
        try:
            for x in range(1, 51):  # only 50 page in web
                res = requests.get(url=home_url.format(x))  # for first page format(1)
                soup = bs4.BeautifulSoup(res.text, "lxml")
                Class = soup.select('.product_pod')
                for book in Class:
                    price = str(book.select('div')[1].select('.price_color'))
                    cost = re.search(r'£\d+.\d+', price)  # grabbing price.
                    title = str(book.select('div a')[1]['title'])
                    stock = book.select('div')[1]
                    stock = str(stock.select('.instock.availability')[0].getText().strip())
                    book_title.append({'Name': title, 'Price': cost.group(), 'Stock': stock})
            df = pd.DataFrame(book_title)
            return df
        except Exception as e:
            print(f"Something went wrong --> {e}")
            exit(3)

    elif (rate is not None) and not all:  # shows book by user mentioned rating rating
        rating = dict_rating[rate]
        try:
            for page in range(1, 51):
                res = requests.get(url=home_url.format(page))  # for first page format(1)
                soup = bs4.BeautifulSoup(res.text, "lxml")
                Class = soup.select('.product_pod')
                for book in Class:
                    if len(book.select(f'.star-rating.{rating}')) != 0:
                        # if empty page returns empty list #rating selects only passed rating
                        price = str(book.select('div')[1].select('.price_color'))
                        cost = re.search(r'£\d+.\d+', price)
                        title = book.select('div a')[1].getText()
                        stock = book.select('div')[1]
                        stock = str(
                            stock.select('.instock.availability')[0].getText().strip())  # to avoid unnecessary space
                        book_title.append({'Name': title, 'Price': cost.group(), 'Stock': stock})
            df = pd.DataFrame(book_title)
            return df
        except Exception as e:
            print(f"Something went wrong --> {e}")
            exit(4)


def by_genre():
    Flag = 0
    home_url = "https://books.toscrape.com/catalogue/page-{}.html"
    book_title = []
    print(Fore.WHITE)
    genre_list = {
    1: "Travel", 2: "Mystery", 3: "Historical Fiction", 4: "Sequential Art", 5: "Classics", 6: "Philosophy",
    7: "Romance", 8: "Womens Fiction", 9: "Fiction", 10: "Childrens", 11: "Religion", 12: "Nonfiction", 13: "Music",
    14: "Default", 15: "Science Fiction", 16: "Sports and Games", 17: "Add a comment", 18: "Fantasy", 19: "New Adult",
    20: "Young Adult", 21: "Science", 22: "Poetry", 23: "Paranormal", 24: "Art", 25: "Psychology", 26: "Autobiography",
    27: "Parenting", 28: "Adult Fiction", 29: "Humor", 30: "Horror", 31: "History", 32: "Food and Drink",
    33: "Christian Fiction", 34: "Business", 35: "Biography", 36: "Thriller", 37: "Contemporary", 38: "Spirituality",
    39: "Academic", 40: "Self Help", 41: "Historical", 42: "Christian", 43: "Suspense", 44: "Short Stories",
    45: "Novels", 46: "Health", 47: "Politics", 48: "Cultural", 49: "Erotica", 50: "Crime"
    }

    try:
        base = "https://books.toscrape.com/catalogue/"
        for key, value in genre_list.items():
            print(f'{key}:{value}')
        idx = int(input(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\nEnter The Sr. Number of Genre:\n"))  # getting index
        print(Fore.LIGHTCYAN_EX+"This Process Will take Few Seconds Please wait!")
        while idx not in range(1, 51):
            print(Fore.RED + Style.BRIGHT + "INVALID INPUT")
            idx = int(input(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\nEnter The number of Genre:\n"))
        res = requests.get(home_url.format(1))
        soup = bs4.BeautifulSoup(res.text, "lxml")
        secondary_url = soup.select(".nav.nav-list")[0].select('li')[0].select('a')[idx].get('href')
        url = base + secondary_url
        url = url.replace("index.html", "page-{}.html")

        for x in range(1, 10):
            url_res = requests.get(url.format(x))
            soup = bs4.BeautifulSoup(url_res.text, "lxml")
            Class = soup.select('.product_pod')
            if Class:
                Flag = 1
                for book in Class:
                    price = str(book.select('div')[1].select('.price_color'))
                    cost = re.search(r'£\d+.\d+', price)  # grabbing price.
                    title = str(book.select('div a')[1]['title'])
                    stock = book.select('div')[1]
                    stock = str(stock.select('.instock.availability')[0].getText().strip())
                    book_title.append({'Name': title, 'Price': cost.group(), 'Stock': stock})
            else:
                break

        if Flag == 0:
            url = base + secondary_url
            url_res = requests.get(url)
            soup = bs4.BeautifulSoup(url_res.text, "lxml")
            Class = soup.select('.product_pod')
            for book in Class:
                price = str(book.select('div')[1].select('.price_color'))
                cost = re.search(r'£\d+.\d+', price)  # grabbing price.
                title = str(book.select('div a')[1]['title'])
                stock = book.select('div')[1]
                stock = str(stock.select('.instock.availability')[0].getText().strip())
                book_title.append({'Name': title, 'Price': cost.group(), 'Stock': stock})

    except Exception as e:
        print(Fore.RED+Style.BRIGHT+f"something went wrong!, {e}")
    print(Fore.RESET)
    df = pd.DataFrame(book_title)

    loop = True
    while loop:
        choice = int(input(Fore.LIGHTYELLOW_EX + Style.BRIGHT+"\n1] Search Book\n2] Add to wishlist\n3] Show Genre Books\n4] Back: "))
        while choice not in [1, 2, 3, 4]:
            print(Fore.RED+Style.BRIGHT+"INVALID INPUT!")
            choice = int(input(Fore.LIGHTYELLOW_EX + Style.BRIGHT+"\n1] Search Book\n2] Add to wishlist\n3] Show Genre Books\n4] Back: "))
        if choice == 1:
            search(df)
        if choice == 2:
            bk.fav(df, bk.books)
        elif choice == 3:
                if not df.empty:
                        show_book(df)
                else:
                    print(Fore.RED+Style.BRIGHT+"oops! data is empty")
        elif choice == 4:
            print(Fore.RESET+Style.RESET_ALL)
            loop = False


def search(a_dataframe):
    book_search = str(input(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Enter the book you want to search:\n ")).strip()
    for idx, book in enumerate(a_dataframe['Name']):
        if str(book).lower() == book_search.lower():
            price = str(a_dataframe['Price'][idx])
            stock = str(a_dataframe['Stock'][idx])
            print(Fore.BLUE + Style.BRIGHT + f"\n{book}\nPrice = {price}\nStock -> {stock}")
            print(Fore.RESET)
            break
    else:
        print(Fore.RED + "book not found")
        print(Fore.RESET)


def show_book(dataframe):
    print(Fore.WHITE + Style.BRIGHT)
    print(dataframe)
    print(Style.RESET_ALL)


def book_all():  # returns boolean
    df = scrape(all=True)
    print(Fore.BLUE + Style.BRIGHT)
    show_book(df)
    loop = True
    while loop:
        choice = int(input(Fore.LIGHTBLUE_EX + Style.BRIGHT + "1] Search\n2] Add Book to Wishlist\n3] Back:\n "))
        while choice not in [1, 2, 3]:
            print(Fore.RED + "\nInvalid input\n")
            choice = int(input(Fore.LIGHTBLUE_EX + Style.BRIGHT + "1] Search\n2] Add Book to Wishlist\n3] Back:\n "))
        if choice == 1:
            search(df)
        elif choice == 2:
            bk.fav(df, bk.books)
        elif choice == 3:
            print(Style.RESET_ALL)
            break


def pages_by_pages():
    global next_page
    df = scrape(page_by_page=True)
    show_book(df)
    loop = True
    while loop:
        choice = int(
            input(Fore.BLUE + Style.BRIGHT + "\n1] Next page\n2] Previous Page\n3] Add to wishlist\n4] Back:\n "))
        while choice not in [1, 2, 3, 4]:
            print(Fore.RED + "\nInvalid input\n")
            choice = int(
                input(Fore.BLUE + Style.BRIGHT + "\n1] Next page\n2] Previous Page\n3] Add to wishlist\n4] Back:\n "))

        if choice == 1:
            try:
                if next_page >= 50:
                    print(Fore.RED + Style.BRIGHT + "\nNo Next Page available\n")
                else:
                    next_page = next_page + 1
                    df = scrape(page_by_page=True)
                    show_book(df)

            except Exception as e:
                print(Fore.RED + f"\nSorry! Something went wrong probably {e}...Restarting whole process!\n")
                main()
        elif choice == 2:
            if next_page != 1:
                try:
                    next_page = next_page - 1
                    df = scrape(page_by_page=True)
                    show_book(df)
                except Exception as e:
                    print(Fore.RED + f"\nSomething went wrong probably {e}....Restarting whole process!\n")
                    main()
            else:
                print(Fore.RED + "\nNo Previous Page !!!\n")
                print(Fore.LIGHTYELLOW_EX + Style.BRIGHT)
                show_book(df)
                print(Style.RESET_ALL)
        elif choice == 3:
            bk.fav(df, bk.books)
        elif choice == 4:
            print(Style.RESET_ALL)
            next_page = 1
            loop = False


def by_rating():
    print(Fore.GREEN+Style.BRIGHT+"\nEnter book rating in Scale of 1-5\n")
    book_rate = int(input(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Enter book rating:\n "))
    while book_rate not in range(1, 6):
        book_rate = int(input(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Enter book rating:\n "))
    print(Fore.RED + Style.BRIGHT + "\nTHIS PROCESS WILL TAKE UP TO FEW MINUTES.....\nPROCESSING.....")
    df_rating = scrape(rate=book_rate)
    choice = int(input(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Search book or show books?\n1] Search\n2] Show Book:\n"))
    while choice not in [1, 2]:
        print("\nINVALID INPUT\n")
        choice = int(
            input(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\nSearch book or show books?\n1] Search\n2] Show Book:\n"))
    print(Style.RESET_ALL)
    if choice == 1:
        search(df_rating)
    elif choice == 2:
        print(Fore.BLUE + Style.BRIGHT)
        show_book(df_rating)
        loop = True
        while loop:
            choice = int(
                input(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "1] Add Book to Wishlist\n2] Search Book\n3] Back:\n "))
            while choice not in [1, 2,]:
                print(Fore.RED + Style.BRIGHT + "INVALID INPUT")
                choice = int(
                    input(
                        Fore.LIGHTYELLOW_EX + Style.BRIGHT + "1] Add Book to Wishlist\n2] Search Book\n3] Back:\n "))
            if choice == 1:
                bk.fav(df_rating, bk.books)  # using bk.books collection
            elif choice == 3:
                search(df_rating)
            elif choice == 3:
                loop = False


# main logic
# ask user input the way they initialize search
# creating a while loop and a nested while loop
# making flow flexible
def main():
    print(Fore.GREEN + Style.BRIGHT + "Welcome to Web Scraping Project!!")
    while True:
        user_input = int(input(Fore.LIGHTCYAN_EX + Style.BRIGHT +
                               "Search book by?\n1] By Genre\n2] Rating\n3] Show All book\n4] 1st Page\n"
                                "5] Show Wishlist\n6] Remove from Wishlist\n7] Exit: "))
        while user_input not in range(0, 8):
            print(Fore.RED + Style.BRIGHT + "INVALID INPUT")
            user_input = int(input(Fore.LIGHTCYAN_EX + Style.BRIGHT +
                                 "Search book by?\n1] By Genre\n2] Rating\n3] Show All book\n4] 1st Page\n"
                                    "5] Show Wishlist\n6] Remove from Wishlist\n7] Exit: "))
            print(Fore.RESET)
        if user_input == 1:
            by_genre()
        elif user_input == 2:
            loop_2 = True
            while loop_2:
                by_rating()
                choice = int(input(Fore.BLUE + Style.BRIGHT + "1] Start again?\n2] Back:\n "))
                while choice not in [1, 2]:
                    print(Fore.RED + "INVALID INPUT!!!")
                    choice = int(input(Fore.BLUE + Style.BRIGHT + "1] Start again?\n2] Back:\n "))
                if choice == 1:
                    by_rating()
                elif choice == 2:
                    loop_2 = False
        elif user_input == 3:
            print(Fore.RED + Style.BRIGHT + "\nTHIS PROCESS WILL TAKE UP TO FEW MINUTES.....\nPROCESSING.....")
            book_all()
        elif user_input == 4:
            loop_1 = True
            while loop_1:
                pages_by_pages()
                choice = int(input(Fore.WHITE + Style.BRIGHT + "1] iter again?\n2] Back:\n "))
                while choice not in [1, 2]:
                    print(Fore.RED + "\nINVALID INPUT\n")
                    choice = int(input(Fore.WHITE + Style.BRIGHT + "\n1] iter again?\n 2] Back:\n "))
                print(Fore.RESET)
                if choice == 1:
                    pages_by_pages()
                elif choice == 2:
                    loop_1 = False
        elif user_input == 5:
            print(Fore.LIGHTMAGENTA_EX)
            bk.show_collection(bk.books)
            print(Fore.RESET)
        elif user_input == 6:
            bk.delete_fav(bk.books)
        elif user_input == 7:
            print(Fore.GREEN + Style.BRIGHT + "Thank You! Visit The Site again")
            exit(0)


try:
    main()
except Exception as e:
    print("SOMETHING WENT WRONG", e)
