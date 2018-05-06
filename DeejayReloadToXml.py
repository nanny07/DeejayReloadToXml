import bs4, requests, re
import xml.etree.ElementTree as ET

programName = 'chiamate-roma-triuno-triuno'

nPage = 0
dicItems = {}

while True:
    baseUrl = 'https://www.deejay.it/audio/'
    if nPage != 0:
        baseUrl = baseUrl + 'page/' + str(nPage) + '/'
    pageUrl = baseUrl + '?reloaded=' + programName
    page = requests.get(pageUrl)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    ul = soup.find('ul', class_='lista')

    liList = ul.find_all('li')
    for li in liList:
        aElement = li.find('a')

        episodeTitle = aElement.text
        episodeUrl = aElement['href']
        episodePage = requests.get(episodeUrl)
        episodeSoup = bs4.BeautifulSoup(episodePage.content, 'html.parser')
        episodeFrameUrl = episodeSoup.find('iframe')['src']
        episodeMp3Link = re.search('https?://flv.+\.mp3', episodeFrameUrl).group(0)

        #TODO Save to a DB and break the while if I found a link already present
        print(episodeMp3Link)

        dicItems[episodeTitle] = episodeMp3Link

    nextPage =  soup.find('a', class_='nextpostslink')
    if nextPage != None:
        break

    nPage+=1

#TODO Create Podcast XML Feed
rss = ET.Element('rss')
rss.set('xmlns:itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')
rss.set('xmlns:googleplay', 'http://www.google.com/schemas/play-podcasts/1.0')
rss.set('xmlns:feedburner', 'http://rssnamespace.org/feedburner/ext/1.0')
channel = ET.SubElement(rss, 'channel')
title = ET.SubElement(channel, 'title').text = 'test'
link = ET.SubElement(channel, 'link').text = 'test'
language = ET.SubElement(channel, 'language')
language.text = 'it'
for k,v in dicItems.items():
    item = ET.SubElement(channel, 'item')
    ET.SubElement(item, 'title').text = k
    ET.SubElement(item, 'link').text = v
ET.dump(rss)