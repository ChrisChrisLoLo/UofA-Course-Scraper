#NOTE: Must have beautiful soup installed

#Added intentional delay so as not to spam server with page requests all at once
#No delay specified in the U of A robots.txt, so the delay is set to 2 seconds. 
#Please do not edit or remove, as spamming the server may hypothetically lead to an IP block or
#future bot blocking measures 

import csv
import time
import sqlite3
import queries
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

connection, cursor = queries.connect("./courseData.db")


UA_ROOT_URL = 'https://catalogue.ualberta.ca'

#First crawl the course faculty page and gather the faculty link as well as the faculty name for each given
#faculty


try:
    courseFacultyPage = urlopen(UA_ROOT_URL+'/Course')
except:
    raise Exception('Error. Url could not be opened. This probably means that the targeted website has moved been shut down.')

#Reset Db
queries.drop_tables(connection,cursor)
queries.define_tables(connection,cursor)

courseFacultySoup = bs(courseFacultyPage, 'html.parser')
facultyTable = courseFacultySoup.find('table',{'class':'pure-table pure-table-striped'})
faculties = facultyTable.findAll('td')

facultyLinks = []
for faculty in faculties:
    facultyLinks.append((faculty.find('a').contents[0], faculty.find('a').get('href')))
    queries.insertFaculty(connection,cursor,faculty.find('a').contents[0])
#print(facultyLinks)


try:
    with open('UAlbertaCoursesSingleTable.csv','w',newline='') as csvfile:
        #Create csv table header
        #csvWriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        #csvWriter.writerow(['facultyName','subjectName','courseLetters','courseNumbers','courseTitle','courseSummary'])
        print('Webcrawler is now running. To ensure crawler is not spamming the server, a hard coded delay is in place. '
            'Please do not modify/remove the delay, as this will slow down the target server and can lead to reprocussions. '
            'This should several minutes, please be patient as it runs. The program will never freeze.')

        #Now use the faculty link stored in memory to traverse the given page to now gather the 
        #course subjects' codename, name, and link.
        for facultyName, facultyURL in facultyLinks:
            courseSubjectPage = urlopen(UA_ROOT_URL+facultyURL)
            time.sleep(2)
            courseSubjectSoup = bs(courseSubjectPage, 'html.parser')
            subjectTable = courseSubjectSoup.find('table',{'class':'pure-table pure-table-striped'})
            subjectRows = subjectTable.findAll('tr')
            #Clear out previous subjects and dictionaries. Dictionaries are to remember each subjectLink's name and code.
            subjectLinks = []
            subjectLongNameDict = {}
            subjectCodeDict = {}
            for subjectRow in subjectRows:
                subjectCols = subjectRow.findAll('td')
                #make sure the row actually has content in it, since the web page can give blank rows 🙄
                if(len(subjectCols)==2):
                    #Get the subject code , name, and the link of each subject in the faculty page.
                    #Links will be opened in order to find all courses in each subject.
                    subjectATag = subjectCols[0]
                    subjectLink = subjectATag.find('a').get('href')
                    subjectLongNameDict[subjectLink] = subjectCols[1].contents[0].strip()
                    subjectLongName = subjectCols[1].contents[0].strip()
                    subjectCodeDict[subjectLink] = subjectATag.find('a').contents[0]
                    subjectCode = subjectATag.find('a').contents[0]
                    subjectLinks.append(subjectATag.find('a').get('href'))

                    queries.insertSubject(connection,cursor,subjectLongName,subjectCode,facultyName)
            #Finally take each subject URL to get all the courses within that given subject
            for subjectLink in subjectLinks:
                coursePage = urlopen(UA_ROOT_URL+subjectLink)
                time.sleep(2)
                courseSoup = bs(coursePage,'html.parser')
                courseDivs = courseSoup.findAll('div',{'class':'claptrap-course'})
                for courseDiv in courseDivs:
                    #Get course code and split it up to find the course number ONLY
                    courseCode = courseDiv.find('span',{'class':'claptrap-course-number'}).contents[0].strip()
                    courseNumber = ''.join(filter(str.isdigit,courseCode))
                    courseTitle = courseDiv.find('span',{'class':'claptrap-course-title'}).contents[0].strip()
                    courseSummaryPTag = courseDiv.find('p')
                    #If no Description is available
                    if courseSummaryPTag is None:
                        courseSummary = 'No description available for this course.'
                    else:
                        courseSummary = courseDiv.find('p').contents[2].strip()

                    queries.insertCourse(connection,cursor,courseCode,courseTitle,courseSummary,subjectCodeDict[subjectLink])

                    #Go to course detail page
                    courseDetailURL = "https://catalogue.ualberta.ca/Course/Details?subjectCode={}&catalog={}&previousTerms=True"\
                                        .format(subjectCodeDict[subjectLink],courseNumber)
                    '''
                    try:
                        courseDetailPage = urlopen(UA_ROOT_URL+'/Course')
                        time.sleep(2)
                    except:
                        raise Exception('Error. Wtf is up with the courseDetail page.')
                    courseDetailSoup = bs(courseDetailPage, 'html.parser')
                    subjectTable = courseDetailSoup.find('table',{'class':'pure-table pure-table-striped'})
                    subjectRows = subjectTable.findAll('tr')
                    '''
                    #csvWriter.writerow([facultyName,subjectLongNameDict[subjectLink],subjectCodeDict[subjectLink],courseNumber,courseTitle,courseSummary])
                    #print(facultyName,subjectLongNameDict[subjectLink],subjectCodeDict[subjectLink],courseNumber,courseTitle)

                print('.')
            
    print('Done!')
except Exception as e:
    print(e)
    print('Error. An exception has occurred while scraping.'
            'It is very likely that the page layout has been'
            'altered since this script has been made. A new script'
            'may be needed to scrape this page.')
    raise(e)
    