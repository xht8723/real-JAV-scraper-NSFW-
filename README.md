# Real JAV Scraper (NSFW)

<img width="401" alt="屏幕截图 2025-02-25 074749" src="https://github.com/user-attachments/assets/8915057b-c0ad-436d-9e6f-17b710e819dd" alt="drawing" width="600"/>
<img src="https://github.com/user-attachments/assets/7d1e2c30-a1fd-4ff3-b41e-c593d78ea659" alt="drawing" width="700"/>
<img src="https://github.com/user-attachments/assets/17ece9e5-4f50-486c-8407-d2e8af1ea6ad" alt="drawing" width="700"/>



## Features

Scrapes JAV metadata for media system like Jellyfin/Emby from javguru/javTrailers. Actress info from javmodel/javguru

Creating .nfo file, folder and cover image that are compatible with Jellyfin file structure.

Using Seleniumbase[https://github.com/seleniumbase/SeleniumBase] to simulate real browser to workaround cloudfare bots prevention.

Format actress names. Gather an actress's CN,JP,EN names and nicely organize them in nfo files so that jellyfin won't identify the same person as different actress.

Pressure tested over 3000+ movies.

Batch rename subtitles.

Batch create hardlinks.

## Upcoming features

Optional recursive directory search.

DLSITE ASMR support.

## How to install

There will be .exe binary available in release page, just use that.

IMPORTANT NOTE: You must have chrome installed on your computer because this is utilizing chrome's CDP mode to avoid captchas.

___________________

## Run it yourself

### Windows

*Install python3 and run ```pip install -r requirements.txt```*

*Install Chrome browser*

Run main.pyw

### Linux

*Install python3 and run ```pip install -r requirements```*

*Install Chrome browser*

*Install libxcb-cursor0 with ```sudo apt install libxcb-cursor0```

Run main.pyw

## Usage

Enter your folder path on the up right corner or just "..." to select one.

Just click start.

Your AV file must contain the AV label number. eg: "<ins>ABF-120</ins>WHATEVERwords.mp4" （MUST contain dash "-"）

After AV being nicely organized and have NFO files in the folder, click "format actress name".

This will go through all AV actresses in folder, search them online to gather JP/EN/CN names of actresses and edit the NFO actress information so that Jellyfin would dub them as the same person.

## Some other tools recommendation

Use [gfriends-inputer](https://github.com/gfriends/gfriends-inputer) to download actress image and merge into your jellyfin system.

Use [ReNamer](https://www.den4b.com/products/renamer) for adding dashes or manay file name in general.

# 中文

一个日本AV metadata爬虫，适配Jellyfin，Emby等媒体管理系统。metadata来源：javguru/javatrailers/javmodel

会采用jellyfin的文件管理结构，创建.nfo文件，并建立文件夹下载媒体封面。

Format actress name会从javmodel网站搜刮女优的中文日文英文名，并把不同语言的名字并作一个人。

采用Seleniumbase模拟真实浏览器，从而绕过各自反爬虫限制，采用chrome CDP模式绕过captcha“你是机器人吗？”

一些小工具：批量重命名字幕文件，批量创建硬链接。

## 如何安装
github的release页面会有打包好的exe文件，直接用就好。

重要：必须安装Chrome浏览器。chrome的CDP模式是绕过captcha认证的关键。

--------------

如果想自己build，只要安装python3，然后安装requirements.txt里的东西就好了：```pip install -r requirements.txt```

下载Chrome浏览器。

只在windows测试过，其它系统怎么样我完全不知道。

## 使用

选取或者自己输入放AV的文件夹地址，点击start就好。

完成影片搜索之后，点击format actress name开始搜索女优的名字，并把日文名/中文名/英文名在NFO文件里并作一个人。这样Jellyfin就不会把同一个人但是名字语言不一样认作两个人了。

重要：你的AV文件名里面必须要有番号和横杠。类似 “ABF-122澳门赌场1111.mp4”

暂不支持没有横杠的文件。搜起来太地狱了。

## 自己运行

*安装python3 并运行： ```pip install -r requirements.txt```*

*安装Chrome浏览器*

*运行main.pyw*

## 一些其它工具推荐

使用[gfriends-inputer](https://github.com/gfriends/gfriends-inputer)来下载并导入女优头像到jellyfin

使用[ReNamer](https://www.den4b.com/products/renamer) 来重命名没有横杠“-”的文件。
