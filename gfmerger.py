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

def retry_click(driver, by, value, retries=3, delay=1, log_callback=None):
    for _ in range(retries):
        try:
            element = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True
        except Exception as e:
            if log_callback:
                log_callback(f"Click failed: {str(e)}")
            time.sleep(delay)
    return False

def retry_clear(driver, by, value, retries=3, delay=1, log_callback=None):
    for _ in range(retries):
        try:
            element = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((by, value)))
            element.clear()
            return True
        except Exception as e:
            if log_callback:
                log_callback(f"retrying clear...\n")
            time.sleep(delay)

def retry_send_keys(driver, by, value, AV, retries=3, delay=1, log_callback=None):
    for _ in range(retries):
        try:
            element = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((by, value)))
            element.send_keys(AV, Keys.ENTER)
            return True
        except Exception as e:
            if log_callback:
                log_callback(f"retrying send keys...\n")
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
        try:
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
        except:
            if log_callback:
                log_callback("Failed to load javmodel.com\n")
    return driver

def processSearch(driver, name, log_callback=None):
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/nav[1]/div/button[2]")))
    except:
        raise(Exception("Search button not found. Please check connection.1"))
    
    log_callback("searching for: " + name + "\n")
    searchbtn = retry_find_element(driver, By.XPATH, "/html/body/nav[1]/div/button[2]",target="search button", log_callback = log_callback)
    if searchbtn == None:
        raise(Exception("Search button not found. Please check connection.2"))
    
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/nav[1]/div/button[2]")))
    except:
        raise(Exception("Search button not found. Please check connection.3"))
    
    retry_click(driver, By.XPATH, "/html/body/nav[1]/div/button[2]")
    searchField = retry_find_element(driver, By.XPATH, "/html/body/div[10]/div[2]/div[4]/div/div/div/div[1]/div/div/form/input", target="search field", log_callback=log_callback)
    if searchField == None:
        retry_click(driver, By.XPATH, "/html/body/nav[1]/div/button[2]")
        searchField = retry_find_element(driver, By.XPATH, "/html/body/div[10]/div[2]/div[4]/div/div/div/div[1]/div/div/form/input", target="search field", log_callback=log_callback)
        if searchField == None:
            if log_callback:
                log_callback("Failed to find search field\n")
            return None
        
    retry_clear(searchField,By.XPATH, "/html/body/div[10]/div[2]/div[4]/div/div/div/div[1]/div/div/form/input", log_callback=log_callback)
    retry_send_keys(driver, By.XPATH, "/html/body/div[10]/div[2]/div[4]/div/div/div/div[1]/div/div/form/input", name, log_callback=log_callback)

    try:
        WebDriverWait(driver, 5).until(EC.url_changes(driver.current_url))
    except:
        if log_callback:
            log_callback("Seaching for " + name + " timed out1\n")
        return None
    
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[1]/div/div[1]/a/span/img")))
    except:
        if log_callback:
            log_callback("Seaching for " + name + " timed out2\n")
        return None
    
    result = retry_find_element(driver, By.XPATH, "/html/body/div[4]/div/div/div/div[1]/div/div[1]/a/span/img", log_callback=log_callback)
    if result == None:
        return None
    
    retry_click(driver, By.XPATH, "/html/body/div[4]/div/div/div/div[1]/div/div[1]/a/span/img")

    if "hd" in driver.current_url:
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div[2]/div[1]/div/div/table/tbody/tr[1]/td[2]/div/ul/li/a")))
        except:
            if log_callback:
                log_callback("Seaching for " + name + " timed out4\n")
            return None
    
        starring = retry_find_element(driver, By.XPATH, "/html/body/div[4]/div/div/div[2]/div[1]/div/div/table/tbody/tr[1]/td[2]/div/ul/li/a", target= "starring", log_callback=log_callback)
        if starring == None:
            return None
        retry_click(starring, By.XPATH, "/html/body/div[4]/div/div/div[2]/div[1]/div/div/table/tbody/tr[1]/td[2]/div/ul/li/a")

    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/div/div[2]")))
    except:
        if log_callback:
            log_callback("Seaching for " + name + " timed out5\n")
        return None
    
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
        if len(altname) > 1:
            altname = altname[1] + " " + altname[0]
        else:
            altname = altname[0]
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
    actors = {}
    for root, dirs, files in os.walk(dir):
        for file in files:
            if nfoFormat in file:
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    match = re.findall(r'<name>.*?</name>', f.read(), flags = re.UNICODE)
                    if match:
                        if match == ['<name></name>']:
                            if log_callback != None:
                                loc = os.path.join(root, file)
                                log_callback(f"No actor name found in {loc}\n", "orange")
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
                            loc = os.path.join(root, file)
                            log_callback(f"No actor name found in {loc}\n", "orange")
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
            endmatch = re.search(r'</movie>', data, flags=re.UNICODE)
            if match:
                for matchactor in match:
                    if actor in matchactor:
                        match = matchactor
                altnames = ""
                tags = ""
                for name in names:
                    altnames += f'\t\t<altname>{name}</altname>\n'
                    if endmatch:
                        tags += f'\t<tag>{name}</tag>\n'
                new_actor_data = f'<actor>\n\t\t<name>{primaryName}</name>\n{altnames}\n\t\t<tmdbid>{primaryName}</tmdbid>\n\t\t<role>Actress</role>\n\t\t<type>Actor</type>\n\t</actor>'
                tags = tags.rstrip('\n')
                data = re.sub(re.escape(match), new_actor_data, data, flags=re.UNICODE | re.DOTALL)
                data = re.sub(r'</movie>', f'{tags}\n</movie>', data, flags=re.UNICODE)

        data = "\n".join([line for line in data.splitlines() if line.strip() != ""])
        unique_lines = set()
        filtered_data = []
        for line in data.splitlines():
            if '<tag>' in line:
                if line not in unique_lines:
                    unique_lines.add(line)
                    filtered_data.append(line)
            else:
                filtered_data.append(line)
        data = "\n".join(filtered_data)

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