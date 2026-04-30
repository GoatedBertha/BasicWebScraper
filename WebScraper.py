#Rewrite of code to make it more legible!!!!!, need to make error handeling a bit better though.
from bs4 import BeautifulSoup
import requests
import re

#--------
#LISTS NEEDED

LinksList = []
ProductsList = []
Priceslist = []
SortedList = []



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
    URL = BaseURL + "/p/pl?d=" + Term + "&page=" + CurrentPage
    #Returns the status code from it
    Response = requests.get(URL)
    StatusCode = Response.status_code
    return URL, StatusCode

#Asks for the get request, if it doesnt return 200 (200 = site working) prints error instead of crashing
def GetRequest(URL, StatusCode):
    if StatusCode == 200:
        try:
            request = requests.get(URL).text
            Doc = BeautifulSoup(request, "html.parser")
            return Doc 
        except:
            #It saves the reason why the code broke
            ReasonCodeBroke = "Could not get HTML!"
            #Stops next code if it cant fetch original document
            CodeBroke = True
            #Stops 
            return CodeBroke, ReasonCodeBroke
    else:
        #It saves the reason why the code broke
        ReasonCodeBroke = "Could not reach website!"
        #Stops next code if it cant fetch original document
        CodeBroke = True

        return CodeBroke, ReasonCodeBroke

#Finds the pages for the current website it is on
def FindPages(Doc, CodeBroke):
    if CodeBroke == False:
        try:
            #finds the class that hold sthe strong tag thats hold the page number
            find_page = Doc.find_all(class_="list-tool-pagination-text")
            pages = list(find_page[0].descendants)


            for page in  pages:
                #Checks if it is a string in pages and if it is a digit
                if isinstance(page, str)and page.isdigit():
                    #appends digit to page lisat as an integer
                    pages_list = []
                    pages_list.append(int(page))
                    CurrentPage = pages_list[0]
                    TotalPages = pages_list[1]


            return CurrentPage, TotalPages
        except:
            #It saves the reason why the code broke
            ReasonCodeBroke = "Could not find pages!"
            #Stops next code if it cant fetch original document
            CodeBroke = True
            return CodeBroke, ReasonCodeBroke
    else:
        ReasonCodeBroke = "Did not execute, code is broken earlier!"
        CodeBroke = True
        return CodeBroke, ReasonCodeBroke




