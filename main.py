import os
import random
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from time_util import sleep
from util import page_id_parser
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import re
import ctypes


# Automates facebook invitations to people who engage with a post but hasn't liked the fanpage yet.
# author @eduardoawakens

def click(x, y):
    # to adjust a new position use $ xdotool getmouselocation
    pyautogui.moveTo(x, y, duration=1)
    pyautogui.click(x, y)
    time.sleep(3)


def post_link_parser(post_link):
    parsed = post_link.replace("https://www.facebook.com/", "").split("/")
    return parsed


def main(usr, psw, post):
    email = usr
    password = psw
    post_url = post
    page_name = post_link_parser(post_url)[0]
    # type = post_link_parser(post_url)[1]
    type_owner = post_link_parser(post_url)[2]
    post_details_content_id = post_link_parser(post_url)[3].replace("a.", "")

    # Create a new Chrome session
    chromedriver_location = "/home/eduardo/PycharmProjects/FacebookConda/chromedriver"
    driver = webdriver.Chrome(chromedriver_location)
    driver.maximize_window()

    # Log in
    driver.get("https://www.facebook.com")
    search_field = driver.find_element_by_id("email")
    search_field.send_keys(email)
    search_field = driver.find_element_by_id("pass")
    search_field.send_keys(password)
    search_field.submit()

    print("Logged in as " + email)
    sleep(5)

    # Navigate to the post url
    driver.get(post_url)
    sleep(1)
    click(297, 201)  # Click on Block notifications by Facebook
    sleep(1)
    # engagement_div = driver.find_element_by_css_selector("a[href*='/ufi/reaction']")
    # driver.execute_script("arguments[0].click();", engagement_div)

    # Get page id
    driver.get(f"https://www.facebook.com/{page_name}/")
    page_source = driver.page_source
    sleep(1)
    print(page_source)
    page_id = page_id_parser(page_source)
    print(page_id)
    driver.get(
        f"https://business.facebook.com/creatorstudio/published?content_table=POSTED_POSTS&post_details_content_id={post_details_content_id}&post_details_content_type=PHOTO&post_details_content_owner_id={page_id}")

    # engagement_link = f'https://business.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier={post_details_content_id}&av={page_id}'

    sleep(5)
    print("Loading all the users who engaged")
    click(521, 879)  # Click on Like icon
    sleep(1)

    # Invite people
    while True:
        try:
            viewMoreButton = driver.find_element_by_css_selector("a[href*='/ufi/reaction/profile/browser/fetch']")
            driver.execute_script("arguments[0].click();", viewMoreButton)
            sleep(2)
        except NoSuchElementException:
            break

    print("Inviting the users.")
    users = driver.find_elements_by_css_selector("a[ajaxify*='/pages/post_like_invite/send/']")
    invitedUsers = 0

    for i in users:
        user = driver.find_element_by_css_selector("a[ajaxify*='/pages/post_like_invite/send/']")
        driver.execute_script("arguments[0].click();", user)
        invitedUsers = invitedUsers + 1
        sleep(1)

    print(f'{str(invitedUsers)} invitations sent')

    # Close the browser window
    driver.quit()


if __name__ == "__main__":
    args = sys.argv[1:]
    AFFIRMATIONS = ["good", "correct", "let's do it"]
    # Check for the arg pattern:
    # python3 affirm.py user password link
    # e.g. args[0] is user, args[1] is password and args[2] is the link of the post
    if len(args) == 3:
        affirmation = random.choice(AFFIRMATIONS)
        print(affirmation, args[0])
        usr = args[0]
        psw = args[1]
        post = args[2]
    main(usr, psw, post)
