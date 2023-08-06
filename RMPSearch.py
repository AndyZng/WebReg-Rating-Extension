import csv
csvFile = 'data.csv'
from bs4 import BeautifulSoup 
from googlesearch import search
import requests
csvFile = 'data.csv'
def getInfo():
    global resp
    name = input("Name: ")    
    query = name + " rate my professor University of California San Diego"
    result = search(query, tld="com", num=1, stop=1, pause = 0.5)
    urlResult = next(result)
    print (query)
    print (urlResult)
    #make sure that url is a rmp url
    if "ratemyprofessors" in urlResult:
        pageContent = requests.get(urlResult)
        soup = BeautifulSoup(pageContent.content, 'html.parser')
        ratingElem = soup.find('div', class_='RatingValue__Numerator-qw8sqy-2 liyUjw')
        wouldTakeAgainElem = soup.find_all('div', class_='FeedbackItem__FeedbackNumber-uof32n-1 kkESWs')[0]
        difficultyElem = soup.find_all('div', class_='FeedbackItem__FeedbackNumber-uof32n-1 kkESWs')[1]
        rating = ratingElem.text
        wouldTakeAgain = wouldTakeAgainElem.text
        difficulty = difficultyElem.text
        print ("Rating " + rating + "/5")
        print ("Percent would take again " + wouldTakeAgain)
        print ("Difficulty " + difficulty +"/5")
        output = ({
                    'Name': name,
                    'Rating': rating + "/5",
                    'Would Take Again': wouldTakeAgain,
                    'Difficulty': difficulty
                })
        print(1)
    else:
        rating = "No rating found"
        wouldTakeAgain = "n/a"
        difficulty = "n/a"
        resp = {'rating': rating, 'wouldTakeAgain': wouldTakeAgain, 'difficulty': difficulty}
        print(2)
        print ("resp: ")
        print (resp) 
    print(3)    
    if __name__ == "__main__":
        app.run(host='127.0.0.1', port=5000)
    