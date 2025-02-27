import os
import re
from datetime import date, datetime
import requests
from selenium.webdriver.common.by import By
import util as ut

#------------------------------------------------------------
# Scrape javguru for a single item's metadata
#------------------------------------------------------------
def processSearchJavguru(driver, banngo, OGfile, cached_NFO, log_callback=None):
    if log_callback:
        log_callback(f"Searching for: {OGfile} on javguru\n")
    else:
        print(f"Searching for: {OGfile} on javguru\n")
    
    if banngo in cached_NFO:# check if the item is already in the json, return stored data if it is
        if log_callback:
            log_callback(f"{OGfile} in cache.\n")
        else:
            print(f"{OGfile} in cache.\n")
        return cached_NFO[banngo]

    wait = ut.waitVisible(driver, By.ID, "searchm", log_callback=log_callback)# wait page load
    if not wait:
        if log_callback:
            log_callback(f"Search for {OGfile} timed out.\n")
        else:
            print(f"Search for {OGfile} timed out.\n")
        return None

    searchField = ut.retry_find_element(driver, By.ID, "searchm", target= "search field",log_callback=log_callback)

    current_url = driver.current_url
    driver.execute_script("arguments[0].scrollIntoView();", searchField)
    ut.retry_clear(driver, By.ID, "searchm", log_callback=log_callback)
    ut.retry_send_keys(driver, By.ID, "searchm", banngo, log_callback=log_callback)# search for the item
    wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)

    if not wait:# redundant retry. sometimes the first click won't go through
        ut.retry_clear(driver, By.ID, "searchm", log_callback=log_callback)
        ut.retry_send_keys(driver, By.ID, "searchm", banngo, log_callback=log_callback)
        wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
        if not wait:
            if log_callback:
                log_callback(f"Search for {OGfile} timed out.\n")
            else:
                print(f"Search for {OGfile} timed out.\n")
            return None
    
    try:# check if there are no search results. This has to be done separately because the HTML stucture is different
        checkresults = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/main/div/div/div")[0].get_attribute("innerHTML")
        if "nothing good matched." in checkresults:
            if log_callback:
                log_callback(f"JavGuru: No search results found for {OGfile}.\n")
            else:
                print(f"JavGuru: No search results found for {OGfile}.\n")
            return None
    except:
        pass

    wait = ut.waitVisible(driver, By.CLASS_NAME, "imgg", log_callback=log_callback)# wait for search results to load
    if not wait:
        if log_callback:
            log_callback(f"Search for {OGfile} timed out.\n")
        else:
            print(f"Search for {OGfile} timed out.\n")
        return None

    searchresults = ut.retry_find_element(driver, By.CLASS_NAME, "imgg", target = "search result",log_callback=log_callback)
    if searchresults is None:
        if log_callback:
            log_callback("No search results found for " + OGfile + "\n")
        else:
            print("No search results found for " + OGfile + "\n")
        return None
    
    first_result = ut.retry_find_element(driver, By.XPATH, '//*[@id="main"]/div[1]/div/div/div[2]/h2/a', target="first result", log_callback=log_callback).text
    temp = first_result.replace('-', '').lower()# check if the search result matches the item we are looking for. case insensitive and remove hyphens
    nodashbanngo = banngo.replace('-', '').lower()
    if nodashbanngo not in temp:
        if log_callback:
            log_callback(f"Search result {first_result} does not match {banngo}\n")
        else:
            print(f"Search result {first_result} does not match {banngo}\n")
        return None

    current_url = driver.current_url
    driver.execute_script("arguments[0].scrollIntoView();", searchresults)
    ut.retry_click(driver, By.CLASS_NAME, "imgg", log_callback=log_callback)# click on the search result
    wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
    if not wait:
        driver.execute_script("arguments[0].scrollIntoView();", searchresults)
        ut.retry_click(driver, By.CLASS_NAME, "imgg", log_callback=log_callback)
        wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
        if not wait:
            if log_callback:
                log_callback(f"Failed to click on search result for {OGfile}\n")
            else:
                print(f"Failed to click on search result for {OGfile}\n")
            return None

    wait = ut.waitVisible(driver, By.CLASS_NAME, "titl", log_callback=log_callback)
    if not wait:
        if log_callback:
            log_callback(f"Failed to open page for {banngo}\n")
        else:
            print(f"Failed to open page for {banngo}\n")
        return None

    if log_callback:
        log_callback("getting metadata on " + banngo + "\n")
    else:
        print("getting metadata on " + banngo + "\n")

    title = ut.retry_find_element(driver, By.CLASS_NAME, "titl", target= "title", log_callback=log_callback)
    metadata = ut.retry_find_element(driver, By.CLASS_NAME, "infoleft", target="metadata", log_callback=log_callback)
    cover = ut.retry_find_element(driver, By.CLASS_NAME, "large-screenimg", target="cover", log_callback=log_callback)
    img_element = cover.find_element(By.TAG_NAME, "img")
    img_src = img_element.get_attribute('src')

    info = {
        "title": title.text,
        "metadata": metadata.text,
        "cover": img_src,
        "OGfilename": OGfile
    }

    data = parseInfoJavguru(info, log_callback=log_callback)

    cached_NFO[banngo] = data

    return data

#------------------------------------------------------------
# Scrape javtrailers for a single item's metadata
#------------------------------------------------------------
def processSearchJavtrailers(driver, banngo, OGfile, cached_NFO, log_callback=None):
    if log_callback:
        log_callback(f"Searching for: {OGfile} on javtrailers\n")
    else:
        print(f"Searching for: {OGfile} on javtrailers\n")
    
    if banngo in cached_NFO:# check if the item is already in the json, return stored data if it is
        if log_callback:
            log_callback(f"{OGfile} in cache.\n")
        else:
            print(f"{OGfile} in cache.\n")
        return cached_NFO[banngo]
    
    wait = ut.waitVisible(driver, By.ID, "searchBox", log_callback=log_callback)
    if not wait:
        if log_callback:
            log_callback(f"Search for {OGfile} timed out.\n")
        else:
            print(f"Search for {OGfile} timed out.\n")
        return None
    
    searchField = ut.retry_find_element(driver, By.ID, "searchBox", target= "search field",log_callback=log_callback)
    current_url = driver.current_url
    driver.execute_script("arguments[0].scrollIntoView();", searchField)
    ut.retry_clear(driver, By.ID, "searchBox", log_callback=log_callback)
    ut.retry_send_keys(driver, By.ID, "searchBox", banngo, log_callback=log_callback)# search for the item
    wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
    if not wait:
        ut.retry_clear(driver, By.ID, "searchBox", log_callback=log_callback)
        ut.retry_send_keys(driver, By.ID, "searchBox", banngo, log_callback=log_callback)
        wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
        if not wait:
            if log_callback:
                log_callback(f"Search for {OGfile} timed out.\n")
            else:
                print(f"Search for {OGfile} timed out.\n")
            return None
        
    wait = ut.waitVisible(driver, By.XPATH, '//*[@id="search"]', log_callback=log_callback)
    if not wait:
        if log_callback:
            log_callback(f"Search for {OGfile} timed out.\n")
        else:
            print(f"Search for {OGfile} timed out.\n")
        return None
    
    searchresults = ut.retry_find_element(driver, By.XPATH, '//*[@id="search"]', target = "search result",log_callback=log_callback)
    if searchresults is None:
        if log_callback:
            log_callback("No search results found for " + OGfile + "\n")
        else:
            print("No search results found for " + OGfile + "\n")
        return None
    
    try:
        driver.refresh()# javtrailer site has a bug where the search results are not loaded properly. This is a workaround
        checkresults = None
        checkresults = driver.find_elements(By.XPATH, '//*[@id="search"]')[0].get_attribute("innerHTML")
        if "No videos available" in checkresults:
            if log_callback:
                log_callback(f"JavTrailers: No search results found for {OGfile}.\n")
            else:
                print(f"JavTrailers: No search results found for {OGfile}.\n")
            return None
    except:
        pass

    first_result = ut.retry_find_element(driver, By.XPATH, '//*[@id="search"]/div/section/div/div[1]/div/a/div/div[2]/div/p', target="first result", log_callback=log_callback)
    text = first_result.text.replace('-', '').lower()
    temp = banngo.replace('-', '').lower()
    if temp not in text:
        if log_callback:
            log_callback(f"Search result {text} does not match {banngo}\n")
        else:
            print(f"Search result {text} does not match {banngo}\n")
        return None

    current_url = driver.current_url
    driver.execute_script("arguments[0].scrollIntoView();", first_result)
    ut.retry_click(driver, By.XPATH, "/html/body/div[1]/div/div[2]/section/div/section/div/div[1]/div/a/div/div[2]/div/p", log_callback=log_callback)
    wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
    if not wait:
        driver.execute_script("arguments[0].scrollIntoView();", first_result)
        ut.retry_click(driver, By.XPATH, "/html/body/div[1]/div/div[2]/section/div/section/div/div[1]/div/a/div/div[2]/div/p", log_callback=log_callback)
        wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
        if not wait:
            if log_callback:
                log_callback(f"Failed to click on search result for {OGfile}\n")
            else:
                print(f"Failed to click on search result for {OGfile}\n")
            return None
    
    wait = ut.waitVisible(driver, By.XPATH, "/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[3]", log_callback=log_callback)
    if not wait:
        if log_callback:
            log_callback(f"Failed to open page for {banngo}\n")
        else:
            print(f"Failed to open page for {banngo}\n")
        return None
    
    if log_callback:
        log_callback("getting metadata on " + banngo + "\n")
    else:
        print("getting metadata on " + banngo + "\n")

    title = ut.retry_find_element(driver, By.XPATH, "/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[3]/h1", target= "title", log_callback=log_callback)
    metadatas = ut.retry_find_element(driver, By.XPATH, "/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[3]/div[1]",target = 'metadata', log_callback=log_callback)
    cover = ut.retry_find_element(driver, By.XPATH, "/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[3]/div[2]/img", target="cover", log_callback=log_callback)
    img_src = cover.get_attribute('data-src')

    info = {
        "title": title.text if title else "Unknown",
        "metadata": metadatas.get_attribute('innerHTML'),
        "cover": img_src,
        "OGfilename": OGfile
    }

    data = parseInfoJavtrailers(info, log_callback=log_callback)

    cached_NFO[banngo] = data

    return data

#------------------------------------------------------------
# Create NFO file
#------------------------------------------------------------
def createNFO(path, metadata, log_callback=None):
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

#------------------------------------------------------------
# Find AV files in directory
#------------------------------------------------------------
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

#------------------------------------------------------------
# Download image
#------------------------------------------------------------
def downloadImage(banngo, url, path, log_callback=None):
    if log_callback:
        log_callback("Downloading image for " + banngo + "\n")
    else:
        print("Downloading image for " + banngo + "\n")
    try:
        response = requests.get(url, timeout=10)
        path = path + '/folder.jpg'
        with open(path, 'wb') as f:
            f.write(response.content)
    except:
        pass

#------------------------------------------------------------
# Parse metadata specific to javguru
#------------------------------------------------------------
def parseInfoJavguru(info, log_callback=None):
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

#------------------------------------------------------------
# Parse metadata specific to javtrailers
#------------------------------------------------------------
def parseInfoJavtrailers(info, log_callback=None):
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

#------------------------------------------------------------
# Create folder structure for the item
#------------------------------------------------------------
def manageFileStucture(dir, metadata, log_callback=None, update_callback=None):
    if log_callback:
        log_callback("Creating folder for " + metadata['Code'] + "\n")
    else:
        print("Creating folder for " + metadata['Code'] + "\n")

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
