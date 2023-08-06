import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup 
import csv
from selenium.common.exceptions import ElementClickInterceptedException

crxPath = "E:\Schedule Pro Extension\AdBlock — best ad blocker 5.8.0.0.crx"
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)
options.add_extension(crxPath)
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
URL = "https://www.ratemyprofessors.com/search/professors/1079?q=*"
driver.get(URL)
curr = driver.current_window_handle
time.sleep(1)
driver.switch_to.window(curr)
time.sleep(1)
try:
    close = driver.find_element(By.XPATH, '//button[text()="Close"]')
    close.click()
    time.sleep(1)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
except:
    print("could not find the button")
def parseSoure():
    content = driver.page_source
    return content
def clickLoadMore():
    try:
        time.sleep(1)
        loadMoreAfter = driver.find_element(By.XPATH, '//button[text()="Show More"]')
        loadMoreAfter.click()
        return True
    except:
        print("couldn't click load more button")
        return False
scrollAmt = 203
currScroll = 0
count = 0
num = 0
scrapedTeachers = set()
bool = True
data = []
nameSet = set()
csvFile = 'data.csv'
time.sleep(1)
with open(csvFile, 'a', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Name', 'Rating', 'Would Take Again', 'Difficulty'])
    writer.writeheader()
    time.sleep(1)
    while(bool):
        for index in range(8):
            teacher = driver.find_elements(By.CSS_SELECTOR, 'div.CardNumRating__CardNumRatingHeader-sc-17t4b9u-1.fVETNc' )
            time.sleep(0.25)
            del teacher[:count]
            time.sleep(0.5)
            teacherToClick = teacher[0]
            try:
                teacherToClick.click()
                try:
                    time.sleep(2)
                    soup = BeautifulSoup(parseSoure(), 'html.parser')
                    nameElem = soup.select('div.NameTitle__Name-dowf0z-0 span')
                    full_name = ' '.join(span.get_text() for span in nameElem)
                    ratingElem = soup.find('div', class_='RatingValue__Numerator-qw8sqy-2 liyUjw')
                    wouldTakeAgainElem = soup.find_all('div', class_='FeedbackItem__FeedbackNumber-uof32n-1 kkESWs')[0]
                    difficultyElem = soup.find_all('div', class_='FeedbackItem__FeedbackNumber-uof32n-1 kkESWs')[1]
                    rating = ratingElem.text
                    wouldTakeAgain = wouldTakeAgainElem.text
                    difficulty = difficultyElem.text
                    count += 1
                    num += 1
                    print(num)
                    writer.writerow({
                        'Name': full_name,
                        'Rating': rating + "/5",
                        'Would Take Again': wouldTakeAgain,
                        'Difficulty': difficulty
                    })
                    time.sleep(0.5)
                except:
                    print("No write: " + full_name)
                driver.back()
                time.sleep(0.3)
                currScroll += scrollAmt
                driver.execute_script(f"window.scrollTo(0, {currScroll})")
            except ElementClickInterceptedException:
                print("up")
                driver.execute_script(f"window.scrollTo(0, {currScroll - 100})")
        time.sleep(0.5)        
        bool = clickLoadMore()
        time.sleep(1.5)
        currScroll += 75
        driver.execute_script(f"window.scrollTo(0, {currScroll})")
        time.sleep(1)
    print ("Saved")
driver.quit()