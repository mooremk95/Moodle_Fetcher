from Browser import Browser
from Course import Course

def build_courses(browser, course_pair_list):
    """Takes in a course pair list of (course_name, url) pairs. Returns a list of Course objects
    created from each entry in the course_pair_list. 

    Args:
        browser (Browser): An instance of the Browser class
        course_pair_list (list): a list of (course_name, url) string pairs
    
    Return:
        course_list (list): a list of Course objects
    """
    return [Course(pair[0], pair[1], browser) for pair in course_pair_list]

def get_course_num(course_count, iput):
    """Gets the course # from user input. Returns -1 if invalid input

    Args:
        course_count (int): number of courses
        iput (string): raw user input string

    Returns:
        int: -1 if invalid user input. Otherwise the course number the user submitted
    """
    try:
        if 0 < int(iput.replace(".","")) <= course_count:
            return int(iput.replace(".","")) - 1
    except:
        return -1
    return -1

def enumerate_options(course_list):
    """Given a course_list generates a propt string which enumerats the courses the user may download.

    Args:
        course_list (list): a list of Course objects

    Returns:
        str : a string detailing the options a user has (courses to fetch files from, and how to exit)
    """
    options = "Courses:\n"
    for i, course in enumerate(course_list):
        options += f"\t{i+1}: {course.get_name()}\n"
    options += "Enter a course number, or type \"q\" to quit: "
    return options 

def main():
    try:
        browser = Browser()
        # Get the raw course data from the Browser object, then create the course list
        course_data = browser.fetch_courses()
        course_list = build_courses(browser, course_data)
        prompt = enumerate_options(course_list)
        while 1:
            iput = input(prompt)
            if iput.lower() == "q":
                print("Closing Program")
                break
            indx = get_course_num(len(course_list), iput)
            if indx == -1:
                print("Ooops, invalid input")
                continue
            course_list[indx].fetch_files()

    finally: # Always close the browser
        browser.close_browser()    

if __name__ == "__main__":
    main()
