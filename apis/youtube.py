from flask import Flask, request, session
from flask_restx import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime
from controller.youtube.YoutubeApiController import YoutubeApiController
import requests

ns_youtube = Namespace('Youtube', description='Youtube Apis')

search_channels_form = ns_youtube.model('Search Channels', {
    'category_id' : fields.String(required=False, description='Category ID'),
    'country' : fields.String(required=False, description='Country'),
    'min_lower' : fields.Integer(required=False, description='Min Followers'),
    'max_upper' : fields.Integer(required=False, description='Max Followers'),
    'sort_order' : fields.String(required=False, description='Sort Order'),
    'offset' : fields.Integer(required=True, description='Offset')
})


@ns_youtube.route('/regionCodes')
class RegionCodes(Resource):
    def get(self):
        '''get all youtube region codes'''
        connecsiObj = ConnecsiModel()
        region_codes = connecsiObj.get__(table_name='youtube_region_codes', STAR='*')
        columns = ['region_code', 'country_name']
        response_list = []
        for item in region_codes:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)

        return {'data' : response_list}

@ns_youtube.route('/regionCode/<string:regionCode>')
class RegionCode(Resource):
    def get(self,regionCode):
        '''get country name by region code'''
        connecsiObj = ConnecsiModel()
        data = connecsiObj.get__(table_name='youtube_region_codes',STAR='*',WHERE='WHERE',compare_column='regionCode',compare_value=str(regionCode))
        return {'data' : data}

@ns_youtube.route('/videoCategories')
class VideoCategories(Resource):
    def get(self):
        ''' get all video categories'''
        connecsiObj = ConnecsiModel()
        video_categories = connecsiObj.get__(table_name='youtube_video_categories', STAR='*')
        print(video_categories)
        columns = ['video_cat_id','video_cat_name']
        response_list = []
        for item in video_categories:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)

        print(response_list)
        return {'data': response_list}

@ns_youtube.route('/videoCategories/<string:video_cat_id>')
class VideoCategories(Resource):
    def get(self,video_cat_id):
        ''' get video categories by video cat id '''
        connecsiObj = ConnecsiModel()
        video_categories = connecsiObj.get__(table_name='youtube_video_categories', STAR='*',WHERE='WHERE',compare_column='video_cat_id',compare_value=video_cat_id)
        print(video_categories)
        columns = ['video_cat_id','video_cat_name']
        response_list = []
        for item in video_categories:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)

        print(response_list)
        return {'data': response_list}


@ns_youtube.route('/searchChannels/<string:channel>')
class SearchChannels(Resource):
    @ns_youtube.expect(search_channels_form)
    def post(self,channel):
        '''search channels'''
        try:
            form_data = request.get_json()
            category_id = form_data.get('category_id')
            country = form_data.get('country')
            min_lower = form_data.get('min_lower')
            max_upper = form_data.get('max_upper')
            sort_order = form_data.get('sort_order')
            offset = form_data.get('offset')
            connecsiObj=ConnecsiModel()
            if channel == 'youtube' or channel == 'Youtube':
                print('i m inside if')
                total_rows = connecsiObj.search_youtube_inf_get_total_rows(min_lower=str(min_lower), max_upper=str(max_upper)
                                              , category_id=str(category_id), country=str(country), sort_order=sort_order)
                total_no_of_rows = len(total_rows)

                # print('my data = ',total_rows)
                print(total_no_of_rows)
                data = connecsiObj.search_youtube_inf(min_lower=str(min_lower), max_upper=str(max_upper)
                                              ,category_id=str(category_id), country=str(country), sort_order=sort_order,offset=str(offset))
                columns = ['channel_id', 'title','channel_img','desc','subscriberCount_gained','subscriberCount_lost','business_email','total_100video_views',
                           'total_100video_views_unique','total_100video_likes','total_100video_dislikes','total_100video_comments','total_100video_shares',
                           'facebook_url','insta_url','twitter_url','country']
                response_list = []

                # print(type(data))
                # print(data)
                for item in data:
                    # print(item)
                    dict_temp = dict(zip(columns, item))
                    dict_temp.update({'total_rows':total_no_of_rows})
                    response_list.append(dict_temp)
                # print(response_list)
                return {'data':response_list}

            elif channel == 'twitter' or channel == 'Twitter':
                total_rows = connecsiObj.search_twitter_inf_get_total_rows(min_lower=str(min_lower),
                                                                           max_upper=str(max_upper)
                                                                           , category_id=str(category_id),
                                                                           country=str(country), sort_order=sort_order)
                total_no_of_rows = len(total_rows)
                data = connecsiObj.search_twitter_inf(min_lower=str(min_lower), max_upper=str(max_upper)
                                                      , category_id=str(category_id), country=str(country),
                                                      sort_order=sort_order, offset=str(offset))
                columns = ['channel_id','screen_name','title', 'channel_img', 'desc', 'subscriberCount_gained',
                            'business_email', 'total_100video_views',
                            'total_100video_likes',
                           'total_100video_comments', 'total_100video_shares',
                           'facebook_url', 'insta_url','youtube_url', 'twitter_url', 'country']
                response_list = []
                for item in data:
                    dict_temp = dict(zip(columns, item))
                    dict_temp.update({'total_rows': total_no_of_rows})
                    response_list.append(dict_temp)
                # print(response_list)
                return {'data': response_list}

            elif channel == 'instagram' or channel == 'Instagram':
                total_rows = connecsiObj.search_instagram_inf_get_total_rows(min_lower=str(min_lower),
                                                                           max_upper=str(max_upper)
                                                                           , category_id=str(category_id),
                                                                           country=str(country), sort_order=sort_order)
                total_no_of_rows = len(total_rows)
                print('total rows insta  = ',total_no_of_rows)
                data = connecsiObj.search_instagram_inf(min_lower=str(min_lower), max_upper=str(max_upper)
                                                      , category_id=str(category_id), country=str(country),
                                                      sort_order=sort_order, offset=str(offset))
                print(data)
                columns = ['channel_id','username','title', 'channel_img', 'desc', 'subscriberCount_gained',
                            'business_email', 'total_100video_views',
                            'total_100video_likes',
                           'total_100video_comments', 'total_100video_shares',
                           'facebook_url', 'insta_url','youtube_url', 'twitter_url', 'country','total_videos']
                response_list = []
                for item in data:
                    dict_temp = dict(zip(columns, item))
                    dict_temp.update({'total_rows': total_no_of_rows})
                    response_list.append(dict_temp)
                print(response_list)
                return {'data': response_list}
        except Exception as e:
            print('i  m in exception ')
            print(e)
            return {'response' : e}


@ns_youtube.route('/top10Influencers')
class Youtube(Resource):
    def get(self):
        '''get top 10 youtube influencers based on number of subscribers desc'''
        connecsiObj = ConnecsiModel()
        youtube_inf = connecsiObj.getTop10YoutubeInfluencers()
        columns = ['channel_id', 'title', 'channel_img','subscriberCount_gained','total_100video_views','total_100video_likes',
                   'total_100video_comments','total_100video_shares','facebook_url', 'insta_url', 'twitter_url','country','total_videos']
        response_list = []
        for item in youtube_inf:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        return {'data' : response_list}


@ns_youtube.route('/totalVideos/<string:channel_id>')
class TotalVideos(Resource):
    def get(self,channel_id):
        '''get total videos by channel_id'''
        connecsiObj = ConnecsiModel()
        data = connecsiObj.getTotalVideos(channel_id=channel_id)
        response_list = []
        columns=['total_videos']
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        return {'data': response_list}


@ns_youtube.route('/addYoutubeChannel/<string:channel_id>/<string:business_email>')
class Youtube(Resource):
    def post(self,channel_id,business_email):
        '''add youtube channel details by channel_id'''
        try:
            data = [channel_id]
            connecsiObj = ConnecsiModel()
            res = connecsiObj.insert__(data=data, table_name='youtube_channel_ids', columns=['channel_id'],
                                 IGNORE='IGNORE')
            print('res = ',res)
            try:
                connecsiObj.insert_youtube_id_into_channels_mapper(youtube_channel_id=channel_id,confirmed='true')
            except Exception as e:
                print(e)
                return {'message' : e}
            try:
                conObj = YoutubeApiController()
                conObj.get_data_by_channel_id(channel_id=channel_id,business_email=business_email)
                return {'message': 'inserted youtube channel id and details'}
            except Exception as e :
                print('exception = ',e)
                return {'message': e}
        except Exception as e :
            return {'message' : e}



@ns_youtube.route('/getYoutubeChannelSnippetFromYoutubeSearchApi/<string:search_query>')
class Youtube(Resource):
    def get(self,search_query):
        ''' Get youtube channel snippet from youtube Search api
            returns a list of channel ids , title and channel img
        '''
        try:
            print(search_query)
            response_list = []
            channel_ids=[]
            api_key = 'AIzaSyDAwoNaRbQYSl7J_Ll2fztqwT1Gg1ZEMzU'
            search_url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&order=viewCount&q='+search_query+'&type=channel&key='+api_key
            print(search_url)
            channel_data = requests.get(url=search_url)
            channel_data_json = channel_data.json()
            for item in channel_data_json['items']:
                print(item)
                response_dict = {}
                channel_id = item['snippet']['channelId']
                print(channel_id)
                channel_ids.append(channel_id)
                channel_thumbnail = item['snippet']['thumbnails']['medium']['url']
                channelTitle = item['snippet']['title']
                response_dict.update({'channel_id':channel_id})
                response_dict.update({'title': channelTitle})
                response_dict.update({'channel_img': channel_thumbnail})
                response_list.append(response_dict)
            connecsiObj = ConnecsiModel()
            connecsiObj.insert__(table_name='youtube_channel_ids',data=channel_ids,columns=['channel_id'],IGNORE='IGNORE')
            return response_list
        except Exception as e:
            print('exception = ',e)
            return {'message': e}

@ns_youtube.route('/getYoutubeChannelDetailsFromYoutubeApi/<string:channel_id>')
class Youtube(Resource):
    def get(self,channel_id):
        ''' Get youtube channel details by channel_id from youtube api'''
        try:
            data = [channel_id]
            connecsiObj = ConnecsiModel()
            res = connecsiObj.insert__(data=data, table_name='youtube_channel_ids', columns=['channel_id'],
                                 IGNORE='IGNORE')
            print('res = ',res)
            try:
                connecsiObj.insert_youtube_id_into_channels_mapper(youtube_channel_id=channel_id,confirmed='true')
            except Exception as e:
                print(e)
                return {'message' : e}
            try:
                conObj = YoutubeApiController()
                conObj.get_data_by_channel_id(channel_id=channel_id,business_email='')
                connecsiObj = ConnecsiModel()
                columns = ['channel_id', 'title', 'channel_img', 'desc', 'subscriberCount_gained', 'subscriberCount_lost',
                           'business_email', 'total_100video_views',
                           'total_100video_views_unique', 'total_100video_likes', 'total_100video_dislikes',
                           'total_100video_comments', 'total_100video_shares',
                           'facebook_url', 'insta_url', 'twitter_url', 'country']
                channel_details = connecsiObj.get__(table_name='youtube_channel_details', columns=columns, WHERE='WHERE',
                                                    compare_column='channel_id', compare_value=channel_id)
                print(channel_details)

                response_list = []
                for item in channel_details:
                    dict_temp = dict(zip(columns, item))
                    response_list.append(dict_temp)
                print(response_list)
                return {'data': response_list}
            except Exception as e :
                print('exception = ',e)
                return {'message': e}
        except Exception as e :
            return {'message' : e}



@ns_youtube.route('/getChannelDetailsByChannelId/<string:channel_id>')
class Youtube(Resource):
    def get(self,channel_id):
        ''' get channel detail by channel id'''
        connecsiObj = ConnecsiModel()
        columns = ['channel_id', 'title', 'channel_img', 'desc', 'subscriberCount_gained', 'subscriberCount_lost',
                   'business_email', 'total_100video_views',
                   'total_100video_views_unique', 'total_100video_likes', 'total_100video_dislikes',
                   'total_100video_comments', 'total_100video_shares',
                   'facebook_url', 'insta_url', 'twitter_url', 'country']
        channel_details = connecsiObj.get__(table_name='youtube_channel_details',columns=columns,WHERE='WHERE',compare_column='channel_id',compare_value=channel_id)
        print(channel_details)

        response_list = []
        for item in channel_details:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)

        print(response_list)
        return {'data': response_list}


@ns_youtube.route('/getAllVideoDetailsByChannelId/<string:channel_id>')
class Youtube(Resource):
    def get(self,channel_id):
        ''' get video detail by channel id'''
        connecsiObj = ConnecsiModel()
        columns = ['video_id','channel_id','publishedAt','title','thumbnail','tags','category_id',
                   'description','viewCount','likeCount','dislikeCount','favoriteCount','commentCount','shareCount']
        video_details = connecsiObj.get__(table_name='youtube_video_details',columns=columns,WHERE='WHERE',compare_column='channel_id',compare_value=channel_id)
        print(type(video_details))
        video_details_list = list(video_details)
        print(type(video_details_list))
        response_list = []
        for item in video_details_list:
            item_list = list(item)
            item_list[2] = datetime.datetime.timestamp(item_list[2])
            dict_temp = dict(zip(columns, item_list))
            response_list.append(dict_temp)
        # print(response_list)
        return {'data': response_list}


@ns_youtube.route('/getVideoCategoriesByChannelId/<string:channel_id>')
class VideoCategories(Resource):
    def get(self,channel_id):
        ''' get video categories by video cat id '''
        connecsiObj = ConnecsiModel()
        video_categories = connecsiObj.get_youtube_video_categories_id_and_name_by_channel_id(channel_id=channel_id)
        print(video_categories)
        columns = ['channel_id','video_cat_id','video_cat_name','category_count']
        response_list = []
        for item in video_categories:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)

        print(response_list)
        return {'data': response_list}