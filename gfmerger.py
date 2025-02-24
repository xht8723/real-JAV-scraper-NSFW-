from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

import os
import re
import time

def retry_find_element(driver, by, value, target = None, retries=3, delay=1, log_callback=None):
    for _ in range(retries):
        try:
            element = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((by, value))
            )
            return element
        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            if log_callback and target:
                log_callback(f"retrying find element {target}...\n")
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

def startFirefox(url = None, log_callback=None, isheadless=False):
    if log_callback:
        log_callback("Starting browser\n")
    if isheadless:
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options = options)
    else:
        driver = webdriver.Firefox()
    
    if url:
        driver.get(url)
        if "404" in driver.title:
            raise(Exception("Page not found. Please check connection."))
        return driver
    else:
        driver.get("https://javmodel.com/index.html")
    return driver

def processSearch(driver, name, log_callback=None):
    log_callback("searching for: " + name + "\n")
    searchbtn = retry_find_element(driver, By.XPATH, "/html/body/nav[1]/div/button[2]",target="search button", log_callback = log_callback)
    if searchbtn == None:
        raise(Exception("Search button not found. Please check connection."))
    retry_click(searchbtn, log_callback=log_callback)
    searchField = retry_find_element(driver, By.XPATH, "/html/body/div[10]/div[2]/div[4]/div/div/div/div[1]/div/div/form/input", target="search field", log_callback=log_callback)
    if searchField == None:
        raise(Exception("Search field not found. Please check connection."))
    retry_clear(searchField, log_callback=log_callback)
    searchField.send_keys(name, Keys.ENTER)
    result = retry_find_element(driver, By.XPATH, "/html/body/div[4]/div/div/div/div[1]/div/div[1]/a/span/img", target= "first result",log_callback=log_callback)
    if result == None:
        return None
    retry_click(result, log_callback=log_callback)
    if "hd" in driver.current_url:
        starring = retry_find_element(driver, By.XPATH, "/html/body/div[4]/div/div/div[2]/div[1]/div/div/table/tbody/tr[1]/td[2]/div/ul/li/a",target="starring", log_callback=log_callback)
        if starring == None:
            return None
        retry_click(starring, log_callback=log_callback)
    card = retry_find_element(driver, By.XPATH, "/html/body/div[3]/div[3]/div/div[2]", target= "card", log_callback=log_callback)
    if card == None:
        return None
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
                        if match == ['<name></name>']:
                            if log_callback != None:
                                log_callback(f"No actor name found in {file}\n", "orange")
                            continue
                        for actor in match:
                            actorname = actor[6:-7]
                            if actorname not in actors:
                                filename = os.path.join(root, file)
                                actors[actorname] = [filename]
                            else:
                                filename = os.path.join(root, file)
                                actors[actorname].append(filename)
                    else:
                        if log_callback != None:
                            log_callback(f"No actor name found in {file}\n", "orange")
                if toDir != None:
                    pass
    if log_callback != None:                
        log_callback(f"Found actors number: {len(actors)}\n")
    return actors
        

def modifyNFO(actors, actor, names, toDir=None, log_callback=None):
    primaryName = decidePrimaryName(names)
    for file in actors[actor]:
        with open(file, 'r', encoding='utf-8') as f:
            data = f.read()
            match = re.findall(r'<actor>.*?</actor>', data, flags=re.UNICODE | re.DOTALL)
            if match:
                for matchactor in match:
                    if actor in matchactor:
                        match = matchactor
                altnames = ""
                for name in names:
                    altnames += f'\t\t<altname>{name}</altname>\n'
                new_actor_data = f'<actor>\n\t\t<name>{primaryName}</name>\n{altnames}\n\t\t<tmdbid>{primaryName}</tmdbid>\n\t\t<role>Actress</role>\n\t\t<type>Actor</type>\n\t</actor>'
                data = re.sub(re.escape(match), new_actor_data, data, flags=re.UNICODE | re.DOTALL)
            
            match = re.search(r'\n<tag>.*?</tag>', data, flags=re.UNICODE | re.DOTALL)
            if match:
                data = re.sub(r'\n<tag>.*?</tag>', '', data, flags=re.UNICODE | re.DOTALL)

            match = re.search(r'</movie>', data, flags=re.UNICODE)
            if match:
                tags = ""
                for name in names:
                    tags += f'\t<tag>{name}</tag>\n'
                tags = tags.rstrip('\n')
                data = re.sub(r'</movie>', f'{tags}\n</movie>', data, flags=re.UNICODE)

        if toDir is not None:
            with open(os.path.join(toDir, os.path.basename(file)), 'w', encoding='utf-8') as f:
                f.write(data)
        else:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(data)
        log_callback(f"Modified actress info for {file}\n")

def decidePrimaryName(names):
    hiragana_characters = re.compile(r'[\u3040-\u309F]')
    katakana_characters = re.compile(r'[\u30A0-\u30FF]')
    any_han = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf\uF900-\uFAFF]')
    for name in names:
        if hiragana_characters.search(name) or katakana_characters.search(name):
            return name
    for name in names:
        if any_han.search(name):
            return name
    return names[0] if names else None