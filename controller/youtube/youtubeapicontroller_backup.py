# import collections
import csv
import re

import os
import requests
from configparser import ConfigParser

import time
from bs4 import BeautifulSoup
from model.ConnecsiModel import ConnecsiModel

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class YoutubeApiController:
    def __init__(self):
        self.channelId = ''
        config = ConfigParser()
        config.read('config.ini')
        self.api_key = config.get('auth', 'api_key')
        self.regionCode_url = 'https://www.googleapis.com/youtube/v3/i18nRegions?part=id,snippet&key='+self.api_key
        self.video_cat_url= 'https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&key='+self.api_key+'&regionCode=US'
        self.channel_details_url = config.get('instance', 'channel_details_url')
        self.get_channel_ids_url = 'https://www.googleapis.com/youtube/v3/search?part=id&type=channel&key='+self.api_key
        self.latest_video_ids_url= 'https://www.googleapis.com/youtube/v3/search?part=snippet&order=date&type=video&key='+self.api_key
        self.video_details_url = 'https://www.googleapis.com/youtube/v3/videos?key=' + self.api_key + '&part=snippet,statistics&id='
        self.channel_thumbnail=''
        self.channelTitle=''
        self.channel_desc=''
        self.subscriberCount=''
        self.subscriberCount_lost=0
        self.total_100video_views = 0
        self.total_100video_views_unique = 0
        self.total_100video_likes = 0
        self.total_100video_dislikes = 0
        self.total_100video_comments = 0
        self.total_100video_shares = 0
        self.facebook_url = ''
        self.insta_url = ''
        self.twitter_url = ''
        self.business_email = ''
        self.country=''



    def get_Json_data_Request_Lib(self, url):
        r = requests.get(url=url)
        json_data = r.json()
        return json_data


    def get_channel_details(self):
        self.country=''
        url = self.channel_details_url+self.channelId+'&key='+self.api_key
        # print(url)
        channel_data = self.get_Json_data_Request_Lib(url=url)
        # print(channel_data)
        # exit()
        try:
            self.channel_thumbnail = channel_data['items'][0]['snippet']['thumbnails']['medium']['url']
            # print(self.channel_thumbnail)
            # exit()
            try:
                self.country = channel_data['items'][0]['snippet']['country']
            except:pass
            self.channelTitle = channel_data['items'][0]['snippet']['title']
            self.channel_desc = channel_data['items'][0]['snippet']['description']
            # print(self.channel_desc)
            # exit()
            self.subscriberCount = channel_data['items'][0]['statistics']['subscriberCount']
            # print('channel id before getting videos data = ',self.channelId)
            video_ids = self.get_latest_video_ids(channelId=self.channelId)
            self.get_video_details(video_ids=video_ids)
            # print('channel id before social media = ',self.channelId)
            self.get_social_media_url(channel_id=self.channelId)
        except Exception as e:
            print(e)
            pass
        # return data

    def get_social_media_url(self,channel_id):
        self.facebook_url=''
        self.twitter_url=''
        self.insta_url=''
        url = 'https://www.youtube.com/channel/'+channel_id
        print(url)
        page = requests.get(url=url).content
        soup = BeautifulSoup(page,"html.parser")
        # print(soup)
        links = []
        for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
            links.append(link.get('href'))
        for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            links.append(link.get('href'))
        links = list(set(links))

        facebook_string = ['facebook']
        facebook_url = [s for s in links if any(xs in s for xs in facebook_string)]
        if facebook_url:
            self.facebook_url=facebook_url[0]

        insta_string = ['instagram']
        insta_url = [s for s in links if any(xs in s for xs in insta_string)]
        if insta_url:
            self.insta_url = insta_url[0]

        twitter_string = ['twitter_module']
        twitter_url = [s for s in links if any(xs in s for xs in twitter_string)]
        if twitter_url:
            self.twitter_url = twitter_url[0]


    def get_video_details(self,video_ids):
        print('video ids before splitting =',video_ids)
        self.total_100video_views = 0
        self.total_100video_likes = 0
        self.total_100video_dislikes = 0
        self.total_100video_comments = 0
        try:
            size = int(len(video_ids)/2)
            video_ids = [video_ids[x:x + size] for x in range(0, len(video_ids), size)]
        except:pass
        data = []
        print('video ids after spliting = ',video_ids)
        # print(type(video_ids))
        if len(video_ids) ==1:
            video_ids = [video_ids]
            print(video_ids)
            # print(type(video_ids))
        for video_id in video_ids:
            print(video_id)
            # print(type(video_id))
            video_ids_string = ','.join(video_id)
            url = self.video_details_url + video_ids_string
            print(url)
            # exit()
            json_video_data = self.get_Json_data_Request_Lib(url=url)
            items = json_video_data['items']
            for item in items:
                # print(item)
                try:
                    self.total_100video_views += int(item['statistics']['viewCount'])
                    self.total_100video_likes += int(item['statistics']['likeCount'])
                    self.total_100video_dislikes += int(item['statistics']['dislikeCount'])
                    self.total_100video_comments += int(item['statistics']['commentCount'])
                    video_cat_id = item['snippet']['categoryId']
                    video_id = item['id']
                    # self.total_100video_shares += int(item['statistics']['viewCount'])
                    # description = item['snippet']['description']
                    # print(description)
                    tdata = (self.channelId,video_id,video_cat_id)
                    data.append(tdata)
                    # print(tdata)
                    # exit()
                except:pass
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.insert__(table_name='youtube_channel_ids_video_categories_id',data=data,columns=['channel_id','video_id','video_cat_id'])
        except:pass
                # facebook_url = re.findall('http://facebook\.*.*',description)
                # if facebook_url:
                #     facebook_url_list.append(facebook_url[0])
                # insta_url = re.findall('http://instagram\.*.*', description)
                # if insta_url:
                #     insta_url_list.append(insta_url[0])
                # twitter_url = re.findall('http://twitter\.*.*', description)
                # if twitter_url:
                #     twitter_url_list.append(twitter_url[0])
                # print(twitter_url_list)
                # self.facebook_url = list(set(facebook_url_list))
                # self.insta_url= list(set(insta_url_list))
                # self.twitter_url = list(set(twitter_url_list))





    def get_latest_video_ids(self,channelId):
        print('channel id inside video method = ',channelId)
        counter = 1
        pageToken = ''
        video_ids = []
        while counter <= 2 :
            url=self.latest_video_ids_url+'&maxResults=50'+'&pageToken='+pageToken+'&channelId='+str(channelId)
            # print(url)
            # exit()
            json_data = self.get_Json_data_Request_Lib(url=url)
            print(json_data)
            try:
                pageToken = json_data['nextPageToken']
            except:pass
            try:
                items = json_data['items']
                # print(items)
                counter = counter+1
                for item in items:
                    video_ids.append(item['id']['videoId'])
            except:pass
            if pageToken == '':
                break
        print('length of video ids = ',len(video_ids))
        # exit()
        return video_ids


    def get_channel_ids_from_socialblade(self):
        all_hrefs = []
        youtube_usernames = []
        youtube_channel_id = []
        youtube_usernames_2 = []
        channel_ids=[]
        social_blade_url = 'https://socialblade.com/youtube/top/5000'
        print(social_blade_url)
        page = requests.get(url=social_blade_url).content
        soup = BeautifulSoup(page, "html.parser")

        for a in soup.find_all('a', href=True):
            # print("Found the URL:", a['href'])
            all_hrefs.append(a['href'])

        for item in all_hrefs:
            # print(item)
            # print(type(item))
            m = re.search("(/youtube/c/)(.*)", item)
            if m:
                usernames = re.sub('\xa0', '', m.group(2))
                usernames = usernames.replace('\\', '')
                # usernames = m.group(2).encode('utf-8')
                youtube_usernames.append(usernames)


            m1  = re.search("(/youtube/channel/)(.*)",item)
            if m1:
                youtube_channel_id.append(m1.group(2))

            m2 = re.search("(/youtube/user/)(.*)", item)
            if m2:
                youtube_usernames_2.append(m2.group(2))


        print(youtube_usernames)
        print(len(youtube_usernames))
        print(youtube_channel_id)
        print(len(youtube_channel_id))
        print(youtube_usernames_2)
        print(len(youtube_usernames_2))

        for username in youtube_usernames:
            social_blade_channel_url = 'https://socialblade.com/youtube/c/'+username
            print(social_blade_channel_url)
            page = requests.get(url=social_blade_channel_url).content
            soup = BeautifulSoup(page, "html.parser")
            for a in soup.find_all('a', href=True):
                m3 = re.search("(https://youtube.com/channel/)(.*)", a['href'])
                if m3:
                    channel_ids.append(m3.group(2))
            print(len(channel_ids))


        for username in youtube_usernames_2:
            social_blade_user_url = 'https://socialblade.com/youtube/user/' + username
            print(social_blade_user_url)
            page = requests.get(url=social_blade_user_url).content
            soup = BeautifulSoup(page, "html.parser")
            for a in soup.find_all('a', href=True):
                m3 = re.search("(https://youtube.com/channel/)(.*)", a['href'])
                if m3:
                    channel_ids.append(m3.group(2))
            print(len(channel_ids))

        print(channel_ids)
        print(len(channel_ids))
        mergerd_channel_ids = channel_ids+youtube_channel_id
        print(mergerd_channel_ids)
        print(len(mergerd_channel_ids))

        connecsiObj = ConnecsiModel()
        connecsiObj.insert__(data=mergerd_channel_ids, table_name='youtube_channel_ids', columns=['channel_id'],
                             IGNORE='IGNORE')




    def get_all_channel_ids(self):
        connecsiObj = ConnecsiModel()
        regionCodes = connecsiObj.get__(table_name='youtube_region_codes', STAR='*')
        # print(regionCodes)
        # query=["gaming in poland",'fashion in poland','moda i uroda w polsce','gry w polsce']
        # keywords = ['Gaming','Fashion','Fitness','Sports','Lifestyle']
        query=["Gaming%20in%20USA"]
            # , 'Fashion%20in%20USA', 'Fitness%20in%20USA','Sports%20in%20USA', 'Lifestyle%20in%20USA']
        for code in regionCodes:
            # print(code[0])
            # country_code_list=['US','CN','IN','DE','CH','AT','AU','NZ','NL','BE','LU','PL','SA','SE','NO','DK']
            priority_country_list=['US']
                # ,'PL','DE','NL','IN']
            if  code[0] in priority_country_list:
                for q in query:
                    counter = 1
                    pageToken = ''
                    channel_ids = []
                    data = []
                    while counter <= 1:
                        url = self.get_channel_ids_url + '&maxResults=50' + '&order=viewcount' + '&pageToken=' + pageToken +'&q='+q
                        print(url)
                        # exit()
                        json_data = self.get_Json_data_Request_Lib(url=url)
                        # print(len(json_data))
                        print('final json = ',json_data)
                        try:
                            pageToken = json_data['nextPageToken']
                        except:
                            pass
                        items = json_data['items']
                        print(len(items))
                        # exit()
                        counter = counter + 1
                        try:
                            for item in items:
                                # print(item)
                                # print(item['id'])
                                # print(item['id']['channelId'])
                                channel_id = item['id']['channelId']
                                # print(channel_id,code[0])
                                channel_ids.append(channel_id)
                                tdata= (channel_id,code[0])
                                print(tdata)
                                data.append(tdata)
                        except:pass

                    connecsiObj = ConnecsiModel()
                    connecsiObj.insert__(data=channel_ids,table_name='youtube_channel_ids',columns=['channel_id'],IGNORE='IGNORE')
                    # connecsiObj.insert__(table_name='youtube_channel_ids_regioncode',columns=['channel_id','regionCode'],data=data)


    def get_all_channel_ids_new(self):
        priority_country_list = ['US', 'PL', 'DE', 'NL', 'IN']
        keywords = ['Gaming','Fashion','Fitness','Sports','Lifestyle']


        # query=["Gaming%20in%20USA", 'Fashion%20in%20USA', 'Fitness%20in%20USA','Sports%20in%20USA', 'Lifestyle%20in%20USA',]
        query=["Gaming%20in%20POLAND", 'Fashion%20in%20POLAND', 'Fitness%20in%20POLAND', 'Sports%20in%20POLAND','Lifestyle%20in%20POLAND',
               "Gaming%20in%20GERMANY", 'Fashion%20in%20GERMANY', 'Fitness%20in%20GERMANY', 'Sports%20in%20GERMANY','Lifestyle%20in%20GERMANY',
               "Gaming%20in%20NETHERLANDS", 'Fashion%20in%20NETHERLANDS', 'Fitness%20in%20NETHERLANDS', 'Sports%20in%20NETHERLANDS','Lifestyle%20in%20NETHERLANDS',
               "Gaming%20in%20INDIA", 'Fashion%20in%20INDIA', 'Fitness%20in%20INDIA', 'Sports%20in%20INDIA','Lifestyle%20in%20INDIA']

        for q in query:
            # counter = 1
            print(q)
            pageToken = ''
            channel_ids=[]
            while len(channel_ids) < 1000:
                print('length of channels ids = ', len(channel_ids))
                url = self.get_channel_ids_url + '&maxResults=50&pageToken=' + pageToken +'&q='+q
                print('search url = ',url)
                # time.sleep(10)
                json_data = self.get_Json_data_Request_Lib(url=url)

                try:
                    pageToken = json_data['nextPageToken']
                except:
                    pass

                items = json_data['items']
                print('length items = ',len(items))
                if len(items) == 0:
                    print(channel_ids)
                    print(len(channel_ids))
                    connecsiObj = ConnecsiModel()
                    connecsiObj.insert__(data=channel_ids, table_name='youtube_channel_ids', columns=['channel_id'],IGNORE='IGNORE')
                    # connecsiObj.insert__(table_name='youtube_channel_ids_regioncode',columns=['channel_id','regionCode'],data=data)
                    break
                print(type(items))
                # exit()
                print("i m outside")
                for item in items:
                    print("i m in for loop")
                    try:
                        channel_id = item['id']['channelId']
                        print(channel_id)
                    except:pass
                    channel_url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&key=' + self.api_key + '&id=' + channel_id
                    print('channel url = ',channel_url)

                    json_stats = self.get_Json_data_Request_Lib(url=channel_url)
                    items1 = json_stats['items']
                    for item1 in items1:
                        try:
                            subscriberCount = item1['statistics']['subscriberCount']
                            print(subscriberCount)
                            print('query = ',q)
                            if int(subscriberCount) >= 10000:
                                channel_ids.append(channel_id)
                            else:
                                print('subscriber Count is less than 10000')
                        except:pass

                # counter = counter + 1















    def get_all_regionCodes(self):
        url = self.regionCode_url
        jsonData = self.get_Json_data_Request_Lib(url=url)
        print(jsonData)
        items=[]
        data = []
        try:
            items = jsonData['items']
        except:pass
        for item in items:
            regionCode = item['snippet']['gl']
            country_name = item['snippet']['name']
            tdata = (regionCode,country_name)
            data.append(tdata)
        print(data)
        columns = ['regionCode','country_name']
        connesiObj = ConnecsiModel()
        connesiObj.insert__(table_name='youtube_region_codes',IGNORE='IGNORE',columns=columns,data=data)

    def get_all_video_categories(self):
        url = self.video_cat_url
        jsonData = self.get_Json_data_Request_Lib(url=url)
        # print(jsonData)
        items = []
        data = []
        try:
            items = jsonData['items']
        except:
            pass
        for item in items:
            video_cat_id = item['id']
            video_cat_name = item['snippet']['title']
            tdata = (video_cat_id, video_cat_name)
            # print(tdata)
            data.append(tdata)
        columns = ['video_cat_id', 'video_cat_name']
        connesiObj = ConnecsiModel()
        connesiObj.insert__(table_name='youtube_video_categories', IGNORE='IGNORE', columns=columns, data=data)

    def get_data(self):
        obj = ConnecsiModel()
        data = obj.get__(table_name='youtube_channel_ids',STAR='*')
        # print(data)
        # exit()
        # data=(('UCsUF5-qBO_oZVMQJPl6JxAw',),('UCqbjngYxb_5vLtnTiAO0-Yw',))
        channelIds = []
        for item in data:
            # print(item[0])
            channelIds.append(item[0])
        # print(channelIds)
        # exit()
        for channelId in channelIds:
            myList = []
            # self.YoutubeApiController(channelId=channelId)
            try:
                self.channelId=channelId
                self.get_channel_details()
                myList.append(channelId)
                myList.append(self.channelTitle)
                myList.append(self.channel_thumbnail)
                myList.append(self.channel_desc)
                myList.append(self.subscriberCount)
                myList.append(self.subscriberCount_lost)
                myList.append(self.business_email)
                myList.append(self.total_100video_views)
                myList.append(self.total_100video_views_unique)
                myList.append(self.total_100video_likes)
                myList.append(self.total_100video_dislikes)
                myList.append(self.total_100video_comments)
                myList.append(self.total_100video_shares)
                myList.append(self.facebook_url)
                myList.append(self.insta_url)
                myList.append(self.twitter_url)
                myList.append(self.country)
                # print(myList)
                # exit()
                columns = ['channel_id', 'title', 'channel_img', 'desc', 'subscriberCount_gained','subscriberCount_lost', 'business_email',
                           'total_100video_views','total_100video_views_unique','total_100video_likes','total_100video_dislikes','total_100video_comments',
                           'total_100video_shares','facebook_url','insta_url','twitter_url','country']
                connecsiObj = ConnecsiModel()
                connecsiObj.insert__(table_name='youtube_channel_details',columns=columns,IGNORE='IGNORE',data=myList)
            except:
                print('Channel details failed to insert for channel_id = ',channelId)
                pass

            # with open("output.csv", 'a') as resultFile:
            #     wr = csv.writer(resultFile, dialect='excel')
            #     wr.writerow(myList)

    def get_data_by_selinium(self):
        # example option: add 'incognito' command line arg to options
        option = webdriver.ChromeOptions()
        option.add_argument("--incognito")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(dir_path)
        # exit()
        # create new instance of chrome in incognito mode
        browser = webdriver.Chrome(executable_path='C:\connecsiAdminMaterial\controller\youtube\chromedriver_win32\chromedriver.exe',
                                   chrome_options=option)
        # go to website of interest
        browser.get("https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ/about")
        # wait up to 10 seconds for page to load
        # timeout = 20
        # try:
        #     WebDriverWait(browser, timeout).until(
        #         EC.visibility_of_element_located((By.XPATH, "//a[@class='style-scope ytd-channel-about-metadata-renderer")))
        # except TimeoutException:
        #     print("Timed out waiting for page to load")
        #     browser.quit()
        wait = WebDriverWait(browser, 10)
        try:
            element = wait.until(EC.element_to_be_clickable((By.ID, 'button')))
        except:
            print("Timed out waiting for page to load")
            browser.quit()
        # get all of the titles for the financial values


        # location = browser.find_element_by_xpath("//td[@class='style-scope ytd-channel-about-metadata-renderer']")
        # titles = [x.text for x in location]



    def update_channel_data(self):
        obj = ConnecsiModel()
        data = obj.get__(table_name='youtube_channel_ids', STAR='*')
        channelIds = []
        for item in data:
            # print(item[0])
            channelIds.append(item[0])
        for channel_id in channelIds:
            country=''
            print(channel_id)
            url = self.channel_details_url + channel_id + '&key=' + self.api_key
            channel_data = self.get_Json_data_Request_Lib(url=url)
            print(channel_data)
            try:
                country = channel_data['items'][0]['snippet']['country']
            except:
                pass
            columns = ['country']
            data = country,
            try:
                connecsiObj = ConnecsiModel()
                res = connecsiObj.update_youtube_channel_data(channel_id=channel_id,country=country)
            except Exception as e:
                print(e)
            # exit()
