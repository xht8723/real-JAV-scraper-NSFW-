import os
import util as ut

#------------------------------------------------------------
# Scrape javguru for a single item's metadata
#------------------------------------------------------------
def processSearchJavguru(driver, banngo, OGfile, cached_NFO = None, log_callback=None):
    if log_callback:
        log_callback(f"Searching for: {OGfile} on javguru\n")
    else:
        print(f"Searching for: {OGfile} on javguru\n")
    
    if cached_NFO:
        cache = ut.check_cache(banngo, cached_NFO, OGfile, log_callback=log_callback)# check if the item is already in the json, return stored data if it is
        if cache:
            return cache

    wait = ut.cdp_find_element(driver, "#searchm", log_callback=log_callback)
    if not wait:
        if log_callback:
            log_callback(f"Search for {OGfile} timed out.\n")
        else:
            print(f"Search for {OGfile} timed out.\n")
        return None

    ut.cdp_clear(driver, "#searchm", log_callback=log_callback)# clear the search field
    ut.cdp_type(driver, "#searchm", banngo, log_callback=log_callback)# search for the item
    ut.cdp_press_keys(driver, "#searchm", "\n", log_callback=log_callback)# press enter to 
    
    wait = ut.cdp_find_element(driver, ".page-title", log_callback=log_callback)
    if wait and "No Results Found" in wait.text:
        if log_callback:
            log_callback(f"No result for {OGfile}\n")
        else:
            print(f"No result for {OGfile}\n")
        return None

    wait = ut.cdp_find_element(driver, ".imgg", log_callback=log_callback)
    if not wait:
        if log_callback:
            log_callback(f"Search for {OGfile} timed out.\n")
        else:
            print(f"Search for {OGfile} timed out.\n")
        return None
    
    first_result = wait.get_attribute("alt")# get the first search result
    if not first_result:
        wait = ut.cdp_find_element(driver, ".grid1", log_callback=log_callback)
        first_result = wait.get_attribute("title")# if the first result is not found, try to get it from the grid1 element

    temp = first_result.replace('-', '').lower()# check if the search result matches the item we are looking for. case insensitive and remove hyphens
    nodashbanngo = banngo.replace('-', '').lower()
    if nodashbanngo not in temp:
        if log_callback:
            log_callback(f"Search result {first_result} does not match {banngo}\n")
        else:
            print(f"Search result {first_result} does not match {banngo}\n")
        return None

    ut.cdp_scroll_to_element(driver, ".imgg", log_callback=log_callback)# scroll to the search result
    ut.cdp_element_click(driver, ".imgg", log_callback=log_callback)# click on the search result again to ensure it is clicked

    wait = ut.cdp_find_element(driver, ".titl", log_callback=log_callback)
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

    metadata = ut.cdp_find_element(driver, ".infoleft", log_callback=log_callback)
    cover = ut.cdp_find_element(driver, ".large-screenshot", log_callback=log_callback)
    cover_src = cover.get_attribute('src')

    dir = os.path.abspath("img_cache")
    cover_img = ut.cdp_downloadImage(cover, banngo, dir, log_callback=log_callback)

    info = {
        "title": wait.text.strip() if wait else "Unknown",
        "metadata": metadata.text if metadata else "Unknown",
        "cover": cover_img if cover_img else cover_src,
        "OGfilename": OGfile
    }
    
    data = ut.parseInfoJavguru(info, log_callback=log_callback)

    # download the cover image
    if cached_NFO:
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
    
    wait = ut.waitVisible(driver, "id", "searchBox", log_callback=log_callback)
    if not wait:
        if log_callback:
            log_callback(f"Search for {OGfile} timed out.\n")
        else:
            print(f"Search for {OGfile} timed out.\n")
        return None
    
    searchField = ut.retry_find_element(driver, "id", "searchBox", target= "search field",log_callback=log_callback)
    current_url = driver.get_current_url()
    driver.execute_script("arguments[0].scrollIntoView();", searchField)
    ut.retry_clear(driver, "id", "searchBox", log_callback=log_callback)
    ut.retry_send_keys(driver, "id", "searchBox", banngo, log_callback=log_callback)# search for the item
    wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
    if not wait:
        ut.retry_clear(driver, "id", "searchBox", log_callback=log_callback)
        ut.retry_send_keys(driver, "id", "searchBox", banngo, log_callback=log_callback)
        wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
        if not wait:
            if log_callback:
                log_callback(f"Search for {OGfile} timed out.\n")
            else:
                print(f"Search for {OGfile} timed out.\n")
            return None
        
    wait = ut.waitVisible(driver, "xpath", '//*[@id="search"]', log_callback=log_callback)
    if not wait:
        if log_callback:
            log_callback(f"Search for {OGfile} timed out.\n")
        else:
            print(f"Search for {OGfile} timed out.\n")
        return None
    
    searchresults = ut.retry_find_element(driver, "xpath", '//*[@id="search"]', target = "search result",log_callback=log_callback)
    if searchresults is None:
        if log_callback:
            log_callback("No search results found for " + OGfile + "\n")
        else:
            print("No search results found for " + OGfile + "\n")
        return None
    
    try:
        driver.refresh()# javtrailer site has a bug where the search results are not loaded properly. This is a workaround
        checkresults = None
        checkresults = driver.find_elements("xpath", '//*[@id="search"]')[0].get_attribute("innerHTML")
        if "No videos available" in checkresults:
            if log_callback:
                log_callback(f"JavTrailers: No search results found for {OGfile}.\n")
            else:
                print(f"JavTrailers: No search results found for {OGfile}.\n")
            return None
    except:
        pass

    first_result = ut.retry_find_element(driver, "xpath", '//*[@id="search"]/div/section/div/div[1]/div/a/div/div[2]/div/p', target="first result", log_callback=log_callback)
    text = first_result.text.replace('-', '').lower()
    temp = banngo.replace('-', '').lower()
    if temp not in text:
        if log_callback:
            log_callback(f"Search result {text} does not match {banngo}\n")
        else:
            print(f"Search result {text} does not match {banngo}\n")
        return None

    current_url = driver.get_current_url()
    driver.execute_script("arguments[0].scrollIntoView();", first_result)
    ut.retry_click(driver, "xpath", "/html/body/div[1]/div/div[2]/section/div/section/div/div[1]/div/a/div/div[2]/div/p", log_callback=log_callback)
    wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
    if not wait:
        driver.execute_script("arguments[0].scrollIntoView();", first_result)
        ut.retry_click(driver, "xpath", "/html/body/div[1]/div/div[2]/section/div/section/div/div[1]/div/a/div/div[2]/div/p", log_callback=log_callback)
        wait = ut.waitURLChange(driver, current_url, log_callback=log_callback)
        if not wait:
            if log_callback:
                log_callback(f"Failed to click on search result for {OGfile}\n")
            else:
                print(f"Failed to click on search result for {OGfile}\n")
            return None
    
    wait = ut.waitVisible(driver, "xpath", "/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[3]", log_callback=log_callback)
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

    title = ut.retry_find_element(driver, "xpath", "/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[3]/h1", target= "title", log_callback=log_callback)
    metadatas = ut.retry_find_element(driver, "xpath", "/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[3]/div[1]",target = 'metadata', log_callback=log_callback)
    cover = ut.retry_find_element(driver, "xpath", "/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[3]/div[2]/img", target="cover", log_callback=log_callback)
    img_src = cover.get_attribute('data-src')

    info = {
        "title": title.text if title else "Unknown",
        "metadata": metadatas.get_attribute('innerHTML'),
        "cover": img_src,
        "OGfilename": OGfile
    }

    data = ut.parseInfoJavtrailers(info, log_callback=log_callback)

    if cached_NFO:
        cached_NFO[banngo] = data

    return data

