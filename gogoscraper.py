from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
driver = webdriver.Safari() #I actually used the chromedriver and did not test firefox, but it should work.
url="https://www.linkedin.com/jobs/search?keywords=%22Data+Scientist%22&location=France&trk=jobs_jserp_search_button_execute&orig=JSERP&locationId=fr%3A0"
driver.get(url)
html=driver.page_source
soup=BeautifulSoup(html) #specify parser or it will auto-select for you
results_context=soup.find('div', {'class' : 'results-context'}).find('strong')
n_jobs = int(results_context.text.replace(',',''))
print "###### Number of job postings #######"
print n_jobs
print "#####################################"

results = soup.find_all('li', {'class': 'job-listing'})
n_postings = len(results)
print "#### Number of job postings per page ####"
print n_postings
print "#########################################"

print "#### Number of pages ####"
n_pages = int(round(n_jobs/float(n_postings)))
print n_pages
print "#########################"
results = soup.find_all('li', {'class': 'job-listing'})
n_postings = len(results)
print "#### Number of job postings per page ####"
print n_postings
print "#########################################"
print "#### Number of pages ####"
n_pages = int(round(n_jobs/float(n_postings)))
print n_pages
print "#########################"


def beautify(url):
    driver.get(url)
    html=driver.page_source
    return BeautifulSoup(html) #specify parser or it will auto-select for you

titles = []
companies = []
locations = []
links = []
#loop over all pages to get the posting details
for i in range(n_pages):    
    # define the base url for generic searching 
    url = ("https://www.linkedin.com/jobs/search/?keywords=marketing&location=Cleveland%2C%20Ohio&locationId=PLACES.us.1-4-0-18-8")
    url = url.replace('nPostings',str(25*i))
    soup = beautify(url)
    # Build lists for each type of information
    results = soup.find_all('li', {'class': 'job-listing'})
    results.sort()
    # print "there are ", len(results) , " results"
    for res in results:
        # set only the value if get_text() 
        titles.append(res.h2.a.span.get_text() if res.h2.a.span else 'None')
        companies.append( res.find('span',{'class' : 'company-name-text'}).get_text() if
                         res.find('span',{'class' : 'company-name-text'}) else 'None')
        locations.append( res.find('span', {'class' : 'job-location'}).get_text() if
                        res.find('span', {'class' : 'job-location'}) else 'None' )
        links.append(res.find('a',{'class' : 'job-title-link'}).get('href') )

jobs_linkedin = pd.DataFrame({'title' : titles, 'company': companies, 'location': locations, 'link' : links})
jobs_linkedin.count()
jobs_linkedin.to_csv("marketingcleveland.csv", sep='\t', encoding='utf-8')


driver.close()
