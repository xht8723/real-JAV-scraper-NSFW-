# Real JAV Scraper (NSFW)

<img src="https://github.com/user-attachments/assets/b6e90801-561d-4778-ab99-d6dec2b170cd" alt="drawing" width="600"/>
<img src="https://github.com/user-attachments/assets/7d1e2c30-a1fd-4ff3-b41e-c593d78ea659" alt="drawing" width="700"/>
<img src="https://github.com/user-attachments/assets/17ece9e5-4f50-486c-8407-d2e8af1ea6ad" alt="drawing" width="700"/>


## Features

Scrapes JAV metadata for media system like Jellyfin/Emby from javguru. Actress info from javmodel

Creating .nfo file, folder and cover image that are compatible with Jellyfin file structure.

Using Selenium to simulate real browser to workaround cloudfare bots prevention.

Format actress names.

Gather an actress's CN,JP,EN names and nicely organize them in nfo files so that jellyfin won't identify the same person as different actress.

Pressure tested over 3000+ movies.

## How to install

There will be .exe binary available in release page.

___________________


If you want build yourself, all dependencies are in requirements.txt

*Install python3 and run ```git install -r requirements.txt```*

*Download firefox driver "geckodriver.exe" and place in same folder.*

Run main.pyw

## Usage

Enter your folder path on the up right corner or just "..." to select one.

Just click start.

If Headless mode is unchecked, there will be a simulated browser window appear and you can watch it scrapping site.

Check headless mode if you don't want see it.

Your AV file must contain the AV label number. eg: "<ins>ABF-120</ins>WHATEVERwords.mp4"


# 中文

一个日本AV metadata爬虫，适配Jellyfin，Emby等媒体管理系统。metadata来源：javguru

会采用jellyfin的文件管理结构，创建.nfo文件，并建立文件夹下载媒体封面。

采用Selenium模拟真实浏览器，从而绕过各自反爬虫限制。

## 如何安装
github的release页面会有打包好的exe文件，直接用就好。

--------------

如果想自己build，只要安装python3，然后安装requirements.txt里的东西就好了：```git install -r requirements.txt```

需要自己下载firefox的浏览器驱动，"geckodriver.exe"，把它放在同一文件夹下。

## 使用

选取或者自己输入放AV的文件夹地址，点击start就好。

如果headless mode没有勾选，则会弹出模拟的firefox浏览器进行自动操作。

如果不想看，把headless mode勾上就可以了。

重要：你的AV文件名里面必须要有番号。类似 “ABF-122澳门赌场1111.mp4”
