#!venv/bin/python

import csv
import os
import time
import argparse
import getpass
from configparser import ConfigParser
from random import randint
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def chartimer(num_chars, string_speed_fast, string_speed_slow):
    '''used for jittering text input, sort of simulating real user input'''
    fast_char_milliseconds = int((string_speed_fast / num_chars)*1000)
    slow_char_milliseconds = int((string_speed_slow / num_chars)*1000)
    return(fast_char_milliseconds, slow_char_milliseconds)

def main():
    '''Configure Tracker'''
    parser = ConfigParser()
    parser.read('config.ini')
    args = argparse.ArgumentParser(description='FB friend online status data agregation utility')
    args.add_argument(
        '--password', '-p',
        dest='password',
        action='store_true',
        default=False,
        help='Prompt for interactive password, ignoring INI'
        )
    args.add_argument(
        '--username', '-u',
        type=str,
        nargs='?',
        dest='username',
        action='store',
        help='Specify username, ignoring INI'
        )
    args.add_argument(
        '--profile', '-r',
        type=str,
        nargs='?',
        dest='profile',
        action='store',
        help='Specify account name, ignoring INI'
        )
    args.add_argument(
        '--interval', '-v',
        type=int,
        dest='interval',
        action='store',
        help='Set interval time (minutes), ignoring INI'
        )
    args.add_argument(
        '--total', '-t',
        type=int,
        dest='total',
        action='store',
        help='Prompt for total time (hours), ignoring INI'
        )
    args.add_argument(
        '--interactive', '-i',
        dest='headless',
        action='store_false',
        default=bool(parser.get('fb', 'headless')),
        help='Run interactively instead of headless, ignoring INI'
        )

    argvars = args.parse_args()
    fb_username = str(parser.get('fb', 'username')) if argvars.username is None else argvars.username
    fb_profilename = str(parser.get('fb', 'profilename')) if argvars.profile is None else argvars.profile
    fb_password = str(parser.get('fb', 'password') if argvars.password is False else str(getpass.getpass('password: ')))
    interval_time = (int(parser.get('fb', 'interval_time')) * 60) if argvars.interval is None else argvars.interval * 60
    total_time = (int(parser.get('fb', 'total_time')) * 3600) if argvars.total is None else argvars.total * 3600
    number_of_iterations = total_time / interval_time
    print(number_of_iterations, "interations within", total_time/3600, "hrs total time @", interval_time/60, "min interval")

    csv_file1 = 'fb_online_count.csv'
    if not os.path.exists(csv_file1):
        with open(csv_file1, 'w') as fil:
            writer = csv.writer(fil, delimiter=',')
            writer.writerow(['datestamp', 'hour', 'minute', 'online_count'])
            print('CSV created: ' + csv_file1)

    csv_file2 = 'fb_online_users.csv'
    if os.path.exists(csv_file2):
        last_line = open(csv_file2, "r").readlines()[-1:]
        reader = csv.reader(last_line, delimiter=',')
        lastrow = next(reader)
        last_pk = int(lastrow[0])
    else:
        last_pk = -1
        with open(csv_file2, 'w') as fil:
            writer = csv.writer(fil, delimiter=',')
            writer.writerow(['id', 'date', 'hour', 'minute', 'username'])
            print('CSV created: ' + csv_file2)

    options = Options()
    if argvars.headless:
        options.add_argument("--headless")
        options.add_argument("--window-size=1400,10000")
        driver = webdriver.Chrome(chrome_options=options)
    else:
        driver = webdriver.Chrome()
        driver.set_window_size(1200, 1600)

    driver.implicitly_wait(5)
    print('Logging into fb...')
    driver.get('https://www.facebook.com/')

    email_box = driver.find_element_by_id('email')
    time.sleep(randint(50, 200)/100)
    millis_range_password = chartimer(len(fb_username), 1, 3)
    for char in fb_username:
        rand_seconds = randint(millis_range_password[0], millis_range_password[1])/1000
        email_box.send_keys(char)
        time.sleep(rand_seconds)
    print('username sent')

    password_box = driver.find_element_by_id('pass')
    time.sleep(randint(50, 200)/100)
    millis_range_password = chartimer(len(fb_password), 1, 3)
    for char in fb_password:
        rand_seconds = randint(millis_range_password[0], millis_range_password[1])/1000
        password_box.send_keys(char)
        time.sleep(rand_seconds)
    print('password sent')
    time.sleep(randint(50, 100)/100)
    driver.find_element_by_id('loginbutton').click()
    driver.get('https://www.facebook.com/' + fb_profilename + '/about')
    try:
        driver.find_element_by_xpath("//a[@action='cancel'][@role='button']").click()
    except:
        print('no disable notification popup detected at login')

    iteration = 0
    while iteration < number_of_iterations:
        time.sleep(5)
        users_online = driver.find_elements_by_xpath('//div[@data-testid="chat_sidebar"]/div/ul/li/a/div/div/div/span/../../../div[3]')
        online_count = len(users_online)
        print(online_count, 'users online:', end=' ')
        fullstamp = datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
        datenow = datetime.now().strftime('%Y/%m/%d')
        hournow = datetime.now().strftime('%H')
        minutenow = datetime.now().strftime('%M')
        with open(csv_file1, 'a') as fil:
            writer = csv.writer(fil, delimiter=',')
            writer.writerow([fullstamp, hournow, minutenow, online_count])
        for user in users_online:
            last_pk += 1
            utext = user.text
            print(utext, end=', ')
            with open(csv_file2, 'a') as fil:
                writer = csv.writer(fil, delimiter=',')
                writer.writerow([last_pk, datenow, hournow, minutenow, utext])
        if argvars.headless:
            screenshot = "screenshot1.png"
            driver.save_screenshot(screenshot)
            print('Screenshot saved:', screenshot)
        print('\nWaiting for update')
        # Wait for next interval and increment iteration counter.
        time.sleep(interval_time - 5)
        #driver.refresh()
        iteration += 1
    # Close Chrome WebDriver.
    driver.quit()

if __name__ == "__main__":
    main()
