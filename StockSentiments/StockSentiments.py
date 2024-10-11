from bs4 import BeautifulSoup
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class StockSentiments:
    def __init__(self):
        self.map = {
            'Strong Sell': -1,
            'Sell': -0.5,
            'Neutral': 0,
            'Buy': 0.5,
            'Strong Buy': 1,
        }
        self.headers = {
            "x-requested-with": "XMLHttpRequest",
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        self.analyzer = SentimentIntensityAnalyzer()
    def __sentiment__(self, url):
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        news = soup.find('ul', attrs={'data-test': 'news-list'})
        news = news.findAll('li')
        score = []
        for i in news:
            try:
                i = i.find('article')
                i = i.find('div')
                i = i.find('a')['href']
                i = " ".join(
                    i.replace("https://www.investing.com/news", "").split("/")[2].replace("-", " ").capitalize().split(
                        " ")[0:-2])
                sentiments = self.analyzer.polarity_scores(i)['compound']
                score.append(sentiments)
            except:
                pass
        return sum(score) / len(score)
    def __technical__(self, url, classname):
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        score = soup.find('div', class_=classname)
        score = score.findAll('div')[-1].text
        return self.map[score]
    def nasdaq(self):
        sentiment = self.__sentiment__("https://www.investing.com/indices/nasdaq-composite-news")
        technical = self.__technical__("https://www.investing.com/indices/nasdaq-composite", 'analyst-price-target_gaugeView__yP3BV')
        return (sentiment, technical)
    def nse(self):
        sentiment = self.__sentiment__("https://www.investing.com/indices/s-p-cnx-nifty-news")
        technical = self.__technical__("https://www.investing.com/indices/s-p-cnx-nifty",'analyst-price-target_gaugeContainer__F_79r')
        return (sentiment, technical)
    def nikkei(self):
        sentiment = self.__sentiment__("https://www.investing.com/indices/japan-ni225-news")
        technical = self.__technical__("https://www.investing.com/indices/japan-ni225",'analyst-price-target_gaugeView__yP3BV')
        return (sentiment, technical)
    def usmarkets(self):
        url = "https://www.moneycontrol.com/us-markets"
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        score = soup.find('div', attrs={'class': 'advdeclbar_addecl_bar__g00jQ'})
        score = score.find('div', attrs={'class': 'advdeclbar_bartxt__PtpoC'})
        positive = int(score.find('span', attrs={'class': 'advdeclbar_baradv__ZR5QZ'}).text)
        negative = int(score.find('span', attrs={'class': 'advdeclbar_bardecl__zHqDg'}).text)
        return (positive - negative)/(positive + negative)
    def inmarkets(self):
        url = "https://www.moneycontrol.com/stocksmarketsindia/"
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        score = soup.find('div', attrs={'class': 'adhvbox'})
        score = soup.find('div', attrs={'class': 'adwgray'})
        score = score.find('div', attrs={'class': 'bartxt'})
        positive = int(score.find('span', attrs={'class': 'baradv'}).text)
        negative = int(score.find('span', attrs={'class': 'bardecl'}).text)
        return (positive - negative)/(positive + negative)

if __name__ == "__main__":
    SS = StockSentiments()
    print("NASDAQ: ", SS.nasdaq())
    print("NSE: ", SS.nse())
    print("NIKKEI: ", SS.nikkei())
    print("US Markets: ", SS.usmarkets())
    print("IN Markets: ", SS.inmarkets())