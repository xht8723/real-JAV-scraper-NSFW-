import re
import os
import util as ut

#----------------------------------------------
# Scrape actress names from javmodels
#----------------------------------------------
def processSearch(driver, name, cached_names = None, log_callback=None):
    if cached_names is None:
        cached_names = {}

    if name in cached_names:
        return cached_names[name]

    if log_callback:
        log_callback("Searching for: " + name + "\n")
    else:
        print("Searching for: " + name + "\n")

    wait = ut.cdp_find_element(driver, 'svg[width="22"][height="22"][viewBox="0 0 22 22"]', log_callback=log_callback)
    if not wait:
        raise(Exception("Search button not found. Please check connection.1"))
    
    driver.cdp.wait_for_element_visible('svg[width="22"][height="22"][viewBox="0 0 22 22"]')
    ut.cdp_scroll_to_element(driver, 'svg[width="22"][height="22"][viewBox="0 0 22 22"]', log_callback=log_callback)
    ut.cdp_element_click(driver, 'svg[width="22"][height="22"][viewBox="0 0 22 22"]', log_callback=log_callback)
    driver.cdp.wait_for_element_visible('.form-control.form-control-lg.flq-form-glass.flq-search-input')
    ut.cdp_clear(driver, '.form-control.form-control-lg.flq-form-glass.flq-search-input', log_callback=log_callback)
    ut.cdp_type(driver, '.form-control.form-control-lg.flq-form-glass.flq-search-input', name, log_callback=log_callback)
    ut.cdp_press_keys(driver, '.form-control.form-control-lg.flq-form-glass.flq-search-input', "\n", log_callback=log_callback)

    wait = ut.cdp_find_element(driver, '.content-wrap', log_callback=log_callback)
    if not wait:
        if log_callback:
            log_callback("Seaching for " + name + " timed out1\n")
        else:
            print("Seaching for " + name + " timed out1\n")
        return None
    
    if "Result Not Found" in wait.text:
        if log_callback:
            log_callback("No result found for " + name + "\n")
        else:
            print("No result found for " + name + "\n")
        return None

    wait = ut.cdp_find_element(driver, '.card-title.h6', log_callback=log_callback)
    ut.cdp_scroll_to_element(driver, '.card-title.h6', log_callback=log_callback)
    ut.cdp_element_click(driver, '.card-title.h6', log_callback=log_callback)

    if 'hd' in driver.cdp.get_current_url():
        wait = ut.cdp_find_element(driver, 'a.flq-tag', log_callback=log_callback)
        if not wait:
            if log_callback:
                log_callback("Seaching for " + name + " timed out2\n")
            else:
                print("Seaching for " + name + " timed out2\n")
            return None
        ut.cdp_scroll_to_element(driver, 'a.flq-tag', log_callback=log_callback)
        ut.cdp_element_click(driver, 'a.flq-tag', log_callback=log_callback)

    card = ut.cdp_find_element(driver, '.col-12.col-lg-7.col-xxl-8.remove-animation.card', log_callback=log_callback)
    if not card:
        if log_callback:
            log_callback("Seaching for " + name + " timed out3\n")
        else:
            print("Seaching for " + name + " timed out3\n")
        return None
    
    innerHTML = card.get_attribute("innerHTML")
    names = processCardInfo(innerHTML, log_callback=log_callback)

    for each in names:
        if name.lower() in each.lower():
            cached_names[name] = names
            return names
    if log_callback:
        log_callback(f"Name {name} not found in search results\n")
    else:
        print(f"Name {name} not found in search results\n")
    return None

#----------------------------------------------
# Scrape actress names from javguru
#----------------------------------------------
def processSearchJavguru(driver, name, cached_names = None, log_callback=None):
    if cached_names is None:
        cached_names = {}
    if name in cached_names:
        return cached_names[name]

    wait = ut.cdp_find_element(driver, '.search-input', log_callback=log_callback)
    if not wait:
        raise(Exception("Search field not found. Please check connection.1"))
    
    if log_callback:
        log_callback("Searching for: " + name + "\n")
    else:
        print("Searching for: " + name + "\n")
    
    ut.cdp_scroll_to_element(driver, '.search-input', log_callback=log_callback)
    ut.cdp_clear(driver, '.search-input', log_callback=log_callback)
    ut.cdp_type(driver, '.search-input', name, log_callback=log_callback)
    ut.cdp_press_keys(driver, '.search-input', "\n", log_callback=log_callback)

    wait = ut.cdp_find_element(driver, '.actress-box', log_callback=log_callback)
    if not wait:
        if log_callback:
            log_callback("Seaching for " + name + " timed out1\n")
        else:
            print("Seaching for " + name + " timed out1\n")
        return None
    
    if "No results found" in wait.text:
        if ' ' in name:
            name = name.split(' ')[1] + ' ' + name.split(' ')[0]# try to reverse first and last name
            ut.cdp_scroll_to_element(driver, '.search-input', log_callback=log_callback)
            ut.cdp_clear(driver, '.search-input', log_callback=log_callback)
            ut.cdp_type(driver, '.search-input', name, log_callback=log_callback)
            ut.cdp_press_keys(driver, '.search-input', "\n", log_callback=log_callback)
            wait = ut.cdp_find_element(driver, '.actress-box', log_callback=log_callback)
            if not wait:
                if log_callback:
                    log_callback("Seaching for " + name + " timed out2\n")
                else:
                    print("Seaching for " + name + " timed out2\n")
                return None
            if "No results found" in wait.text:
                if log_callback:
                    log_callback("No result found for " + name + "\n")
                else:
                    print("No result found for " + name + "\n")
                return None
    
    enName = ut.cdp_find_element(driver, '.actrees-name', log_callback=log_callback)
    if enName is None:
        if log_callback:
            log_callback("Seaching for " + name + " timed out2\n")
        else:
            print("Seaching for " + name + " timed out2\n")
        return None

    jpName = ut.cdp_find_element(driver, 'span[style*="#7664bf"]', log_callback=log_callback)
    if jpName is None:
        if log_callback:
            log_callback("Seaching for " + name + " timed out3\n")
        else:
            print("Seaching for " + name + " timed out3\n")
        return None

    enName = enName.text
    enNameR = enName.split(" ")
    enNameR = ' '.join(enNameR[::-1])# reverse first and last name
    jpName = jpName.text
    if name.lower() not in [enName.lower(), jpName.lower(), enNameR.lower()]:
        if log_callback:
            log_callback(f"Name {name} not found in search results\n")
        else: 
            print(f"Name {name} not found in search results\n")
        return None
    
    cached_names[name] = [enName, jpName, enNameR]
    return [enName, jpName, enNameR]

#----------------------------------------------
# process actress names from card info for javmodels
#----------------------------------------------
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
    if log_callback is not None:
        log_callback(f"Found names: {names}\n")
    else:
        print(f"Found names: {names}\n")
    names = list(set(names))
    return names

#----------------------------------------------
# recursive search for actress names in nfo files under directory
#----------------------------------------------
def searchNFO(dir, toDir=None, log_callback=None, update_callback=None):
    nfoFormat = '.nfo'
    actors = {}
    for root, dirs, files in os.walk(dir):
        for file in files:
            if nfoFormat in file:
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    match = re.findall(r'<name>.*?</name>', f.read(), flags = re.UNICODE)
                    if match:
                        for actor in match:
                            if actor == '<name></name>':
                                continue
                            if actor == '<name>Unknown</name>':
                                continue
                            actorname = actor[6:-7]
                            if actorname not in actors:
                                filename = os.path.join(root, file)
                                actors[actorname] = [filename]
                                if update_callback is not None:
                                    update_callback(actorname, '')
                            else:
                                filename = os.path.join(root, file)
                                actors[actorname].append(filename)
                    else:
                        if log_callback is not None:
                            loc = os.path.join(root, file)
                            log_callback(f"No actor name found in {loc}\n", "orange")
                        else:
                            loc = os.path.join(root, file)
                            print(f"No actor name found in {loc}\n")
                if toDir is not None:
                    pass
    if log_callback is not None:                
        log_callback(f"Found actors number: {len(actors)}\n")
    else:
        print(f"Found actors number: {len(actors)}\n")
    return actors

#----------------------------------------------
# modify actress info in nfo files(and tags)
#----------------------------------------------
def modifyNFO(actors, actor, names, toDir=None, log_callback=None, update_callback=None):
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
        if log_callback is not None:
            log_callback(f"Modified actress info for {file}\n")
        else:
            print(f"Modified actress info for {file}\n")
        if update_callback is not None:
            nameString = ''
            for name in names:
                nameString += name + ', '
            update_callback(actor, nameString[:-2])
    return

#----------------------------------------------
# decide primary name from names. Japanese names are preferred
#----------------------------------------------
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

