from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import time
import json

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
    return False

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
    return False

def waitVisible(driver, by, value, retries=3, delay=1, log_callback=None):
    for _ in range(retries):
        try:
            WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except Exception as e:
            if log_callback:
                log_callback(f"Wating element visible...\n")
            time.sleep(delay)
    return False

def waitURLChange(driver, url = None, retries=3, delay=1, log_callback=None):
    if not url:
        url = driver.current_url
    for _ in range(retries):
        try:
            WebDriverWait(driver, 3).until(EC.url_changes(url))
            return True
        except Exception as e:
            if log_callback:
                log_callback(f"Waiting url change...\n")
            time.sleep(delay)
    return False

def waitDomReady(driver, retries=3, delay=1, log_callback=None):
    for _ in range(retries):
        try:
            WebDriverWait(driver, 5).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            return True
        except Exception as e:
            if log_callback:
                log_callback(f"Waiting dom ready...\n")
            time.sleep(delay)
    return False


def startFirefox(url, log_callback=None, isheadless=False):
    if log_callback:
        log_callback(f"Starting browser: {url}\n")
    if isheadless:
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.set_preference("dom.webdriver.enabled", True)
        options.set_preference("useAutomationExtension", True)
        driver = webdriver.Firefox(options = options)
    else:
        driver = webdriver.Firefox()
        driver.get(url)
        waitDomReady(driver, log_callback=log_callback)
    return driver

def gotoURL(driver, url, log_callback=None):
    if log_callback:
        log_callback(f"Going to: {url}\n")
    driver.get(url)
    waitDomReady(driver, log_callback=log_callback)
    return True

def readJson(filename):
    try:
        with open(filename, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def writeJson(data, filename):
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def formatnameJson(data):
    for name, aliases in list(data.items()):
        for alias in aliases:
            if alias not in data:
                data[alias] = aliases
    return data
