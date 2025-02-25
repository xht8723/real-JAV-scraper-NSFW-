from selenium.webdriver.common.by import By
import os
import re
import util as ut
from datetime import date, datetime
import requests

def processSearch(driver, banngoTuple, cached_NFO, log_callback=None):
    banngoList, fileList = banngoTuple
    infoList = []
    for eachAV in banngoList:
        if log_callback:
            log_callback(f"Searching for: {eachAV} \n")
        
        if eachAV in cached_NFO:
            if log_callback:
                log_callback(f"{eachAV} in cache.\n")
            infoList.append(cached_NFO[eachAV])
            continue

        wait = ut.waitVisible(driver, By.ID, "searchm", log_callback=log_callback)
        if not wait:
            if log_callback:
                log_callback(f"Search for {eachAV} timed out.\n")
            continue

        searchField = ut.retry_find_element(driver, By.ID, "searchm", target= "search field",log_callback=log_callback)

        current_url = driver.current_url
        driver.execute_script("arguments[0].scrollIntoView();", searchField)
        ut.retry_clear(driver, By.ID, "searchm", log_callback=log_callback)
        ut.retry_send_keys(driver, By.ID, "searchm", eachAV, log_callback=log_callback)
        wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
        if not wait:
            ut.retry_clear(driver, By.ID, "searchm", log_callback=log_callback)
            ut.retry_send_keys(driver, By.ID, "searchm", eachAV, log_callback=log_callback)
            wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
            if not wait:
                if log_callback:
                    log_callback(f"Search for {eachAV} timed out.\n")
                continue
        
        try:
            checkresults = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/main/div/div/div")[0].get_attribute("innerHTML")
            if "nothing good matched." in checkresults:
                if log_callback:
                    log_callback(f"No search results found for {eachAV}.\n")
                continue
        except:
            pass

        wait = ut.waitVisible(driver, By.CLASS_NAME, "imgg", log_callback=log_callback)
        if not wait:
            if log_callback:
                log_callback(f"Search for {eachAV} timed out.\n")
            continue

        searchresults = ut.retry_find_element(driver, By.CLASS_NAME, "imgg", target = "search result",log_callback=log_callback)
        if searchresults is None:
            if log_callback:
                log_callback("No search results found for " + eachAV + "\n")
            continue
        
        current_url = driver.current_url
        driver.execute_script("arguments[0].scrollIntoView();", searchresults)
        ut.retry_click(driver, By.CLASS_NAME, "imgg", log_callback=log_callback)
        wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
        if not wait:
            driver.execute_script("arguments[0].scrollIntoView();", searchresults)
            ut.retry_click(driver, By.CLASS_NAME, "imgg", log_callback=log_callback)
            wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
            if not wait:
                if log_callback:
                    log_callback(f"Failed to click on search result for {eachAV}\n")
                continue

        wait = ut.waitVisible(driver, By.CLASS_NAME, "titl", log_callback=log_callback)
        if not wait:
            if log_callback:
                log_callback(f"Failed to open page for {eachAV}\n")
            continue

        if log_callback:
            log_callback("getting metadata on " + eachAV + "\n")

        title = ut.retry_find_element(driver, By.CLASS_NAME, "titl", target= "title", log_callback=log_callback)
        metadata = ut.retry_find_element(driver, By.CLASS_NAME, "infoleft", target="metadata", log_callback=log_callback)
        cover = ut.retry_find_element(driver, By.CLASS_NAME, "large-screenimg", target="cover", log_callback=log_callback)
        img_element = cover.find_element(By.TAG_NAME, "img")
        img_src = img_element.get_attribute('src')

        info = {
            "title": title.text,
            "metadata": metadata.text,
            "cover": img_src,
            "OGfilename": fileList[eachAV]
        }

        infoList.append(info)
        cached_NFO[eachAV] = info
        
    driver.quit()
    return infoList


def createNFO(path, metadata, log_callback=None):
    if log_callback:
        log_callback("Creating NFO for " + metadata['Code'] + "\n")

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
    file_list = os.listdir(directory)
    pattern = re.compile(r'([a-zA-Z]+\d*?-\d+[a-zA-Z]?)')
    pending_BanngoList = []
    pending_fileList = {}
    for file in file_list:
        filename, format = os.path.splitext(file)
        if format in file_format:
            match = pattern.findall(filename)
            if match:
                banngo = match[0].upper()
                pending_BanngoList.append(banngo)
                pending_fileList[banngo] = file
                if log_callback:
                    log_callback("Found " + banngo + "\n")
                if update_callback:
                    update_callback(file, "")
            else:
                if log_callback:
                    log_callback(f"skipped {file}\n")
    return pending_BanngoList, pending_fileList


def downloadImage(banngo, url, path, log_callback=None):
    if log_callback:
        log_callback("Downloading image for " + banngo + "\n")
    try:
        response = requests.get(url)
        path = path + '/folder.jpg'
        with open(path, 'wb') as f:
            f.write(response.content)
    except:
        pass


def parseInfo(info, log_callback=None):
    pattern = re.compile(r'\[([a-zA-Z]+\d*?-\d+[a-zA-Z]?)\]')
    title = re.sub(pattern, '', info['title']).strip()
    metadata = info['metadata']
    cover = info['cover']
    OGfilename = info['OGfilename']
    movie_info = {}
    movie_info['Title'] = title
    movie_info['Image'] = cover
    movie_info['OGfilename'] = OGfilename

    lines = metadata.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            movie_info[key.strip()] = value.strip()

    if 'Tags' in movie_info:
        movie_info['Tags'] = [tag.strip() for tag in movie_info['Tags'].split(',')]
    
    if 'Actress' in movie_info:
        movie_info['Actress'] = [actress.strip() for actress in movie_info['Actress'].split(',')]
    else:
        movie_info['Actress'] = ["Unknown"]

    if 'Studio' not in movie_info:
        movie_info['Studio'] = "Unknown"

    if 'Release Date' not in movie_info:
        movie_info['Release Date'] = "Unknown"

    return movie_info

def manageFileStucture(dir, metadata, log_callback=None, update_callback=None):
    if log_callback:
        log_callback("Creating folder for " + metadata['Code'] + "\n")

    folder_name = metadata["Code"] + ' [' + metadata['Studio'] + '] - ' + metadata['Title'] + ' (' + metadata['Release Date'].split('-')[0] + ')'
    if (len(folder_name) > 200):
        folder_name = metadata["Code"] + ' [' + metadata['Studio'] + '] - ' + metadata['Title'][:150] + ' (' + metadata['Release Date'].split('-')[0] + ')'
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        folder_name = folder_name.replace(char, '_')

    abspath = os.path.join(dir, folder_name)
    if not os.path.exists(abspath):
        os.makedirs(abspath)

    os.rename(os.path.join(dir, metadata["OGfilename"]), abspath + '/' + metadata["OGfilename"])
    downloadImage(metadata['Code'], metadata['Image'], abspath, log_callback=log_callback)
    createNFO(abspath, metadata, log_callback=log_callback)

    if update_callback:
        update_callback(metadata['OGfilename'], folder_name)
    return
