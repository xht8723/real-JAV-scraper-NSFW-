import time
import json
from seleniumbase import Driver
import os
import re
import shutil
from datetime import date, datetime

def cdp_open_url(driver, url, log_callback=None):
    """
    Opens a URL in a new tab using CDP mode.
    
    :param driver: The Seleniumbase WebDriver instance.
    :param url: The URL to open.
    :param log_callback: Optional callback function for logging messages.
    """
    if log_callback:
        log_callback(f"Opening URL: {url}\n")
    driver.cdp.open_new_tab(url)

def cdp_close_tab(driver, log_callback=None):
    """
    Closes the current tab using CDP mode.
    
    :param driver: The Seleniumbase WebDriver instance.
    :param log_callback: Optional callback function for logging messages.
    """
    if log_callback:
        log_callback("Closing current tab.\n")
    driver.cdp.close_active_tab()

def cdp_close_ad_tab(driver, log_callback=None):
    """
    Closes the current tab if it is an advertisement tab.
    
    :param driver: The Seleniumbase WebDriver instance.
    :param log_callback: Optional callback function for logging messages.
    """
    if log_callback:
        log_callback("Closing ad tab if present.\n")
    try:
        tabs = driver.cdp.get_tabs()
        while len(tabs) > 1:
            driver.cdp.switch_to_tab(len(tabs) - 1)  # Switch to the last tab
            driver.cdp.close_active_tab()            # Close the last tab
            tabs = driver.cdp.get_tabs()             # Refresh the tabs list
        driver.cdp.switch_to_tab(0)
        return
    except Exception as e:
        if log_callback:
            log_callback(f"Failed to close ad tab: {e}\n")

def cdp_find_element(driver, cssSelector, retries=3, delay=1, log_callback=None):
    """
    Attempts to find an element on the page, retrying if necessary.
    
    :param driver: The Seleniumbase WebDriver instance.
    :param cssSelector: css style selector to locate the element.
    :param retries: Number of retries if the element is not found.
    :param delay: Delay between retries in seconds.
    :param log_callback: Optional callback function for logging messages.
    :return: The found element or None if not found after retries.
    """
    for _ in range(retries):
        try:
            # Wait for the element to be visible (this will block until visible or timeout)
            driver.cdp.wait_for_element_visible(cssSelector, timeout=5)
            # Now check presence and visibility
            isPresent = driver.cdp.is_element_present(cssSelector)
            isVisible = driver.cdp.is_element_visible(cssSelector)
            driver.cdp.assert_element_visible(cssSelector, timeout=5)
            if isPresent and isVisible:
                driver.cdp.assert_element_visible(cssSelector, timeout=5)
                element = driver.cdp.find_element(cssSelector, timeout=5)
                return element
        except Exception as e:
            if log_callback:
                log_callback(f"Retrying find element {cssSelector}...\n")
            time.sleep(delay)
    return None

def cdp_type(driver, cssSelector, text, log_callback=None):
    """
    Types text into an input field identified by a CSS selector.
    
    :param driver: The Selenium WebDriver instance.
    :param cssSelector: The CSS selector for the input field.
    :param text: The text to type into the input field.
    :param log_callback: Optional callback function for logging messages.
    """
    if log_callback:
        log_callback(f"Typing into {cssSelector}: {text}\n")
    element = cdp_find_element(driver, cssSelector, retries=3, delay=1, log_callback=log_callback)
    if element:
        driver.cdp.type(cssSelector, text)

def cdp_press_keys(driver, cssSelector, keys, log_callback=None):
    """
    Presses keys on an input field identified by a CSS selector.
    
    :param driver: The Selenium WebDriver instance.
    :param cssSelector: The CSS selector for the input field.
    :param keys: The keys to press.
    :param log_callback: Optional callback function for logging messages.
    """
    if log_callback:
        log_callback(f"Pressing enter on {cssSelector}\n")
    element = cdp_find_element(driver, cssSelector, retries=3, delay=1, log_callback=log_callback)
    if element:
        driver.cdp.press_keys(cssSelector, keys)

def cdp_clear(driver, cssSelector, log_callback=None):
    """
    Clears the text in an input field identified by a CSS selector.
    
    :param driver: The Selenium WebDriver instance.
    :param cssSelector: The CSS selector for the input field.
    :param log_callback: Optional callback function for logging messages.
    """
    if log_callback:
        log_callback(f"Clearing text in {cssSelector}\n")
    element = cdp_find_element(driver, cssSelector, retries=3, delay=1, log_callback=log_callback)
    if element:
        element.clear_input()

def cdp_scroll_to_element(driver, cssSelector, log_callback=None):
    """
    Scrolls the page to bring the element identified by a CSS selector into view.
    
    :param driver: The Selenium WebDriver instance.
    :param cssSelector: The CSS selector for the element to scroll to.
    :param log_callback: Optional callback function for logging messages.
    """
    if log_callback:
        log_callback(f"Scrolling to {cssSelector}\n")
    element = cdp_find_element(driver, cssSelector, retries=3, delay=1, log_callback=log_callback)
    if element:
        driver.cdp.scroll_into_view(cssSelector)

def cdp_click(driver, cssSelector, log_callback=None):
    """
    Clicks on an element identified by a CSS selector.
    
    :param driver: The Selenium WebDriver instance.
    :param cssSelector: The CSS selector for the element to click.
    :param log_callback: Optional callback function for logging messages.
    """
    if log_callback:
        log_callback(f"Clicking on {cssSelector}\n")
    element = cdp_find_element(driver, cssSelector, retries=3, delay=1, log_callback=log_callback)
    if element:
        driver.cdp.click(cssSelector)

def cdp_element_click(driver, cssSelector, log_callback=None):
    """
    Clicks on an element identified by a CSS selector using the CDP.
    
    :param driver: The Selenium WebDriver instance.
    :param cssSelector: The CSS selector for the element to click.
    :param log_callback: Optional callback function for logging messages.
    """
    if log_callback:
        log_callback(f"Clicking on {cssSelector}\n")
    element = cdp_find_element(driver, cssSelector, retries=3, delay=1, log_callback=log_callback)
    if element:
        element.mouse_click()

def startChrome(url, log_callback=None, isheadless=False):
    """
    Starts a Chrome browser instance and activates CDP mode for the specified URL.

    :param url: The URL to navigate to.
    :param log_callback: Optional callback function for logging messages.
    :param isheadless: Boolean indicating whether to run the browser in headless mode.
    :return: The Selenium WebDriver instance.
    """
    if log_callback:
        log_callback(f"Starting browser: {url}\n")
    driver = Driver(browser="chrome", headless=isheadless, uc=True)
    driver.uc_activate_cdp_mode(url)
    return driver

def cdp_gotoURL(driver, url, log_callback=None):
    """
    Navigates the browser to the specified URL using CDP.

    :param driver: The Selenium WebDriver instance.
    :param url: The URL to navigate to.
    :param log_callback: Optional callback function for logging messages.
    :return: True if navigation was successful, False otherwise.
    """
    if log_callback:
        log_callback(f"Going to: {url}\n")
    driver.cdp.get(url)
    return True

def readJson(filename):
    """
    Reads a JSON file and returns its content as a dictionary.

    :param filename: The path to the JSON file.
    :return: A dictionary containing the JSON data, or an empty dictionary if the file does not exist.
    """
    try:
        with open(filename, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def writeJson(data, filename):
    """
    Writes a dictionary to a JSON file.

    :param data: The dictionary to write to the file.
    :param filename: The path to the JSON file.
    """
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def formatnameJson(data):
    """
    Formats a JSON dictionary by ensuring that each alias is also a key in the dictionary.

    :param data: The dictionary to format.
    :return: The formatted dictionary with aliases as keys.
    """
    for name, aliases in list(data.items()):
        for alias in aliases:
            if alias not in data:
                data[alias] = aliases
    return data

def check_cache(banngo, cached_NFO, OGfile, log_callback=None):
    """
    Checks if the given item is already in the cached NFO data.

    :param banngo: The key to check in the cached NFO data.
    :param cached_NFO: The cached NFO data as a dictionary.
    :return: The cached data if the item is found, otherwise None.
    """
    if banngo in cached_NFO:# check if the item is already in the json, return stored data if it is
        if log_callback:
            log_callback(f"{OGfile} in cache.\n")
        return cached_NFO[banngo]
    return None
    
def createNFO(path, metadata, log_callback=None):
    """
    Creates an NFO file for the given metadata in the specified path.

    :param path: The directory where the NFO file will be created.
    :param metadata: A dictionary containing the metadata for the NFO file.
    :param log_callback: Optional callback function for logging messages.
    """

    if log_callback:
        log_callback("Creating NFO for " + metadata['Code'] + "\n")
    else:
        print("Creating NFO for " + metadata['Code'] + "\n")

    path = os.path.join(path, "movie.nfo") 
    with open(path, 'w+', encoding = 'utf-8') as f:
        f.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
        f.write('<movie>\n')
        f.write('\t<dateadded>' + str(date.today()) + ' ' + str(datetime.now()) + '</dateadded>\n')
        f.write('\t<title>' + f"[{metadata['Code']}] " + metadata['Title'] + '</title>\n')
        f.write('\t<year>' + metadata['Release Date'].split('-')[0] + '</year>\n')
        f.write('\t<mpaa>XXX</mpaa>\n')
        f.write('\t<tmdbid>' + metadata['Code'] + '</tmdbid>\n')
        f.write('\t<premiered>' + metadata['Release Date'] + '</premiered>\n')
        f.write('\t<releasedate>' + metadata['Release Date'] + '</releasedate>\n')
        for eachtag in metadata['Tags']:
            f.write('\t<genre>' + eachtag + '</genre>\n')
        f.write('\t<studio>' + metadata['Label'] + '</studio>\n')
        f.write('\t<art>\n')
        f.write('\t\t<poster>' + metadata['Image'] + '</poster>\n')
        f.write('\t\t<fanart>' + metadata['Image'] + '</fanart>\n')
        f.write('\t</art>\n')
        for eachAct in metadata['Actress']:
            f.write('\t<actor>\n')
            f.write('\t\t<name>' + eachAct + '</name>\n')
            f.write('\t\t<role>Actress</role>\n')
            f.write('\t\t<type>Actor</type>\n')
            f.write('\t</actor>\n')
        f.write('\t<set>' + metadata["Studio"] + '</set>\n')
        f.write('\t<thumb>' + metadata['Image'] + '</thumb>\n')
        f.write('</movie>')


def findAVIn(directory, log_callback=None, update_callback=None):
    """
    Scans the specified directory for video files and extracts the banngo code from their filenames.

    :param directory: The directory to scan for video files.
    :param log_callback: Optional callback function for logging messages.
    :param update_callback: Optional callback function to update the status of each file.
    :return: A tuple containing a list of banngo codes and a dictionary mapping banngo codes to filenames.
    """
    file_format = [
    '.mp4',
    '.MP4',
    '.mkv',
    '.rmvb',
    '.AVI',
    '.avi'
    ]
    if log_callback:
        log_callback(f"Scanning directory: {directory}\n")
    else:
        print(f"Scanning directory: {directory}\n")
    file_list = os.listdir(directory)
    pattern = re.compile(r'([a-zA-Z]+\d*?-\d+[a-zA-Z]?)')
    pending_BanngoList = []
    pending_fileList = {}
    for file in file_list:
        filename, file_extension = os.path.splitext(file)
        if file_extension in file_format:
            match = pattern.findall(filename)
            if match:
                banngo = match[0].upper()
                pending_BanngoList.append(banngo)
                pending_fileList[banngo] = file
                if log_callback:
                    log_callback("Found " + banngo + "\n")
                else:
                    print("Found " + banngo + "\n")
                if update_callback:
                    update_callback(file, "")
            else:
                if log_callback:
                    log_callback(f"skipped {file}\n")
                else:
                    print(f"skipped {file}\n")
    return pending_BanngoList, pending_fileList


def cdp_downloadImage(url, driver, banngo, path, log_callback=None):
    """
    Screenshot the target element(an image) from the specified element and saves it to the given path using cdp.

    :param element: The Selenium WebDriver element containing the image.
    :param banngo: The banngo code used to name the image file.
    :param path: The directory where the image will be saved.
    :param log_callback: Optional callback function for logging messages.
    :return: None if the download was successful, or None if an error occurred.
    """
    from seleniumbase import SB
    if log_callback:
        log_callback("Downloading image for " + banngo + "\n")
    else:
        print("Downloading image for " + banngo + "\n")
    try:
        if not os.path.exists(path):
            os.makedirs(path)

        with SB(browser="chrome", uc=True) as sb:
            sb.download_file(url, path)
            sb.assert_downloaded_file(path, timeout=10)

        downloaded_file = os.path.join(path, url.split('/')[-1])
        filename = os.path.join(path, f'{banngo.upper()}.jpg')
        os.rename(downloaded_file, filename)
        return 
    
    except Exception as e:
        error_type = type(e).__name__
        if log_callback:
            log_callback(f"Failed to download image for {banngo}: [{error_type}] {e}\n")
        else:
            print(f"Failed to download image for {banngo}: [{error_type}] {e}\n")
        return None
    
def cdp_screenshotElement(driver, url, path, banngo, log_callback=None):
    """
    Takes a screenshot of the specified element and saves it to the given path.

    :param element: The Selenium WebDriver element to screenshot.
    :param path: The directory where the screenshot will be saved.
    :param banngo: The banngo code used to name the screenshot file.
    :param log_callback: Optional callback function for logging messages.
    :return: None if the screenshot was successful, or None if an error occurred.
    """
    if log_callback:
        log_callback("Taking screenshot for " + banngo + "\n")
    else:
        print("Taking screenshot for " + banngo + "\n")
    
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        filename = os.path.join(path, f'{banngo.upper()}.jpg')
        if os.path.exists(filename):
            if log_callback:
                log_callback(f"Screenshot for {banngo} already exists, skipping.\n")
            else:
                print(f"Screenshot for {banngo} already exists, skipping.\n")
            return filename
        
        cdp_open_url(driver, url, log_callback=log_callback)
        pic = cdp_find_element(driver, 'img', log_callback=log_callback)
        pic.save_screenshot(filename)
        if log_callback:
            log_callback(f"Screenshot saved as {filename}\n")
        else:
            print(f"Screenshot saved as {filename}\n")
        cdp_close_tab(driver, log_callback=log_callback)
        driver.cdp.switch_to_tab(0)  # Switch back to the original tab
        return filename
    except Exception as e:
        error_type = type(e).__name__
        if log_callback:
            log_callback(f"Failed to take screenshot for {banngo}: [{error_type}] {e}\n")
        else:
            print(f"Failed to take screenshot for {banngo}: [{error_type}] {e}\n")
        return None

def parseInfoJavguru(info, log_callback=None):
    """
    Parses metadata from a Javguru info dictionary.

    :param info: A dictionary containing the metadata information.
    :param log_callback: Optional callback function for logging messages.
    :return: A dictionary containing the parsed movie information.
    """

    pattern = re.compile(r'\[([a-zA-Z]+\d*?-\d+[a-zA-Z]?)\]')
    title = re.sub(pattern, '', info['title']).strip()
    metadata = info['metadata'].replace('Movie Information:', '')
    cover = info['cover']
    OGfilename = info['OGfilename']
    movie_info = {}
    movie_info['Title'] = title
    movie_info['Image'] = cover
    movie_info['OGfilename'] = OGfilename

    # List of known keys in the order they appear
    keys = [
        "Code", "Release Date", "Category", "Studio", "Label",
        "Tags", "Series", "Actor", "Actress"
    ]
    # Build a regex pattern to match only these keys
    pattern = r'(' + '|'.join(re.escape(k) for k in keys) + r'):'
    matches = list(re.finditer(pattern, metadata))
    for i, match in enumerate(matches):
        key = match.group(1)
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(metadata)
        value = metadata[start:end].strip()
        # Handle fields that are lists
        if key in ["Category", "Tags", "Actor", "Actress"]:
            value = [v.strip() for v in value.split(',') if v.strip()]
        movie_info[key] = value

    if 'Tags' not in movie_info:
        movie_info['Tags'] = [""]
    
    if 'Actress' not in movie_info:
        movie_info['Actress'] = ["Unknown"]

    if 'Studio' not in movie_info:
        movie_info['Studio'] = "Unknown"

    if 'Release Date' not in movie_info:
        movie_info['Release Date'] = "Unknown"

    return movie_info

def parseInfoJavtrailers(info, log_callback=None):
    """
    Parses metadata from a Javtrailers info dictionary.

    :param info: A dictionary containing the metadata information.
    :param log_callback: Optional callback function for logging messages.
    :return: A dictionary containing the parsed movie information.
    """

    html = info['metadata']
    pattern = re.compile(r'\[([a-zA-Z]+\d*?-\d+[a-zA-Z]?)\]')
    title = re.sub(pattern, '', info['title']).strip()
    cover = info['cover']
    OGfilename = info['OGfilename']
    DID_id = re.search(r'DVD ID:</span>\s*(.*?)\s*</p>', html)
    release_date = re.search(r'Release Date:</span>\s*(.*?)</p>', html)
    studio = re.search(r'/studios/.*?" class="badge bg-light text-dark mr-2 badge-link">(.*?)</a>', html)
    tags = re.findall(r'/categories/.*?" class="badge bg-light text-dark badge-link">(.*?)</a>', html)
    actress = re.findall(r'/casts/.*?" class="badge bg-light text-dark mr-2 badge-link">(.*?)</a>', html)
    
    if release_date:
        release_date = datetime.strptime(release_date.group(1), '%d %b %Y').strftime('%Y-%m-%d')
    else:
        release_date = "Unknown"

    if actress:
        actress = [re.sub(r'[^\x00-\x7F]+', '', act) for act in actress]# remove japanese characters
        actress = [act.strip() for act in actress]
    else:
        actress = ["Unknown"]

    if DID_id:
        DID_id = DID_id.group(1)
    else:
        DID_id = "Unknown"

    if studio:
        studio = studio.group(1)
    else:
        studio = "Unknown"
    
    if not tags:
        tags = [""]

    movie_info = {}
    movie_info['Title'] = title
    movie_info['Image'] = cover
    movie_info['OGfilename'] = OGfilename
    movie_info['Code'] = DID_id
    movie_info['Release Date'] = release_date
    movie_info['Studio'] = studio
    movie_info['Tags'] = tags
    movie_info['Actress'] = actress
    movie_info['Label'] = studio

    return movie_info

def manageFileStucture(dir, renameType, metadata, log_callback=None, update_callback=None):
    """
    Creates a folder structure for the given metadata and moves the file to the new folder.

    :param dir: The directory where the file is currently located.
    :param renameType: Boolean indicating whether to rename the folder based on the code only.
    :param metadata: A dictionary containing the metadata for the file.
    :param log_callback: Optional callback function for logging messages.
    :param update_callback: Optional callback function to update the status of the file.
    :return: None
    """
    if log_callback:
        log_callback("Creating folder for " + metadata['Code'] + "\n")
    else:
        print("Creating folder for " + metadata['Code'] + "\n")

    if renameType:
        folder_name = metadata["Code"]
    else:
        title = metadata["Title"]
        if len(title) > 180:
            title = title.split(',')[0]  # Truncate title if too long
            if len(title) > 180:
                title = title[:180]
        folder_name = metadata["Code"] + ' [' + metadata['Studio'] + '] - ' + title + ' (' + metadata['Release Date'].split('-')[0] + ')'

    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        folder_name = folder_name.replace(char, '-')

    abspath = os.path.join(dir, folder_name)
    if not os.path.exists(abspath):
        os.makedirs(abspath)

    extension = os.path.splitext(metadata["OGfilename"])[1]
    os.rename(os.path.join(dir, metadata["OGfilename"]), abspath + '/' + metadata["Code"] + extension)
    if os.path.exists("img_cache"):
        img_cache_dir = os.path.abspath("img_cache")
        try:
            shutil.copyfile(
                os.path.join(img_cache_dir, f'{metadata["Code"]}.jpg'),
                os.path.join(abspath, 'folder.jpg')
            ) 
        except FileNotFoundError:
            if log_callback:
                log_callback(f"Cover image for {metadata['Code']} not found in img_cache.\n")
            else:
                print(f"Cover image for {metadata['Code']} not found in img_cache.\n")

    createNFO(abspath, metadata, log_callback=log_callback)

    if update_callback:
        update_callback(metadata['OGfilename'], folder_name)
    return
