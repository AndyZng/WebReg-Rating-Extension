import time
from selenium import webdriver

from bs4 import BeautifulSoup 
import csv
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
URL = "https://cape.ucsd.edu/responses/Results.aspx?Name=&CourseNumber="
driver.get(URL)
time.sleep(25)
def parseSoure():
    content = driver.page_source
    return content
Terms = {"SP23", "WI23", "FA22", "S222", "S122", "SP22", "WI22", "FA21", "S221", "S121", "SP21", "WI21", "FA20"}
csvFile = 'capes_data.csv'
index = 0
with open(csvFile, 'a', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Instructor', 'Term', 'Course', 'RcmndClass', 'RcmndInstr', 'Study Hrs/wk', 'Avg Grade Received'])
    writer.writeheader()
    while(True):
        soup = BeautifulSoup(parseSoure(), 'html.parser')
        rows = soup.find_all('tr', class_=["odd", "even"])
        for row in rows:
            if row.find('td', string=Terms):
                term = row.find('td', string=Terms).text
                print(term)
                if term:
                    instructorName = row.find('td').text.strip()
                    courseName = row.find('a').text.strip()
                    rights = row.find_all('td', attrs={'align': 'right'})
                    rcmndClass = rights[2].find('span').text.strip() 
                    rcmndInstr = rights[3].find('span').text.strip() 
                    studyHrs = rights[4].find('span').text.strip() 
                    avgGrade = rights[6].find('span').text.strip() 
                    writer.writerow({
                            'Instructor': instructorName,
                            'Term': term,
                            'Course': courseName,
                            'RcmndClass': rcmndClass,
                            'RcmndInstr': rcmndInstr,
                            'Study Hrs/wk': studyHrs,
                            'Avg Grade Received': avgGrade
                            })
        print(rows[0])            
        time.sleep(7)
        print("5 sec left")
        time.sleep(5)


