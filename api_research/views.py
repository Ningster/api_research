# -*- coding: utf8 -*-
# coding: utf8
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
import json
import facebook
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io
import uniout

#yelp api
with io.open('config_secret_yelp.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

#graph api
with io.open('config_secret_fb.json') as cred_fb:
    creds = json.load(cred_fb)
    graph = facebook.GraphAPI(access_token=creds['access_token'])

def main(request):
    return render_to_response('index.html')

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def page_FB_data(page_id):
    # input: facebook page id, output: [facebook response] facebook page data set with specified fields
    page_data = graph.request('/'+page_id,{'fields':'is_community_page'+','+'category'+','+'location'})
    return page_data

def search_FB_ID(business):
    # input: yelp business dict, output: [list] contains all valid facebook page in dict format
    business_name = business['yelp_name']
    FB_search_results_by_name=graph.request('/search',{'q':business_name,'type':'page'})['data']
    valid_FB_page = []
    for page in FB_search_results_by_name:    #page type: dictionary
        page_name = page['name']
        # print page_name
        page_id = page['id']
        page_data = page_FB_data(page_id)
        is_community_page=page_data['is_community_page']
        if not is_community_page:
            try:
                fb_latitude=page_data['location']['latitude']
                fb_longitude=page_data['location']['longitude']
                if truncate(fb_latitude,2)==business['yelp_coordinate']['latitude'] and truncate(fb_longitude,2)==business['yelp_coordinate']['longitude']:
                    fb_business_dict = {'fb_name':page_name,'fb_id':page_id}
                    valid_FB_page.append(fb_business_dict)
            except Exception as e:
                print(e)
    return valid_FB_page

def search_yelp_category(category):
        params={
        'category_filter':category,
        'cc':'TW',
        'limit':3,
        'sort':0
        }
        results = client.search('taipei',**params)
        yelp_business_list=[]
        for business in results.businesses:
            name = business.name.encode('utf8')
            location_latitude = truncate(business.location.coordinate.latitude,2)
            location_longitude = truncate(business.location.coordinate.longitude,2)
            business_dict = {'yelp_name':name,'yelp_coordinate':{'latitude':location_latitude,'longitude':location_longitude}}
            yelp_business_list.append(business_dict)
        return yelp_business_list

def name_match_id(request):
    if request.method == 'GET' and request.GET['category'] != '':
        category=request.GET['category']
        yelp_business_list=search_yelp_category(category)
        results = []
        for business in yelp_business_list:
            print business['yelp_name']
            valid_fb_page_list=search_FB_ID(business)
            # yelp_fb_match_dict = {'yelp_name':business['yelp_name'],'fb_page':valid_fb_page_list}
            fb_id = []
            for page in valid_fb_page_list:
                fb_id.append(page['fb_id'])
            yelp_fb_match_dict = {'yelp_name':business['yelp_name'],'fb_id':fb_id}
            results.append(yelp_fb_match_dict)
        return JsonResponse({'data':results})
    else:
        return JsonResponse({'request':False})
