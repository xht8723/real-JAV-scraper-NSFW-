from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

import os
import shutil
import re
import time

def retry_find_element(driver, by, value, retries=2, delay=2, log_callback=None):
    for _ in range(retries):
        try:
            element = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((by, value))
            )
            return element
        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            if log_callback:
                log_callback(f"retrying...\n")
            time.sleep(delay)
    return None

def retry_click(element, retries=3, delay=1, log_callback=None):
    for _ in range(retries):
        try:
            element.click()
            return True
        except Exception as e:
            if log_callback:
                log_callback(f"retrying click...\n")
            time.sleep(delay)
    return None

def retry_clear(element, retries=3, delay=1, log_callback=None):
    for _ in range(retries):
        try:
            element.clear()
            return True
        except Exception as e:
            if log_callback:
                log_callback(f"retrying clear...\n")
            time.sleep(delay)

def startFirefox(log_callback=None, isheadless=False):
    if log_callback:
        log_callback("Starting browser\n")
    if isheadless:
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options = options)
    else:
        driver = webdriver.Firefox()
    driver.get("https://javmodel.com/index.html")
    return driver

def processSearch(driver, name, log_callback=None):
    log_callback("searching for: " + name + "\n")
    searchField = retry_find_element(driver, By.XPATH, "/html/body/nav[1]/div/button[2]", log_callback = log_callback)
    if searchField == None:
        raise(Exception("Search field not found. Please check connection."))
    retry_click(searchField, log_callback=log_callback)
    searchField = retry_find_element(driver, By.XPATH, "/html/body/div[10]/div[2]/div[4]/div/div/div/div[1]/div/div/form/input", log_callback=log_callback)
    if searchField == None:
        raise(Exception("Search field not found. Please check connection."))
    retry_clear(searchField, log_callback=log_callback)
    searchField.send_keys(name, Keys.ENTER)
    result = retry_find_element(driver, By.XPATH, "/html/body/div[4]/div/div/div/div[1]/div/div[1]/a/span/img", log_callback=log_callback)
    if result == None:
        return None
    retry_click(result, log_callback=log_callback)
    card = retry_find_element(driver, By.XPATH, "/html/body/div[3]/div[3]/div/div[2]", log_callback=log_callback)
    if card == None:
        raise(Exception("Card not found. Please check connection."))
    return card.get_attribute("innerHTML")

def processCardInfo(card, log_callback=None):
    names = []
    match = re.findall(r'"actor">.*?</h1>', card, flags = re.UNICODE)
    cnMatch = re.findall(r'"actor">.*?</h2>', card, flags = re.UNICODE)
    if match:
        names.append(match[0][8:-5])
        altname = match[0][8:-5].split(" ")
        altname = altname[1] + " " + altname[0]
        names.append(altname)
    if cnMatch:
        temp = cnMatch[0][8:-5].split("  -  ")
        for name in temp:
            name = name.strip(" ")
            names.append(name)
    if log_callback != None:
        log_callback(f"Found names: {names}\n")
    return names
    
def searchNFO(dir, toDir=None, log_callback=None):
    nfoFormat = '.nfo'
    blacklist = 'movie.nfo'
    actors = {}
    for root, dirs, files in os.walk(dir):
        for file in files:
            if nfoFormat in file and file != blacklist:
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    match = re.findall(r'<name>.*?</name>', f.read(), flags = re.UNICODE)
                    if match:
                        for actor in match:
                            actorname = actor[6:-7]
                            if actorname not in actors:
                                filename = os.path.join(root, file)
                                actors[actorname] = [filename]
                            else:
                                filename = os.path.join(root, file)
                                actors[actorname].append(filename)
                if toDir != None:
                    shutil.copy(os.path.join(root, file), os.path.join(toDir, file))
    if log_callback != None:                
        log_callback(f"Found actors number: {len(actors)}\n")
    return actors
        

def modifyNFO(actors, actor, names, toDir=None, log_callback=None):
        for file in actors[actor]:
            with open(file, 'r', encoding='utf-8') as f:
                data = f.read()
                new_lines = []
                for line in data.splitlines():
                    new_lines.append(line)
                    if '<tag>' in line and '</tag>' in line:
                        for name in names:
                            if name not in line:
                                new_lines.append(f'\t<tag>{name}</tag>')
                    if '<name>' in line and '</name>' in line:
                        for name in names:
                            if name not in line:
                                new_lines.append(f'\t\t<name>{name}</name>')
                new_data = '\n'.join(new_lines)
                if toDir != None:
                    with open(os.path.join(toDir, os.path.basename(file)), 'w', encoding='utf-8') as f:
                        f.write(new_data)
                else:
                    with open(file, 'w', encoding='utf-8') as f:
                        f.write(new_data)
            log_callback(f"Modified actress info for {file}\n")

# if __name__ == "__main__":
#     dir = "Z:/r18/test"
#     toDir = "Z:/r18/test/tt"

#     actors = searchNFO(dir)
#     driver = startFirefox()
#     for actor in actors:
#         card = processSearch(driver, actor)
#         names = processCardInfo(card)
#         print(names)
#         modifyNFO(actors, actor, names)
#     driver.quit()

