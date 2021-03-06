import urllib.parse

from flask import Flask, request, session
from flask_restx import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_graph_history = Namespace('GraphHistory', description='History details for graphs')

@ns_graph_history.route('/getNoOfFollowersHistory/<string:channel_name>/<string:channel_id>')
class History(Resource):
    def get(self,channel_name,channel_id):
        """get no of followers history by channel name and id"""
        modelObj = ConnecsiModel()
        if channel_name == 'youtube':
            columns = ['channel_id', 'subscriberCount_gained', 'inserted_date']
            channel_history_data = modelObj.get__(table_name='youtube_channels_history', columns=columns,WHERE='WHERE'
                                          ,compare_column='channel_id',compare_value=str(channel_id))
            response_list = []
            response_columns = ['channel_id','no_of_followers','timestamp']
            print(channel_history_data)
            # channel_history_data = list(channel_history_data)
            channel_history_data_list = []
            for item in channel_history_data:
                temp_list = []
                temp_list.append(item[0])
                temp_list.append(item[1])
                timestamp = datetime.datetime.timestamp(item[2])
                temp_list.append(timestamp)
                print('temp list = ',temp_list)
                channel_history_data_list.append(temp_list)
            for item1 in channel_history_data_list:
                dict_temp = dict(zip(response_columns, item1))
                response_list.append(dict_temp)
            return {'data': response_list}

        if channel_name == 'twitter':
            columns = ['twitter_id', 'no_of_followers', 'inserted_date']
            channel_history_data = modelObj.get__(table_name='twitter_channels_history', columns=columns,WHERE='WHERE'
                                          ,compare_column='twitter_id',compare_value=str(channel_id))
            response_list = []
            response_columns = ['twitter_id','no_of_followers','timestamp']
            print(channel_history_data)
            # channel_history_data = list(channel_history_data)
            channel_history_data_list = []
            for item in channel_history_data:
                temp_list = []
                temp_list.append(item[0])
                temp_list.append(item[1])
                timestamp = datetime.datetime.timestamp(item[2])
                temp_list.append(timestamp)
                print('temp list = ',temp_list)
                channel_history_data_list.append(temp_list)
            for item1 in channel_history_data_list:
                dict_temp = dict(zip(response_columns, item1))
                response_list.append(dict_temp)
            return {'data': response_list}

        if channel_name == 'instagram':
            columns = ['insta_id', 'no_of_followers', 'inserted_date']
            channel_history_data = modelObj.get__(table_name='insta_channels_history', columns=columns,WHERE='WHERE'
                                          ,compare_column='insta_id',compare_value=str(channel_id))
            response_list = []
            response_columns = ['insta_id','no_of_followers','timestamp']
            print(channel_history_data)
            # channel_history_data = list(channel_history_data)
            channel_history_data_list = []
            for item in channel_history_data:
                temp_list = []
                temp_list.append(item[0])
                temp_list.append(item[1])
                timestamp = datetime.datetime.timestamp(item[2])
                temp_list.append(timestamp)
                print('temp list = ',temp_list)
                channel_history_data_list.append(temp_list)
            for item1 in channel_history_data_list:
                dict_temp = dict(zip(response_columns, item1))
                response_list.append(dict_temp)
            return {'data': response_list}


