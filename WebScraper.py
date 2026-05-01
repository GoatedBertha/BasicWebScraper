#Rewrite of code to make it more legible!!!!!, need to make error handeling a bit better though.
#PRCIES DO NOT WORK, seems like its grabbing the wrong price AND it grabs multiple prices
from bs4 import BeautifulSoup
import requests
import re

#--------
#LISTS NEEDED

LinksList = []
ProductsList = []
Priceslist = []
SortedList = []
PriceSortedList = []
pages_list = []


#---------


UserInput = None
URL = None
StatusCode = None
Doc = None
ProcessFailed = None
ReasonCodeBroke = None
CodeBroke = False



CurrentPage = 1
TotalPages = 0
BaseURL = "https://www.newegg.com/"


#----------
#Functions + Code

#Combines all aspects of a normal url to make the url we want, while checking for errors
def MakeURL(BaseURL, Term, CurrentPage):
    #Makes the URL

    URL = BaseURL + "/p/pl?d=" + Term + "&page=" + str(CurrentPage)
    #Returns the status code from it, times out after 10 seconds
    Response = requests.get(URL, timeout=10) 
    StatusCode = Response.status_code
    return URL, StatusCode

#Asks for the get request, if it doesnt return 200 (200 = site working) prints error instead of crashing
def GetRequest(URL, StatusCode):
    if StatusCode == 200:
        try:
            request = requests.get(URL).text
            Doc = BeautifulSoup(request, "html.parser")
            return Doc, None, None 
        except:
            #It saves the reason why the code broke
            ReasonCodeBroke = "Could not get HTML!"
            #Stops next code if it cant fetch original document
            CodeBroke = True
            #Stops 
            return None, CodeBroke, ReasonCodeBroke
    else:
        #It saves the reason why the code broke
        ReasonCodeBroke = "Could not reach website!"
        #Stops next code if it cant fetch original document
        CodeBroke = True

        return None, CodeBroke, ReasonCodeBroke

#Finds the pages for the current website it is on
def FindPages(Doc, CodeBroke):
    if not CodeBroke:
        try:
            #finds the class that hold sthe strong tag thats hold the page number
            find_page = Doc.find_all(class_="list-tool-pagination-text")
            pages = list(find_page[0].descendants)


            for page in  pages:
                #Checks if it is a string in pages and if it is a digit
                if isinstance(page, str)and page.isdigit():
                    #appends digit to page lisat as an integer
                    pages_list.append(int(page))
                    CurrentPage = pages_list[0]
                    TotalPages = pages_list[1]


            return CurrentPage, TotalPages, None, None
        except:
            #It saves the reason why the code broke
            ReasonCodeBroke = "Could not find pages!"
            #Stops next code if it cant fetch original document
            CodeBroke = True
            return None, None, CodeBroke, ReasonCodeBroke
    else:
        ReasonCodeBroke = "Did not execute, code is broken earlier!"
        CodeBroke = True
        return None, None, CodeBroke, ReasonCodeBroke


def FindData(Doc, CodeBroke):
    if not CodeBroke:

            #Claude solution, works but where did it get "item-cell"?????
            # all_items = Doc.find_all(class_="item-cell")  # each product's wrapper div

            # for item in all_items:
            #     # grab link, product, and price all from the same container
            #     link_tag = item.find(class_="item-title")
            #     price_tag = item.find(class_="price-current")

            #     if link_tag and price_tag:
            #         strong_tag = price_tag.find("strong")
            #         if strong_tag:
            #             price = int(strong_tag.get_text().replace(",", ""))
            #             LinksList.append(link_tag["href"])
            #             ProductsList.append(link_tag.get_text())
            #             Priceslist.append(price)



            #prices broken, will try to recode later on


        #sorts second index of sorted list
        #key = is a sort basis, Ex: if key = len, it would sort by length
        #lambda is an anonymous function, value is automatically returned at the end
        PriceSortedList = sorted(SortedList, key=lambda x: x[2])

        return LinksList, ProductsList, Priceslist, SortedList, PriceSortedList, None, None
    else:
        ReasonCodeBroke = "Did not execute, code is broken earlier!"
        CodeBroke = True
        return None, None, None, None, None, CodeBroke, ReasonCodeBroke



#TEST
UserInput = input("What would you like to search for today?: ")

words = re.findall(r'\w+', UserInput)
Term = '+'.join(words)


URL, StatusCode = MakeURL(BaseURL, Term, CurrentPage)

Doc, CodeBroke, ReasonCodeBroke = GetRequest(URL, StatusCode)

LinksList, ProductsList, Priceslist, SortedList, PriceSortedList, CodeBroke, ReasonCodeBroke = FindData(Doc, CodeBroke)

# print(len(LinksList))
# print(len(ProductsList))
# print(len(Priceslist))



# print(SortedList)
# print()
# print()
# print()
# print(PriceSortedList)