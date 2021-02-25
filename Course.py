from pathlib import Path
from Browser import Browser


HOME = str(Path.home)

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
        # TODO: This
        pass

    def __check_json__(self):
        # TODO: THis
        if self.__destination is None:
            self.__set_dir__()

    def __set_json__(self):
        # TODO: This
        pass

    def __restrict_list__(self):
        #TODO: This
        pass

    def __download_file__(self, name_url_pair):
        # TODO: This
        pass

    def fetch_files():
        #TODO: This
        pass