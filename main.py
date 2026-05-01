#add error handeling AKA what if no page tag are found, what if somethign is empty etc
#use PyScript to connect it to html


from bs4 import BeautifulSoup
import requests
#regular expresions
#^ pattern will start at the begginig of the string
#^[A-Z]+$ will look for pattern that styarts with capital and ends with capital, has to occure once but may occure more
import re


user_input = input("What item are you looking for today?: ")

#re.compile only makes the pattern to see, not extract


words = re.findall(r'\w+', user_input)
term = '+'.join(words)
print(term)



#sets url to book site, sends get request and retireves the html
url = "https://www.newegg.com/p/pl?d=" + term
request = requests.get(url).text
doc = BeautifulSoup(request, "html.parser")

#----------------------
pages_list = []

#Finds Pages
def FindPages():
    #finds the class that hold sthe strong tag thats hold the page number
    find_page = doc.find_all(class_="list-tool-pagination-text")
    pages = list(find_page[0].descendants)


    for page in  pages:
        #Checks if it is a string in pages and if it is a digit
        if isinstance(page, str)and page.isdigit():
            #appends digit to page lisat as an ijnteger
            pages_list.append(int(page))


    return pages_list

FindPages()
#Stes current and total pages
CurrentPage = pages_list[0]
TotalPages = pages_list[1]

#------------------------

print(f"Current Page Your are On: {CurrentPage}  Total Amount of Pages: {TotalPages}")

#Sets a new url with the current page
NEWurl = url + '&page=' + str(CurrentPage)

#Sends another get request to the new url
request2 = requests.get(NEWurl).text
doc2 = BeautifulSoup(request2, "html.parser")

#--- FINDING LINK OF ALL PRODUCTS + NAME + CASH ---
#Finds all links

LinksList = []
ProductsList = []
Priceslist = []

SortedList = []

all_links = doc2.find_all(class_="item-title", title="View Details")


for  linktag in all_links:
    #looks for attribute href, makes list with link (inside href attribute)
    links = linktag['href']
    LinksList.append(links)





all_products = doc2.find_all(class_="item-title", title="View Details")



for producttag in all_products:
    products = producttag.get_text()
    ProductsList.append(products)



#Since li holds strong tag, we waqnt to extarct strong out of there
all_strong = []


all_pricesPARENT = (doc2.find_all(class_="price-current"))

#for all the li tags in the list extracted, we extract the strong tag within it and put it in another list.
for parent in all_pricesPARENT:
    strong_tag = parent.find('strong')
    if strong_tag:
        #appends all stronmg tags to news list
        all_strong.append(strong_tag)

#gets only the text from the strong tag
#REMINDER FOR FUTURE: any tag "<strong>" is NOT treated as text as it is converted back into html before retrieving only the text, makming it back into a tag
RawStrong = []
for strongtag in all_strong:
    RawStrong.append(strongtag.get_text())
    for strong in RawStrong:
        strong = strong.replace(',', '')
        Priceslist.append(int(strong))


# for every link ther eit, it will append the link, product, and price in a list within another list
for x in range(len(LinksList)):
    SortedList.append([LinksList[x], ProductsList[x], Priceslist[x]])


#sorts second index of sorted list
#key = is a sort basis, Ex: if key = len, it would sort by length
#lambda is an anonymous function, value is automatically returned at the end
SortedList.sort(key=lambda x: x[2])


print(SortedList)
print("hello world!")








