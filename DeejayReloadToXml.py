import bs4, requests, re

programName = 'chiamate-roma-triuno-triuno'

nPage = 0

while True:
    baseUrl = 'https://www.deejay.it/audio/'
    if nPage != 0:
        baseUrl += 'page/' + nPage + '/'
    pageUrl = baseUrl + programName
    page = requests.get(pageUrl)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    ul = soup.find('ul', class_='lista')
    nextPage =  soup.find('a', class_='nextpostslinksssss')

    liList = ul.find_all('li')
    for li in liList:
        episodeUrl = li.find('a')['href']
        episodePage = requests.get(episodeUrl)
        episodeSoup = bs4.BeautifulSoup(episodePage.content, 'html.parser')

        episodeFrameUrl = episodeSoup.find('iframe')['src']

        # http://flv.kataweb.it/deejay/audio/chiamate_roma_triuno_triuno/20180503.mp3
        episodeMp3Link = re.search('https?://flv.+\.mp3', episodeFrameUrl).group(0)

        print(episodeMp3Link)

    if nextPage == None:
        break

    nPage+=1

#TODO Create Podcast XML Feed