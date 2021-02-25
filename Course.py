from pathlib import Path
from os.path import isdir, isfile
from os import makedirs
from re import sub
from time import sleep
from Browser import Browser


HOME = str(Path.home())
DOWNLOAD_WAIT_TIME = 1

def prettify_filename(filename):
    filename.replace(" - ", "-").replace(" ", "_")

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
        if not dirpath.endswith("/"):
            dirpath += "/"
        self.__destination = dirpath
        if not isdir(dirpath):
            makedirs(dirpath)

    def __check_log__ (self):
        """Checks whether the destination directory contains a downloaded.log file which records previously downloaded resources.
        Returns:
            boolean: true if downloaded.log exists
        """
        if self.__destination is None:
            self.__set_dir__()
        return isfile(self.__destination + "downloaded.log")

    def __write_log__(self, filename_set):
        """Takes a set of filemane strings. Writes a downloaded.log file containing all of these filenmanes as a \n separated list
        of unicode strings. Overwrites any previously existing downloaded.log file.

        Args:
            filename_set (set): set of filename strings
        """
        with open(self.__destination + "/downloaded.log","w") as f:
            for filename in filename_set:
                f.write(f"{filename}\n")

    def __restrict_lists__(self, link_lists):
        """Restricts the link_lists dicitonary (in place) to lists of (filename, url link) pairs for which a file of the same 
        filenmame has not been downloaded (per downloaded.log)

        Args:
            link_lists (dict): dictionary of file extension key strings to lists of (filename, url) pairs
        """
        with open(self.__destination + "/downloaded.log", "r") as f:
            previous_downloads = {filename for filename in f.read().split("\n")}
        for ext in link_lists.keys():
            link_lists[ext] = [file_pair for file_pair in link_lists[ext] if file_pair[0] not in previous_downloads]
        

    def __download_file__(self, destination, session, name, url):
        """Given a destination string

        Args:
            destination (string): destination folder as a string
            session (requests.Session): requests.session object containing session cookies
            name (string): filename 
            url (string): URL to the associated file on moodle
        Return:
            boolean: True if successful, False if not
        """
        inStream = session.get(url, stream=True) # open a stream to the PDF
        filepath = destination + "/" + name
        if not isdir(destination):
            print(f"Ooops, destination {destination} is not a directory")
            return
        # Check that the stream opened properly
        try:
            inStream.raise_for_status()
            # open and write to the file
            chunk = 1024 # let's use 1kb chunks. Why not? 
            with open(filepath,"wb") as f:
                for chunk in inStream.iter_content(chunk): # iterate over our stream, writing the bytes
                    f.write(chunk)
        except Exception as e:
            print(f"Oops, Something went wrong with the download:\n{e}")
            return False
        return True 

    def fetch_files(self):
        """
        Uses the associated Browser instance, and course's URL to scrape moodle course page for links to
        PDFs, Word docs, and ppt files. Fetches these files and saves them to directories within the 
        destination directory per filetype (pdf, docx, etc.) If not in overwrite mode, determines which 
        fiiles have aleady been downloaded per the previous_downloads.log file and ommits them from downloading. 
        """
        self.__set_dir__()
        # Get the resource file lists form the browser, as well as its session
        file_lists = self.__broswer.fetch_links(self.__url)
        session = self.__broswer.get_session()
        downloaded_filenames = set()
        if self.__check_log__() and input("Overwrite previously downloaded files? (y/n) ").lower() in ["n", "no"]:
            print("Only downloading files not previously downloaded") 
            self.__restrict_lists__(file_lists) # Restrict the lists of filename,link pairs to those not yet downloaded 

        for ext, file_list in file_lists.items():
            subdir = self.__destination + ext.replace(".","")
            if not isdir(subdir):
                makedirs(self.__destination + ext.replace(".", ""))
            # Now loop over the filenames/links to files, and download them
            for i, pair in enumerate(file_list):
                name = pair[0]
                url = pair[1]
                print(f"Downloading file {i + 1} of {len(file_list)} {ext} files. {name}")
                if self.__download_file__(subdir, session, name, url):
                    downloaded_filenames.add(name)
                sleep(DOWNLOAD_WAIT_TIME) # Be polite and give moodle a breather between downloads
        self.__write_log__(downloaded_filenames)
                



if __name__ == "__main__":
    url = input("enter url: ")
    name = input("enter name: ")
    b = Browser()
    c = Course(name, url, b)
    c.fetch_files()
    b.close_browser()