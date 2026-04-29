#Rewrite of code to make it more legible!!!!!
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
Term = None
URL = None
StatusCode = None
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

def GetRequest():
    if StatusCode == 200:
        try:
            

