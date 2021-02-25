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
    return []

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
    options += "Enter a course #, or type \"q\" to quit: "
    return options 

def main():
    try:
        browser = Browser()

    finally: # Always close the browser
        browser.close_browser()    

if __name__ == "__main__":
    main()
