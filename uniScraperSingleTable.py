#NOTE: Must have beautiful soup installed

import csv
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs


UA_ROOT_URL = 'https://catalogue.ualberta.ca'

#First crawl the course faculty page and gather the faculty link as well as the faculty name for each given
#faculty
courseFacultyPage = urlopen(UA_ROOT_URL+'/Course')
time.sleep(2)
courseFacultySoup = bs(courseFacultyPage, 'html.parser')
facultyTable = courseFacultySoup.find('table',{'class':'pure-table pure-table-striped'})
faculties = facultyTable.findAll('td')

facultyLinks = {}
for faculty in faculties:
    facultyLinks[faculty.find('a').contents[0]] = faculty.find('a').get('href')
#print(facultyLinks)



subjectLinks = {}
subjectNamePairs = {}

with open('UAlbertaCoursesSingleTable.csv','w',newline='') as csvfile:
    #Create csv table header
    csvWriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    csvWriter.writerow(['facultyName','subjectName','courseLetters','courseNumbers','courseTitle','courseSummary'])
    print('Webcrawler is now running. To ensure crawler is not spamming the server, a hard coded delay is in place.')
    print('Please do not modify/remove the delay, as this will slow down the target server and can lead to reprocussions')
    print('This should take about 6 hours, please be patient as it runs. The program will never freeze.')

    #Now use the faculty link stored in memory to traverse the given page to now gather the 
    #course subjects' codename, name, and link.
    for facultyName, facultyURL in facultyLinks.items():
        courseSubjectPage = urlopen(UA_ROOT_URL+facultyURL)
        #Added intentional delay so as not to spam server with page requests all at once
        #No delay specified in the U of A robots.txt, so the limit is set to 2. 
        #Please do not edit or remove, as spamming the server may hypothetically lead to an IP block or
        #future bot blocking measures 
        time.sleep(2)
        courseSubjectSoup = bs(courseSubjectPage, 'html.parser')
        subjectTable = courseSubjectSoup.find('table',{'class':'pure-table pure-table-striped'})
        subjectRows = subjectTable.findAll('tr')
        #Clear out previous subjects
        subjectLinks = {}
        for subjectRow in subjectRows:
            subjectCols = subjectRow.findAll('td')
            if(len(subjectCols)==2):
                subjectATag = subjectCols[0]
                subjectLongName = subjectCols[1]
                subjectLinks[subjectATag.find('a').contents[0]] = subjectATag.find('a').get('href')
                subjectNamePairs[subjectATag.find('a').contents[0]] = subjectLongName.contents[0].strip()

        #Finally take each subject URL to get all the courses within that given subject
        for subjectName, subjectURL in subjectLinks.items():
            coursePage = urlopen(UA_ROOT_URL+subjectURL)
            time.sleep(2)
            courseSoup = bs(coursePage,'html.parser')
            courseDivs = courseSoup.findAll('div',{'class':'claptrap-course'})
            #print(courseDivs)
            for courseDiv in courseDivs:
                courseCode = courseDiv.find('span',{'class':'claptrap-course-number'}).contents[0].strip()
                courseNumber = ''.join(filter(str.isdigit,courseCode))
                courseLetters = ''.join(filter(lambda x: x.isalpha(), courseCode))
                courseTitle = courseDiv.find('span',{'class':'claptrap-course-title'}).contents[0].strip()
                courseSummaryPTag = courseDiv.find('p')
                #If no Description is available
                if courseSummaryPTag is None:
                    courseSummary = 'No description available for this course.'
                else:
                    courseSummary = courseDiv.find('p').contents[2].strip()
                csvWriter.writerow([facultyName,subjectNamePairs[subjectName],courseLetters,courseNumber,courseTitle,courseSummary])
                print(facultyName,subjectNamePairs[subjectName] ,courseLetters,courseNumber,courseTitle,courseSummary)
            print('.')
print('Done!')




#print(courseFacultySoup.find_all('a'))