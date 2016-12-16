from bs4 import BeautifulSoup
import urllib2
import re
import os
import sys
import getopt

def getContestCode(address):
	x = 1
	while address[x] != '/':
		x += 1
	return address[1:x]

def getProblemCode(address, userNameLength):
	x = len(address) - userNameLength - 1
	y = x
	while address[x] != '/':
		x -= 1
	return address[x+1:y]

def getLanguageExtension(strg):
	if len(strg) == 1 and strg == 'C':
		return '.c'
	if strg[0:3] == 'C++':
		return '.cpp'
	if strg[0:4] == 'JAVA':
		return '.java'
	if strg[0:4] == 'PYTH':
		return '.py'
	return '-1'

def main(argv):

	argList = getopt.getopt(argv, "hd")
	userName = str(argList[1][0])

	url = "https://www.codechef.com/users/" + userName
	userNameLength = len(userName)

	content = urllib2.urlopen(url).read()

	soup = BeautifulSoup(content, "lxml")

	if not os.path.exists('Practice'):
		os.makedirs('Practice')

	base = os.getcwd()

	os.chdir(base + '/Practice')

	for link in soup.find_all('a', href=re.compile('^/status/')):

		problemCode = getProblemCode(link.get('href'), userNameLength)

		statusPage = ("https://www.codechef.com" + link.get('href'))
		statusPageStream = urllib2.urlopen(statusPage).read()
		statusPageSoup = BeautifulSoup(statusPageStream, "lxml")

		solcnt = 0
		table = statusPageSoup.find('table', class_='dataTable')
		for row in table.findAll('tr'):
			cells = row.findAll('td')
			if len(cells) != 0:
				if cells[3].span.get('title') == 'accepted' or (cells[3].span.get('title') == '' and cells[3].find(text=True) == '100'):
					lang = getLanguageExtension(cells[6].find(text=True))
					if(lang == '-1'):
						continue
					if not os.path.exists(problemCode):
						os.makedirs(problemCode)
					solutionLink = cells[7].a.get('href')
					solution = "https://www.codechef.com/viewplaintext" + solutionLink[13:]
					fileName = problemCode + '_' + str(solcnt) + lang
					code = urllib2.urlopen(solution).read()
					codeSoup = BeautifulSoup(code, "lxml")
					with open(problemCode + '/' + fileName, 'w') as file:
						file.write(codeSoup.get_text())
					solcnt += 1

	os.chdir(base)

	if not os.path.exists('Contests'):
		os.makedirs('Contests')

	for link in soup.find_all('a', href=re.compile('^(?!/status/).*(/status/).*$')):
	 	
	 	os.chdir(base + '/Contests')
	 	contestCode = getContestCode(link.get('href'))
	 	if not os.path.exists(contestCode):
	 		os.makedirs(contestCode)
	 	os.chdir(base + '/Contests/' + contestCode)

	 	problemCode = getProblemCode(link.get('href'), userNameLength)
	 	
	 	statusPage = ("https://www.codechef.com" + link.get('href'))
	 	statusPageStream = urllib2.urlopen(statusPage).read()
	 	statusPageSoup = BeautifulSoup(statusPageStream, "lxml")
	 	
	 	solcnt = 0
	 	table = statusPageSoup.find('table', class_='dataTable')
	 	for row in table.findAll('tr'):
	 		cells = row.findAll('td')
	 		if len(cells) != 0:
	 			if cells[3].span.get('title') == 'accepted' or (cells[3].span.get('title') == '' and cells[3].find(text=True) == '100'):

	 				lang = getLanguageExtension(cells[6].find(text=True))
					if(lang == '-1'):
						continue
	 				if not os.path.exists(problemCode):
	 					os.makedirs(problemCode)
	 				solutionLink = cells[7].a.get('href')
	 				solution = "https://www.codechef.com/viewplaintext" + solutionLink[13:]
	 				fileName = problemCode + '_' + str(solcnt) + lang
	 				code = urllib2.urlopen(solution).read()
	 				codeSoup = BeautifulSoup(code, "lxml")
	 				with open(problemCode + '/' + fileName, 'w') as file:
	 					file.write(codeSoup.get_text())
	 				solcnt += 1

	os.chdir(base)

if __name__ == "__main__":
	main(sys.argv[1:])
