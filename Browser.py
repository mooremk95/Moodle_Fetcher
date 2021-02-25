from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from time import sleep
import re
from getpass import getpass

MOODLE_HOME = "https://moodle.oakland.edu"
WAIT_TIME = 3

def prettify_name(name):
	"""Helper function prettifying the truncated course names retrieved from 
	moodle. 

	Args:
		name ([type]): [description]

	Returns:
		[type]: [description]
	"""
	# The ugly bits are 5 digits followed by ., followed by 6 digits
	for match in re.findall("\d{5}\.\d{6}|\.{3}", name):
		name = name.replace(match, "")
	return name.replace("--", " ").strip().strip("-")


class Browser():
	"""
	A wrapper class around a headless selenium firefox webdriver. This class logs into moodle
	on initialization, and has methods for generating a requests lib session, scraping course links
	from the user logged in, as well as scaping resource links for PDFs, Word docs, and powerpoint 
	files. 
	"""
	def __init__(self):
		# set up the web driver to be a headless firefox instance
		firefox_opts = webdriver.FirefoxOptions()
		firefox_opts.headless = True
		self.__driver = webdriver.Firefox(options = firefox_opts)
		self.__session = None
		self.__login__()

	def __verify_login__(self):
		"""Validates a login to moodle

		Returns:
			boolean: whether the headless firefox web driver has sucessfully logged into moodle
		"""
		soup = BeautifulSoup(self.__driver.page_source, "html.parser")
		bad_login = soup.find(name="a", attrs={"id": "loginerrormessage"})
		if bad_login:
			return False
		return True

	def __set_session__(self):
		"""After sucessfully logging in this method sets the session property of the Broswer class 
		so that it is  a requests session containing the session cookies for moodle.
		"""
		self.__session = requests.session()
		for cookie in self.__driver.get_cookies():
			self.__session.cookies.set(cookie["name"], cookie["value"])

	
	def __login__(self):
		"""Attempt logging into moodle until success, or the user decides to quit. 
		"""
		while 1:
			uname = input("Enter username (q or quit to exit program): ")
			if uname.lower() in {"q", "quit"}:
				print("Closing")
				self.__driver.close()
				exit()
			pword = getpass("Enter password: ")
			try:
				self.__driver.get(MOODLE_HOME)
				sleep(WAIT_TIME)
				unameField = self.__driver.find_element_by_id("username")
				pwordField = self.__driver.find_element_by_id("password")
				unameField.send_keys(uname)
				pwordField.send_keys(pword)
				pwordField.submit()  # Calling submit on elements w/in a form submits the parent form
			except:
				print("Get Request Errored out. Trying again")
				continue
			sleep(WAIT_TIME)
			if self.__verify_login__():
				print("Seccessful login")
				break
			print("Ooops, invalid login. Try again")
		# Once logged in set the session property
		self.__set_session__()

	def get_session(self):
		return self.__session

	def fetch_links(self, url):
			"""From a course page url, retrieve all of the links to resources which are either pdfs, word docs, or powerpoint files. 

			Args:
				url (string): URL of course page to fetch links from

			Returns:
				list: A list contining pairs of strings of the form (resource_name, url) where url is the url to the resource
			"""
			links = []
			i = 0
			while i < 5:
				try:
					self.__driver.get(url)
					break
				except:
					print("Get Request Errored out. Trying again")
					i += 1
					sleep(WAIT_TIME)
					continue
			sleep(WAIT_TIME)
			links = BeautifulSoup(self.__driver.page_source, "html.parser").findAll(name="a", class_="aalink")
			# Helper which decides if link is to a PDF, Word, or PPT file based on embedded image source (lol kill me)
			def is_document(link):
				img = link.find("img")
				if img:
					src = img["src"].lower()
					if "powerpoint" in src:
						return ".ppt"
					elif "pdf" in src:
						return ".pdf"
				return False
			def get_name(link):
				return link.find(name="span").text
			link_list = []
			for link in links:
				ext = is_document(link)
				if ext:
					name = get_name(link) + ext
					link_list.append((name.replace(" ", "_"), link["href"]))
			return link_list

	def fetch_courses(self):
		"""fetches the courses from the moodle homepage of a logged in user. Generates a list of pairs of (course_name, url)
		pairs where both elements of the pair are strings. 

		Returns:
			list: A list of (couse_name, url) pairs where both elements are strings
		"""
		def get_name(course):
			name_span = course.find(name="span", class_="multiline")
			if name_span is None:
				name_span = course.find(name="span", class_="text-truncate")
			return prettify_name(name_span.string)

		courses = []
		if self.__driver.current_url != MOODLE_HOME:
			while 1:
				try:
					self.__driver.get(MOODLE_HOME)
					sleep(WAIT_TIME)
					break
				except:
					print("Error get requesting moodle homepage. Trying again")
					continue
		page_content = self.__driver.page_source
		soup = BeautifulSoup(page_content, "html.parser")
		course_overview = soup.find(name="section", attrs={"id": "region-main"})
		course_links = course_overview.findAll(name="a", attrs={"class": "aalink coursename mr-2"})
		# Build the list of (course_name, url) pairs
		for link in course_links:
			courses.append((get_name(link), link["href"]))
		return courses

	def close_browser(self):
		"""Simply closes the headless firefox webdriver

		Returns: 
			None: Nothing
		"""
		if self.__driver is not None:
			self.__driver.close()

if __name__ == "__main__":
	print("Running Broswer Demo")
	b = Browser()
	print("Fetching Courses")
	print(b.fetch_courses())
	print("Fetching links")
	url = input("Enter a valid moodle class URL: ")
	print(b.fetch_links(url))
	print(f"Presenting Session:\n{b.get_session()}")	
	b.close_browser()
