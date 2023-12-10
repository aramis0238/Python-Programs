import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from tkinter import messagebox
import requests
from PIL import Image
from fpdf import FPDF
from datetime import datetime


# NOTE: variable names correspond to names of elements being clicked on, not the actual ID of the elements.




def init_selenium_webdriver():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Uncomment this line to run Chrome in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    
    global print_to_pdfPath, submissionNumber
    print_to_pdfPath = ""
    options.add_argument(f"--print-to-pdf={print_to_pdfPath}")  # Enable print to PDF

    driver = webdriver.Chrome(options=options)
    return driver

def enter_login(driver, username, password):
    
    # Locate the username and password fields 
    username_box = driver.find_element(By.ID, "ctl00_ctl00_bcph_mca_LoginControl1_tbLogin")
    password_box = driver.find_element(By.ID, "ctl00_ctl00_bcph_mca_LoginControl1_tbPassword")

    # Enter the username and password
    username_box.send_keys(username)
    password_box.send_keys(password)

    # Find the login button and click it
    # Assuming the login button has the type attribute set as "submit"
    login_button = driver.find_element(By.ID, "ctl00_ctl00_bcph_mca_LoginControl1_btnLogin")
    login_button.click()
    
def element_detector(element_ID):

    print("running element detector...")
    element_found = False
    while not element_found:
        try:
            element = driver.find_element(By.ID, element_ID)
            element_found = True
            return element_found, element
            
        except NoSuchElementException:
            messagebox.showinfo("Captcha Warning!", "Please complete captcha!")
            time.sleep(5) # wait 5 seconds to check again for captcha
        
def wait_for_page_load():
    timeout = 10  # Maximum time to wait for the page to load (in seconds)
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print("Page fully loaded!")
    except Exception:
        print("Timeout occurred while waiting for the page to load.")
        
def submissions_page(driver):
    
    submissions_link_ID = 'hlMyFilings'
    
    temp, submissions_link = element_detector(submissions_link_ID)
    submissions_link.click()
    
    # create objects for date boxes
    subDateFrom = driver.find_element(By.ID, 'tbSubFrom')
    subDateTo = driver.find_element(By.ID, 'tbSubTo')
    
    # clear contents from 'Submission Date From' text box
    for i in range(len(subDateFrom.get_attribute('value'))):
        subDateFrom.send_keys(Keys.BACK_SPACE)
    
    # clear contents from 'Submission Date To' text box
    for j in range(len(subDateTo.get_attribute('value'))):
        subDateTo.send_keys(Keys.BACK_SPACE)   
    
    # initialize "Matter #" box
    matterNumber = driver.find_element(By.ID, 'tbMatterNumber')
    matterNumber.send_keys("3000998275")
    
    print("What was entered into matter number - ", matterNumber)
    # change time sleep to 0.5 if too quick
    time.sleep(1)
    
    # initialize "Search" box
    searchBtn = driver.find_element(By.ID, 'btnRefresh')
    searchBtn.click()
    print("search button clicked!")
    
    # element in row structure
    # <tr> -> <5th td> -> <a href>
    
def set_pdf_filePath(newPath):
    
    global print_to_pdfPath
    print_to_pdfPath = newPath
    
def find_most_recent_date(dictionary):
    # Initialize a variable to hold the most recent date
    most_recent_date = None
    
    # Iterate through the dictionary values
    for value in dictionary.values():
        # Check if the value is a valid date string
        try:
            date = datetime.strptime(value, "%m/%d/%Y %I:%M:%S %p")
            
            # Update the most recent date if it's None or greater than the current date
            if most_recent_date is None or date > most_recent_date:
                most_recent_date = date
        except ValueError as e:
            print("exception for date - ", e)
            # Ignore non-date values in the dictionary
            continue
    
    # Return the most recent date (or None if no valid dates were found)
    return most_recent_date.strftime("%m/%d/%Y %I:%M:%S %p")

def get_nefNums_and_dates(driver):
    
    # NOTE: selenium  DOES NOT read index of numbers for items on a page in a zero-based indexing method
    # Example - td[3] == 3rd box found in table on page.
    
    nefNums_and_dates = {}
     
    # Find the <tbody> element and identify all <tr> elements within it
    tbody_element = driver.find_element(By.XPATH, "//tbody[@role='rowgroup']")
    tr_elements = tbody_element.find_elements(By.XPATH, ".//tr")
    
    # Iterate through each <tr> element
    for tr_element in tr_elements:
        # Find the 3rd and 8th <td> elements within the current <tr>
        td4_element = tr_element.find_element(By.XPATH, ".//td[4]") # submission/NEF number
        td10_element = tr_element.find_element(By.XPATH, ".//td[10]") # date
        
        # Get the text content of the <td> elements
        td4_text = td4_element.text
        td10_text = td10_element.text
        
        # assign the text content of the <td> elements to a dictionary, key=case number, value=date
        nefNums_and_dates[td4_text] = td10_text
        
        # Perform actions with the retrieved data
        print("4th <td>:", td4_text)
        print("10th <td>:", td10_text)
        
        
    return nefNums_and_dates

def get_docket(driver):
    
    # Find the <tbody> element and identify all <tr> elements within it using function get_nefNums_and_dates()
    nefNums_and_dates = get_nefNums_and_dates(driver)
    
    # Find the most recent date of the case numbers
    most_recent_date = find_most_recent_date(nefNums_and_dates)
    print("most recent date - ", most_recent_date)
    
    # Find the case number of the most recent date
    for nefNum, date in nefNums_and_dates.items():
        if date == most_recent_date:
            return nefNum

    print("nefNum - ", nefNum)
    
    # Find the <tbody> element and identify all <tr> elements within it
    tbody_element = driver.find_element(By.XPATH, "//tbody[@role='rowgroup']")
    tr_elements = tbody_element.find_elements(By.XPATH, ".//tr")
    
    # wait one second
    time.sleep(1)
    
    # check through tds in rows to find nefNum
    for td_element in tr_elements:
        td4_element = td_element.find_element(By.XPATH, ".//td[4]")
        td10_element = td_element.find_element(By.XPATH, ".//td[10]")
        
        # Get the text content of the <td> elements
        td4_text = td4_element.text
        td10_text = td10_element.text
        
        print("(docket) 4th <td>:", td4_text)
        print("(docket) 10th <td>:", td10_text)
        
        if str(nefNum) == td4_text:
            print("nefNum == td4_text!!!")
            docket_link = driver.find_element(By.XPATH, ".//td[5]/a")
            print("docket link - ", docket_link)
            href_value = docket_link.get_attribute("href")
            driver.get(href_value)
            
            print("waiting for page to load...")
            wait_for_page_load()
            
    submissionNumber = td4_text
    newFilepath = os.path.join(os.getcwd(), submissionNumber + ".pdf")
    set_pdf_filePath(newFilepath)
    print("newFilepath - ", newFilepath)
    
    print("6. Take screen shot of the selected docket page!")
    print_screen(driver)

    print("7. Process complete!!!")
    
def print_screen(driver):
    driver.execute_script('window.print();')
    
    
def login_to_website(driver, url, username, password):
    
    print("1. Opening Website")
    driver.get(url)
    
    print("waiting for page to load...")
    wait_for_page_load()

    print("2. Logging in")
    enter_login(driver, username, password)
    
    print("waiting for next page to load...")
    wait_for_page_load()
    
    print("3. Going to Submissions Page")
    submissions_page(driver) # click on submissions page and perform its operations
    
    print("waiting for page to load...")
    wait_for_page_load()
    
    print("4. Pulling up dockets")
    print("waiting for page to load...")
    wait_for_page_load()
    
    print("5. Selecting docket")
    get_docket(driver) # open 
    

if __name__ == '__main__':
    # Initialize Selenium WebDriver
    driver = init_selenium_webdriver()

    # URL and credentials
    url_to_login = "https://www.myexamplesite.com/foo/bar"  # Replace with the login URL
    username = "tempUsername"  # Replace with your username
    password = "tempPass"  # Replace with your password

    # Perform login
    login_to_website(driver, url_to_login, username, password)

    # Perform any additional tasks or scraping
    # ...

    driver.quit()  # Close the driver
