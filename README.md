# Real JAV Scraper

Scrapes JAV metadata for media system like Jellyfin/Emby from javguru

Creating .nfo file, folder and cover image that are compatible with Jellyfin file structure.

Using Selenium to simulate real browser to workaround cloudfare bots prevention.

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