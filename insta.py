import time
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import pyjokes
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


# method to click on a element.
def button_click(browser, xpath):
    try:
        button = WebDriverWait(browser, 3).until(EC.presence_of_element_located(
            (By.XPATH, xpath)))
        button.click()
    except TimeoutException:
        print("Loading took too much time!")
    return button


# gets both the follower and the following counts of a account.
# But for this script I will only use followers thing.
def get_followers():
    username = "gurashish_arneja"
    url = 'https://www.instagram.com/' + username
    r = requests.get(url).text

    start = '"edge_followed_by":{"count":'
    end = '},"followed_by_viewer"'
    followers = r[r.find(start) + len(start):r.rfind(end)]

    start = '"edge_follow":{"count":'
    end = '},"follows_viewer"'
    following = r[r.find(start) + len(start):r.rfind(end)]
    return followers
    # print(followers, following)


if __name__ == '__main__':
    # Starting the chrome and logging in
    browser = webdriver.Chrome(r"C:\Users\guras\Downloads\chromedriver_win32\chromedriver.exe")
    browser.get('https://www.instagram.com/')
    time.sleep(2)
    # filling in the fields
    user = browser.find_element_by_name("username")
    user.send_keys("")
    passwd = browser.find_element_by_name("password")
    passwd.send_keys("")
    time.sleep(2)
    # logging in
    button_click(browser, '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button' )
    time.sleep(3)

    # Bypassing the not now button
    # Special check because the not now button sometimes doesn't appear
    if browser.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').size != 0:
        nn_button = browser.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
        nn_button.click()
        time.sleep(1)

    # Clicks on the profile button to get the profile page
    try:
        browser.refresh()
        button_click(browser, '//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a')
        time.sleep(1)
    except TimeoutException:
        print("Loading took too much time!")

    initial_followers = int(get_followers())

    try:
        while True:
            time.sleep(6)
            num = get_followers()
            # print(num)
            followers = int(num)
            # print(followers)

            # If the numbers of followers change
            if followers != initial_followers:
                initial_followers = followers
                # edit_profile_button
                button_click(browser,
                             '//*[@id="react-root"]/section/main/div/header/section/div[1]/a/button')

                # get the joke
                joke = pyjokes.get_joke()
                # clicking on bio button to edit the bio.
                bio = button_click(browser, '//*[@id="pepBio"]')
                bio.clear()

                # maximum bio length for instagram is only 150. So checking for that.
                line = ('Realtime followers : ' + str(initial_followers) + '\n'
                        + 'Joke : ' + joke)
                if len(line) > 149:
                    line = ('Realtime followers : ' + str(initial_followers) + '\n'
                            + 'Joke : ' + "Liverpool")

                bio.send_keys(line)

                # submit button
                button_click(browser,
                             '//*[@id="react-root"]/section/main/div/article/form/div[11]/div/div/button[1]')
                browser.back()
    except:
        print('Something went wrong while trying to update the bio')
