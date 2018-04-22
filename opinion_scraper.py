import urllib2
import sys
import os
from bs4 import BeautifulSoup

def download_file(url, fname):
    response = urllib2.urlopen(url)
    file = open(fname, 'w')
    file.write(response.read())
    file.close()

def scrape_pdf(case, year):
    names = case.split("/")
    session, docket = names[-3], names[-2]
    year_dir = "pdfs/" + str(year) + "/"
    if not os.path.exists(year_dir):
        os.mkdir(year_dir)
    directory = "pdfs/" + str(year) + "/" + str(session) + "/"
    if not os.path.exists(directory):
        os.mkdir(directory)
    fname = directory + docket + ".pdf"
    print "Downloading " + str(year) + "/" + session + "/" + docket + "...",
    try:
        download_file(case, fname)
        print("done")
    except KeyboardInterrupt:
        sys.exit()
    except:
        print("FAILED")

def find_pdf_for_case(case, year):
    try:
        names = case.split("/")
        session, docket = names[-3], names[-2]
        print "Finding PDF for " + str(year) + "/" + session + "/" + docket + "...",
        response = urllib2.urlopen(case)
        soup = BeautifulSoup(response.read(), "lxml")
        a = soup.find("a", class_="pull-right pdf-icon has-margin-bottom-20")
        link = a['href']
        print("done")
        return link
    except KeyboardInterrupt:
        sys.exit()
    except:
        print("FAILED")
        return None 

def scrape_cases(cases, year):
    for case in cases:
        link = find_pdf_for_case(case, year)
        if link is not None:
            scrape_pdf(link, year)

def find_cases_for_year(year):
    url = "https://supreme.justia.com/cases/federal/us/year/" + str(year) + ".html"
    response = urllib2.urlopen(url)
    soup = BeautifulSoup(response.read(), "lxml")
    divs = soup.find_all("div", class_="color-green")
    cases = []
    for element in divs:
        cases.append(element.a.get_text().strip())
    return cases

def scrape_years(start, end):
    for year in range(start, end+1):
        cases = find_cases_for_year(year)
        scrape_cases(cases, year)

def main():
    scrape_years(int(sys.argv[1]), int(sys.argv[2]))

if __name__ == "__main__":
    main()