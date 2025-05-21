#次にやること・・・安曇野中学校のすクールリストを整理し接続を確認する


import csv
import os
import site
import sys
import requests
import tweepy
from pprint import pprint
import time


#import slackweb
import pandas as pd
from bs4 import BeautifulSoup

import schoolList
import tweetPro
#import schoolInfodata.saveSchoolInfocsv as saaveCsv



def main():
    for school in schoolList.schoolList:
        scraypedDate = scrayping(school[1],school[2],school[4])
        #output_csv(scraypedDate,school[0])
        newInfo = list_diff(scraypedDate,read_csv(school[0]))
        if(len(newInfo) != 0):
            tweetPro.tweetNewinfo(newInfo,school[3])
        output_csv(scraypedDate,school[0])
        time.sleep(2)
        """
        
        
        """
        


#ホームページから必要な情報を配列で返す
def scrayping(url,classificationTag,siteclassificationTag):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    results = []
    if(siteclassificationTag == 'ShindaiFuzoku'):
        for siteData in soup.find_all(class_ = classificationTag):
            url = siteData.find("a")
            if(url is not None):
                results.append([
                    siteData.text,
                    url.get('href')
                ])

    elif(siteclassificationTag == 'Yashiro'):
        for siteData in soup.find_all(classificationTag):
            url = siteData.find("a")
            results.append([
                siteData.text,
                'https://www.nagano-c.ed.jp/yashiro/posts/'+url.get('href')
            ])
    elif(siteclassificationTag == 'GakkoDayoriPDF'):
        siteData = soup.find_all(class_ = classificationTag)
        for siteData in soup.find_all("p"):
            url = siteData.find("a")
            if(url == None):
                break
            else:
                results.append([
                    siteData.text,
                    url.get('href')
                ])
    elif(siteclassificationTag == 'Uedashi'):
        for siteData in soup.find_all(classificationTag):
            try:
                url = siteData.find_all("a")[1]
                results.append([
                    siteData.text,
                    url.get('href')
                ])
            except IndexError:
                print('IndexError')

    elif(siteclassificationTag == 'greenHiruzu'):
        soup =soup.find_all(class_ = classificationTag)[1]
        for siteData in soup.find_all("a"):
            if(siteData is not None):
                results.append([
                    siteData.text,
                    siteData.get('href')
                ])

    elif(siteclassificationTag == 'NaganoNichidaiSyo'):
        soup = soup.find(class_ = 'content')
        for siteData in soup.find_all(classificationTag):
            try:
                url = siteData.find("a")
                results.append([
                    siteData.text,
                    url.get('href')
                ])
            except IndexError:
                print('IndexError')
    
    elif(siteclassificationTag == 'OohinatasyoCyu'):
        for siteData in soup.find_all(class_ = 'info-list-item'):
            tytle =siteData.find("em")
            try:
                url = siteData.find("a")
                results.append([
                    tytle.text,
                    url.get('href')
                ])
            except IndexError:
                print('IndexError')
    
    elif(siteclassificationTag == 'Azuminoshi'):
        for siteData in soup.find_all(class_ = classificationTag):
            try:
                results.append([
                    siteData.text,
                    url
                ])
            except IndexError:
                print('IndexError')

    elif(siteclassificationTag == 'Naganoshi'):
        for siteData in soup.find_all(classificationTag):
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
                    print('IndexErrorNaganoshi')

    for result in results:
        for Record in result:
            Record.encode('cp932', "ignore")     

    return results

#受け取った配列をCSVに記入する 
def output_csv(result,schoolName):
    with open('schoolInfodata/'+schoolName+'_last_log.csv', 'w', newline='',encoding='cp932', errors="ignore") as file:
        headers = ['Title', 'URL']
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in result:
            writer.writerow(row) 


#CSVを開く
def read_csv(schoolName):
    if not os.path.exists('schoolInfodata/'+schoolName+'_last_log.csv'):
        print('schoolInfodata/'+schoolName+'_last_log.csv')
        raise Exception('ファイルがありません。')
    if os.path.getsize('schoolInfodata/'+schoolName+'_last_log.csv') == 0:
        raise Exception('ファイルの中身が空です。')
    csv_list = pd.read_csv('schoolInfodata/'+schoolName+'_last_log.csv', header=None, encoding="cp932",encoding_errors='ignore')
    return csv_list

#二種類の配列から差分を出す
def list_diff(result, last_result):
    return_list = []
    for tmp in result:
        if tmp not in last_result.values:
            return_list.append(tmp)
    return return_list

#与えられた配列を最下部に記録する
def write_csv(newInfo):
    if not os.path.exists('tewwtedInfo'):
        raise Exception('ファイルがありません。')
    if os.path.getsize('tewwtedInfo') == 0:
        raise Exception('ファイルの中身が空です。')

    with open('tewwtedInfo','w',newline='',encoding='cp932',errors="ignore") as file:
        writer = csv.writer(file)
        for row in newInfo: 
            writer.writerow(row)

    

if __name__ == "__main__":
    main()

 