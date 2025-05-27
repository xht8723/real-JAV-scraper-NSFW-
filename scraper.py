import os
import util as ut

def processSearchJavguru(driver, banngo, OGfile, cached_NFO = None, log_callback=None):
    """
    Searches for a single item on javguru and returns its metadata.

    :param driver: The Selenium WebDriver instance.
    :param banngo: The identifier for the item to search for.
    :param OGfile: The original filename of the item.
    :param cached_NFO: A dictionary to cache the metadata.
    :param log_callback: A callback function for logging messages.
    :return: A dictionary containing the item's metadata or None if not found.
    """
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

    wait_img = ut.cdp_find_element(driver, ".imgg", log_callback=log_callback)
    wait_text = ut.cdp_find_element(driver, ".grid1", log_callback=log_callback)
    
    first_result = wait_img.get_attribute("alt")# get the first search result
    if not first_result:
        first_result = wait_text.get_attribute("title")# if the first result is not found, try to get it from the grid1 element

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
    ut.cdp_scroll_to_element(driver, ".large-screenshot", log_callback=log_callback)  # Ensure the cover is in view
    cover_src = cover.get_attribute('src')

    dir = os.path.abspath("img_cache")
    cover_img = ut.cdp_screenshotElement(driver, cover_src, dir, banngo, log_callback=log_callback)

    info = {
        "title": wait.text.strip() if wait else "Unknown",
        "metadata": metadata.text if metadata else "Unknown",
        "cover": cover_img if cover_img else cover_src,
        "OGfilename": OGfile
    }
    
    data = ut.parseInfoJavguru(info, log_callback=log_callback)

    if cached_NFO is not None:
        if log_callback:
            log_callback(f"Caching metadata for {banngo}\n")
        else:
            print(f"Caching metadata for {banngo}\n")
        cached_NFO[banngo] = data
    return data

def processSearchJavtrailers(driver, banngo, OGfile, cached_NFO, log_callback=None):
    """
    Searches for a single item on javtrailers and returns its metadata.
    :param driver: The Selenium WebDriver instance.
    :param banngo: The identifier for the item to search for.
    :param OGfile: The original filename of the item.
    :param cached_NFO: A dictionary to cache the metadata.
    :param log_callback: A callback function for logging messages.
    :return: A dictionary containing the item's metadata or None if not found.
    """

    if log_callback:
        log_callback(f"Searching for: {OGfile} on javtrailers\n")
    else:
        print(f"Searching for: {OGfile} on javtrailers\n")
    
    if cached_NFO:
        cache = ut.check_cache(banngo, cached_NFO, OGfile, log_callback=log_callback)# check if the item is already in the json, return stored data if it is
        if cache:
            return cache
    
    wait = ut.cdp_find_element(driver, "#searchBox", log_callback=log_callback)
    if not wait:
        if log_callback:
            log_callback(f"Search for {OGfile} timed out.\n")
        else:
            print(f"Search for {OGfile} timed out.\n")
        return None
    
    ut.cdp_clear(driver, "#searchBox", log_callback=log_callback)# clear the search field
    ut.cdp_type(driver, "#searchBox", banngo, log_callback=log_callback)# search for the item
    ut.cdp_press_keys(driver, "#searchBox", "\n", log_callback=log_callback)# press enter to search

    wait = ut.cdp_find_element(driver, "#search", log_callback=log_callback)
    wait = ut.cdp_find_element(driver, ".videos-list", log_callback=log_callback)
    if "No videos available" in wait.text:
        if log_callback:
            log_callback(f"JavTrailers: No search results found for {OGfile}.\n")
        else:
            print(f"JavTrailers: No search results found for {OGfile}.\n")
        return None
    
    wait = ut.cdp_find_element(driver, ".card-text", log_callback=log_callback)

    first_result = wait.text
    text = first_result.replace('-', '').lower()
    temp = banngo.replace('-', '').lower()
    if temp not in text:
        if log_callback:
            log_callback(f"Search result {text} does not match {banngo}\n")
        else:
            print(f"Search result {text} does not match {banngo}\n")
        return None

    ut.cdp_scroll_to_element(driver, ".card-text", log_callback=log_callback)# scroll to the search result
    ut.cdp_element_click(driver, ".card-text", log_callback=log_callback)
    
    if log_callback:
        log_callback("getting metadata on " + banngo + "\n")
    else:
        print("getting metadata on " + banngo + "\n")

    title = ut.cdp_find_element(driver, '.lead', log_callback=log_callback)
    metadata = ut.cdp_find_element(driver, '.col-md-9', log_callback=log_callback)
    ut.cdp_scroll_to_element(driver, '#description .img-fluid.mt-4', log_callback=log_callback)  # Ensure the cover is in view
    cover = ut.cdp_find_element(driver, '#description .img-fluid.mt-4', log_callback=log_callback)
    img_src = cover.get_attribute('src')

    dir = os.path.abspath("img_cache")
    cover_img = ut.cdp_screenshotElement(driver, img_src, dir, banngo, log_callback=log_callback)


    info = {
        "title": title.text if title else "Unknown",
        "metadata": metadata.get_attribute('innerHTML'),
        "cover": cover_img if cover_img else img_src,
        "OGfilename": OGfile
    }

    data = ut.parseInfoJavtrailers(info, log_callback=log_callback)

    if cached_NFO is not None:
        if log_callback:
            log_callback(f"Caching metadata for {banngo}\n")
        else:
            print(f"Caching metadata for {banngo}\n")
        cached_NFO[banngo] = data
    return data

