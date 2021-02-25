from pathlib import Path
from os.path import isdir, isfile
from os import makedirs
from re import sub
from Browser import Browser


HOME = str(Path.home())

class Course():
    def __init__(self, name, url, browser):
        """Couse constructor. 

        Args:
            name ([type]): [description]
            url ([type]): [description]
            browser ([type]): [description]
        """
        self.__name = name
        self.__url = url
        self.__broswer = browser
        self.__destination = None
        self.__document_list = [] 

    def __set_dir__(self):
        """Set the destinaiton directory per user input. Create the directory if it DNE.
        """
        dirpath = input("Enter Destination Directory: ")
        dirpath = sub("~|~/", HOME, dirpath).replace(" ", "_")
        self.__destination = dirpath
        if not isdir(dirpath):
            makedirs(dirpath)

    def __check_log__ (self):
        # TODO: THis
        if self.__destination is None:
            self.__set_dir__()

    def __set_log__(self):
        # TODO: This
        pass

    def __restrict_list__(self):
        #TODO: This
        pass

    def __download_file__(self, name_url_pair):
        # TODO: This
        pass

    def fetch_files(self):
        """
        Uses the associated Browser instance, and course's URL to scrape moodle course page for links to
        PDFs, Word docs, and ppt files. Fetches these files and saves them to directories within the 
        destination directory per filetype (pdf, docx, etc.) If not in overwrite mode, determines which 
        fiiles have aleady been downloaded per the previous_downloads.log file and ommits them from downloading. 
        """
        self.__set_dir__()
        if input("Overwrite previously downloaded files? (y/n) ").lower() in ["n", "no"]:
            print("Only Writing New") 
        else:
            print("Overwritting")


if __name__ == "__main__":
    url = input("enter url: ")
    name = input("enter name: ")
    b = Browser()
    c = Course(name, url, b)
    c.fetch_files()