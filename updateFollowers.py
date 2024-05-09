from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

#### IMPORTANT ####
# Change the following username and password to load into your desired account
# (i promise it wont be saved anywhere :) )
INSTAGRAM_USERNAME = "Example_username"
INSTAGRAM_PASSWORD = "Example_pass"

def get_driver(headless=False):
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

    if headless:
        options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=options)
    
    return driver

def log_in(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD, driver=None):
    print("logging in...")
    if(driver is None):
        driver = get_driver()
    url = "https://www.instagram.com/"
    driver.get(url)

    #Login logic, set your username and password to the right values
    USERNAME_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input'
    PASSWORD_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input'
    LOGIN_BUTTON_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button'
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, USERNAME_XPATH)))
    username_input = driver.find_element(By.XPATH, USERNAME_XPATH)
    password_input = driver.find_element(By.XPATH, PASSWORD_XPATH)
    login_button = driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH)
    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()

    MY_PROFILE_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[8]/div/span/div/a'

    WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.XPATH, MY_PROFILE_XPATH)))

    return driver

def get_followers(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD, driver=None, loggedIn=False):    
    if driver is None:
        driver = get_driver()
    
    #Login logic, set your username and password to the right values
    if not loggedIn:
        url = "https://www.instagram.com/"
        driver.get(url)
        USERNAME_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input'
        PASSWORD_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input'
        LOGIN_BUTTON_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button'
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, USERNAME_XPATH)))
        username_input = driver.find_element(By.XPATH, USERNAME_XPATH)
        password_input = driver.find_element(By.XPATH, PASSWORD_XPATH)
        login_button = driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH)
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

    #Navigates to home profile page
    MY_PROFILE_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[8]/div/span/div/a'
    WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.XPATH, MY_PROFILE_XPATH)))
    driver.find_element(By.XPATH, MY_PROFILE_XPATH).click()
    return_url = driver.current_url

    #Opens the followers modal
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "followers")))
    num_followers = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span').text
    print(num_followers, "followers")
    driver.find_element(By.PARTIAL_LINK_TEXT, "followers").click()

    FOLLOWERS_MODAL_XPATH = '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]'
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, FOLLOWERS_MODAL_XPATH)))
    
    #Loads all followers, since instagram loads by batch into document HTML
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,"_aano")))
    followers_modal = driver.find_element(By.CLASS_NAME,'_aano')
    num_loaded_followers = 0
    num_iterations=0
    while  num_loaded_followers != int(num_followers):
        print("Loaded # followings: ",num_loaded_followers,"Expected num: ",int(num_followers), "scrolling down...\n")
        followers_modal = driver.find_element(By.CLASS_NAME,'_aano')
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', followers_modal)
        time.sleep(1.5)
        FOLLOWERS_LABEL_XPATH = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div"
        if num_loaded_followers == len(driver.find_elements(By.XPATH, FOLLOWERS_LABEL_XPATH)):
            num_iterations+=1
        else:
            num_loaded_followers = len(driver.find_elements(By.XPATH, FOLLOWERS_LABEL_XPATH))
            num_iterations=0
        if num_iterations==10:
            raise Exception("Failed to load all followers, stuck at ",num_loaded_followers, " followers. If problem persists, account may be rate limited. Try again later")
    
    #Returns entire body HTML
    print('\n\n\nDONE LOADING FOLLOWERS')
    body_text = driver.execute_script("return document.body.outerHTML;")
    print("Found followers, saving body text")
    driver.get(return_url)
    
    return body_text

def get_following(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD, driver=None, loggedIn=False):    
    if driver is None:
        driver = get_driver()

    url = "https://www.instagram.com/"
    driver.get(url)
    
    #Login logic, set your username and password to the right values
    if not loggedIn:
        USERNAME_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input'
        PASSWORD_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input'
        LOGIN_BUTTON_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button'
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, USERNAME_XPATH)))
        username_input = driver.find_element(By.XPATH, USERNAME_XPATH)
        password_input = driver.find_element(By.XPATH, PASSWORD_XPATH)
        login_button = driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH)
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

    #Navigates to home profile page
    MY_PROFILE_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[8]/div/span/div/a'
    WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.XPATH, MY_PROFILE_XPATH)))
    driver.find_element(By.XPATH, MY_PROFILE_XPATH).click()
    return_url = driver.current_url

    #Opens the followers modal
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "followers")))
    num_following = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span').text
    print(num_following, "following")
    driver.find_element(By.PARTIAL_LINK_TEXT, "following").click()

    #Loads all followers, since instagram loads by batch into document HTML
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,"_aano")))
    following_modal = driver.find_element(By.CLASS_NAME,'_aano')
    num_loaded_following = 0
    num_iterations=0
    while  num_loaded_following != int(num_following):
        print("Loaded # followings: ",num_loaded_following,"Expected num: ",int(num_following), "scrolling down...\n")
        following_modal = driver.find_element(By.CLASS_NAME,'_aano')
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', following_modal)
        time.sleep(1.5)
        FOLLOWING_LABEL_XPATH = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div/div"
        if num_loaded_following == len(driver.find_elements(By.XPATH, FOLLOWING_LABEL_XPATH)):
            num_iterations+=1
        else:
            num_loaded_following = len(driver.find_elements(By.XPATH, FOLLOWING_LABEL_XPATH))
            num_iterations=0
        if num_iterations==10:
            raise Exception("Failed to load all followings, stuck at: ",num_loaded_following, "followings. If problem persists, account may be rate limited. Try again later")
    
    #Returns entire body HTML
    print('\n\n\nDONE LOADING FOLLOWINGS')
    body_text = driver.execute_script("return document.body.outerHTML;")
    print("Found followings, saving body text")
    driver.get(return_url)

    return body_text

def write_to_file(content, updating_followers=False):
    if updating_followers:
        if os.path.isfile("my_followers_current.txt"):
            new_name = "my_followers_OLD_LATEST.txt"
            if(os.path.isfile(new_name)):
                os.remove(new_name)
            os.rename("my_followers_current.txt", new_name)
        file = open("my_followers_current.txt", 'w', encoding="UTF-8")
        file.write(content)
        file.close()
    else:
        file = open("my_following.txt",'w', encoding='UTF-8')
        file.write(content)
        file.close()

def update_followers_list(driver=None, loggedIn=False):
    loaded_followers = get_followers(driver=driver, loggedIn=loggedIn)
    write_to_file(loaded_followers)
    print("\nDone updating followers list")

def update_followings_list(driver=None, loggedIn = False):
    loaded_followings = get_following(driver=driver, loggedIn=loggedIn)
    write_to_file(loaded_followings)
    print("\nDone updating followings list")

def user_control():
    isLoggedIn = False
    while(True):
        print("Enter any following number to perform the associated action:\n")
        print("""1-Log in (MANDATORY IF NOT DONE ALREADY)       2-Update followers list\n3-Update following list        4-Quit program""")
        action = input()
        driver = get_driver()
        if '1' in action:
            driver = log_in(driver=driver)
        elif '2' in action:
            if not isLoggedIn:
                log_in(driver=driver)
                isLoggedIn=True
            update_followers_list(driver=driver, loggedIn=isLoggedIn)
        elif '3' in action:
            if not isLoggedIn:
                log_in(driver=driver)
                isLoggedIn=True
            update_followings_list(driver=driver, loggedIn=isLoggedIn)
        else:
            print("Exiting program...")

if __name__ == "__main__":
    user_control()