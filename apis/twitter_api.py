import urllib.parse

from flask import Flask, request, session
from flask_restx import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime
from controller.twitter_module.TwitterApiController import TwitterApiController

ns_twitter = Namespace('Twitter', description='Twitter Apis')

@ns_twitter.route('/addTwitterChannel/<string:screen_name>/<string:business_email>/<string:youtube_channel_id>')
class Twitter_api(Resource):
    def post(self,screen_name,business_email,youtube_channel_id):
        '''add twitter_module channel by screen_name'''
        modelObj = ConnecsiModel()
        columns = ['channel_id', 'twitter_url', 'country', 'facebook_url', 'insta_url']
        channel_data = modelObj.get__(table_name='youtube_channel_details', columns=columns,WHERE='WHERE'
                                      ,compare_column='channel_id',compare_value=str(youtube_channel_id))

        print('channel data = ',channel_data)

        for item in channel_data:
            print('im inside for')
            youtube_channel_id = item[0]
            country = item[2]
            facebook_url = item[3]
            insta_url = item[4]
            youtube_url = 'https://www.youtube.com/channel/' + youtube_channel_id
            vc_data = ''
            screen_name = screen_name
            output = ''
            try:
                print('twitter  url',item[1])
                vc_data = modelObj.get_youtube_categories_by_channel_id(channel_id=youtube_channel_id)
                print(vc_data)
            except Exception as e:
                print(e)
                pass
            video_categories = []
            try:
                for vc_item in vc_data:
                    video_categories.append(vc_item[1])
            except Exception as e:
                print(e)
                pass
            twitter_url = 'https://www.twitter.com/' + screen_name
                # output = re.findall('http(.*)', twitter_url)
            try:
                conObj = TwitterApiController()
                conObj.get_data_by_screen_name(channel_id=youtube_channel_id, twitter_url=twitter_url,
                                               screen_name=screen_name, video_categories=video_categories
                                               , country=country, facebook_url=facebook_url, insta_url=insta_url,
                                               youtube_url=youtube_url,business_email=business_email)
                modelObj.update_twitter_url_in_youtube_channel_details(twitter_url=twitter_url,youtube_channel_id=youtube_channel_id)
            except Exception as e:
                print(e)
                pass





@ns_twitter.route('/getTwitterChannelsFromTwitterSearchApi/<string:search_query>')
class Twitter_api(Resource):
    def get(self,search_query):
        '''search twitter channel by search query'''
        modelObj = ConnecsiModel()
        # output = re.findall('http(.*)', twitter_url)
        try:

            conObj = TwitterApiController()
            data = conObj.search_only_users(raw_query=search_query)
            # print(results)
            return data
        except Exception as e:
            print(e)
            return e

@ns_twitter.route('/getTwitterChannelsDetailsFromConnecsi/<string:screen_name>')
class Twitter_api(Resource):
    def get(self,screen_name):
        '''get twitter channel by screen name'''

        try:
            conObj = TwitterApiController()
            twitter_url = 'https://www.twitter.com/' + screen_name
            conObj.get_data_by_screen_name(channel_id='', twitter_url=twitter_url,
                                           screen_name=screen_name, video_categories=[]
                                           , country='', facebook_url='', insta_url='',
                                           youtube_url='', business_email='')
        except Exception as e:
            print(e)
            return e
        try:
            modelObj = ConnecsiModel()
            data = modelObj.get_twitter_channel_details_by_screen_name(screen_name=screen_name)
            columns = ['channel_id', 'screen_name', 'title', 'channel_img', 'desc', 'subscriberCount_gained',
                       'business_email', 'total_100video_views',
                       'total_100video_likes',
                       'total_100video_comments', 'total_100video_shares',
                       'facebook_url', 'insta_url', 'youtube_url', 'twitter_url', 'country','hashtags']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            # print(response_list)
            return {'data': response_list}
        except Exception as e:
            print(e)
            return e
