import webbrowser
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import mail_functions

def notify_user(url):
    # webbrowser.open("https://www.youtube.com/watch?v=c9e-80s3kOY&t=1m")
    # time.sleep(2.2)
    webbrowser.open(url)
    print("No alert found")

def is_alert_visible(driver):
    try:
        alert = Wait(driver, 0.5).until(EC.alert_is_present())
        return alert.text
    except (TimeoutException,):
        return False

def init_driver(driver_position, timeout):
    driver = webdriver.Chrome(driver_position)
    driver.set_page_load_timeout(timeout)
    driver.set_window_position(800, 0)
    return driver

def get_codes():
    soda = [1404, 1405, 1406]
    univ = [1407, 1408, 1409]
    beauty = [1410, 1411, 1412]
    sing = [1413, 1414]
    summer = [1415, 1416, 1417]
    autumn = [1418, 1419, 1420]
    winter = [1421, 1422, 1423]
    trouble =[1424, 1425, 1426]
    once = [1427, 1428]
    spring = [1429, 1430, 1431]
    return soda, univ, beauty, sing, summer, autumn, winter, trouble, once, spring


def get_code2date():
    code2date = {1404: "08/05", 1405: "08/06", 1406: "08/07",
                 1407: "08/12", 1408: "08/13", 1409: "08/14",
                 1410: "08/19", 1411: "08/20", 1412: "08/21",
                 1413: "08/27", 1414: "08/28",
                 1415: "09/02", 1416: "09/03", 1417: "09/04",
                 1418: "09/09", 1419: "09/10", 1420: "09/11",
                 1421: "09/16", 1422: "09/17", 1423: "09/18",
                 1424: "09/23", 1425: "09/24", 1426: "09/25",
                 1427: "10/01", 1428: "10/02",
                 1429: "10/07", 1430: "10/08", 1431: "10/09"}
    return code2date


if __name__ == '__main__':

    soda, univ, beauty, sing, summer, autumn, winter, trouble, once, spring = get_codes()
    code2date = get_code2date()
    codes = univ + beauty + sing + summer + autumn + winter + trouble + once + spring
    urls = []
    main_url = "https://tixcraft.com/ticket/area/16_soda/"
    for num in codes:
        urls.append(main_url + str(num))

    driver_position = '/home/anson/chromedriver'
    driver = init_driver(driver_position, 4)
    got_ticket = False
    reset_driver = False
    should_notify_user = False
    prev_time = 0
    curr_time = 0
    count = 0

    while True:
        for url, code in zip(urls, codes):
            if reset_driver or (prev_time > 2.5 and curr_time > 2.5):
                try:
                    driver.quit()
                except:
                    print("No driver to quit")
                driver = init_driver(driver_position, 4)
                curr_time = 0
                count = 0
                reset_driver = False

            count += 1      
            try:
                prev_time = curr_time
                start = time.time()
                driver.get(url)
                end = time.time()
                curr_time = end - start
                alert_found = is_alert_visible(driver)
                if not alert_found:
                    mail_functions.notify_email(code2date[code])
                    if should_notify_user:
                        notify_user(url)
                        got_ticket = True
                        driver.quit()
                        break
                else:                    
                    driver.switch_to_alert().accept()
                    print(alert_found + " " + str(count) + " Elapsed time: " + str(curr_time))
            except:
                print("Error getting from url")
                reset_driver = True
                driver.quit()

        if got_ticket:
            break

