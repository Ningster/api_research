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

def page_FB_data(page_id):
    # input: facebook page id, output: [dict] facebook page data set with specified fields
    page_data = graph.request('/'+page_id,{'fields':'is_community_page'+','+'category'})
    return page_data

def search_FB_ID(restaurant_name):
    # input: restaurant name, output: [json] the ID/name of the restaurant business facebook fanpage of given restaurant name
    FB_search_results_by_name=graph.request('/search',{'q':restaurant_name,'type':'page'})['data']
    valid_FB_page = {restaurant_name:[]}
    for page in FB_search_results_by_name:    #page type: dictionary
        page_name = page['name']
        page_id = page['id']
        page_data = page_FB_data(page_id)
        is_community_page=page_data['is_community_page']
        category=page_data['category']
        if not is_community_page and category=="Restaurant/Cafe":
            valid_FB_page[restaurant_name].append(page)
    return valid_FB_page


def search_yelp_term(term):
        params={
        'term':term,
        'cc':'TW',
        'limit':20,
        'offset':20,
        'sort':0
        }
        results = client.search('taipei',**params)
        yelp_restaurant_name=[]
        for restaurant in results.businesses:
            name = restaurant.name.encode('utf8')
            yelp_restaurant_name.append(name)
        return yelp_restaurant_name

def name_match_id(request):
    if request.method == 'GET' and request.GET['term'] != '':
        term=request.GET['term']
        restaurant_name_list=search_yelp_term(term)
        results = []
        for restaurant_name in restaurant_name_list:
            print restaurant_name
            fb_page_dict=search_FB_ID(restaurant_name)
            print fb_page_dict
            results.append(fb_page_dict)
        return JsonResponse({'data':results})
    else:
        return JsonResponse({'request':False})
