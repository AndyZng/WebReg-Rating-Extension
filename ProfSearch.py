import csv
from bs4 import BeautifulSoup 
from googlesearch import search
import requests
import time
numSuccess = 0
def getInfo(name):
    global numSuccess
    print (name)
    name = name
    query = name + " rate my professor University of California San Diego"
    result = search(query, tld="com", num=1, stop=1, pause = 0.5)
    time.sleep(0.8)
    try:
        urlResult = next(result)
    except:
        print("fail")
        writer.writerow({
                    'Instructor': name,
                    'Rating': "FAILED SEARCH",
                    'Would Take Again': "FAILED SEARCH",
                    'Difficulty': "FAILED SEARCH"
                })
        return False
    if "ratemyprofessors" in urlResult:
        pageContent = requests.get(urlResult)
        time.sleep(1.75)
        soup = BeautifulSoup(pageContent.content, 'html.parser')
        try:
            ratingElem = soup.find('div', class_='RatingValue__Numerator-qw8sqy-2 liyUjw')
            wouldTakeAgainElem = soup.find_all('div', class_='FeedbackItem__FeedbackNumber-uof32n-1 kkESWs')[0]
            difficultyElem = soup.find_all('div', class_='FeedbackItem__FeedbackNumber-uof32n-1 kkESWs')[1]
            rating = ratingElem.text.strip()
            wouldTakeAgain = wouldTakeAgainElem.text.strip()
            difficulty = difficultyElem.text.strip()
            try: 
                tags = []
                tagContainer = soup.find('div', class_='TeacherTags__TagsContainer-sc-16vmh1y-0 dbxJaW')
                tagElems = tagContainer.find_all('span', class_='Tag-bs9vf4-0 hHOVKF')
                for tagElem in tagElems:
                    tags.append(tagElem.text.strip())
                writer.writerow({
                    'Instructor': name,
                    'Rating': rating + "/5",
                    'Would Take Again': wouldTakeAgain,
                    'Difficulty': difficulty,
                    'Tags': ', '.join(tags)
                })
                numSuccess += 1 
            except:
                    writer.writerow({
                            'Instructor': name,
                            'Rating': rating+ "/5",
                            'Would Take Again': wouldTakeAgain,
                            'Difficulty': difficulty,
                            'Tags': "None"
                        })
                    numSuccess += 1 
        except:
                writer.writerow({
                            'Instructor': name,
                            'Rating': "N/A",
                            'Would Take Again': "N/A",
                            'Difficulty': "N/A"
                        })
        return True
    else:
        print("fail")
        return False

instructorSet = set()
with open("capes_data.csv", "r", newline="", encoding='utf-8') as file:
    csvreader = csv.DictReader(file)
    for col in csvreader:
        instructorName = col['Instructor']
        instructorName = instructorName.split(',')
        length = len(instructorName)
        profName = instructorName[length - 1] + " " + instructorName[length - 2]
        profName = profName.strip()
        instructorSet.add(profName)
    print(instructorSet)

""" with open("rmp_data.csv", 'a') as file:
    writer = csv.DictWriter(file, fieldnames=['Instructor', 'Rating', 'Would Take Again', 'Difficulty', 'Tags'])
    writer.writeheader()
    for prof in instructorSet:
        otherName = prof
        otherName = otherName.split()
        length = len(otherName)
        if not getInfo(prof) and length > 2: 
            otherName = otherName[0] + " " + otherName[length-1]
            if not getInfo(otherName):
                prof = prof.split()
                prof = prof[0] + " " + prof[1]
                getInfo(prof)
                writer.writerow({
                        'Instructor': "CHECK INFO",
                        'Rating': "CHECK INFO",
                        'Would Take Again': "CHECK INFO",
                        'Difficulty': "CHECK INFO"
                    })
        print (numSuccess)
 """