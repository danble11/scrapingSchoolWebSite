import requests
import pandas as pd
from bs4 import BeautifulSoup



def main():

    url = 'https://www.nagano-ngn.ed.jp/joyamajs/top.html'
    siteclassificationTag = 'Naganoshi'


    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    results = []
    if(siteclassificationTag == 'Naganoshi'):
        for siteData in soup.find_all("iframe"):
            url = url[:6] + siteData['src']
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            for InformationsiteData in soup.find_all("b"):
                try:
                    results.append([
                    InformationsiteData.text,
                    url
                ])
                except IndexError:
                    print('IndexError')

        print(results)


if __name__ == "__main__":
    main()


