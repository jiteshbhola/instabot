# The following code gets added to the main.py file

import peewee
from Models import *


def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


def add_user_details(insta_username):
    user_id = get_user_id(insta_username)
    request_url = (BASE_URL + 'users/%s/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    response = requests.get(request_url).json()

    if response['meta']['code'] == 200:
        username = response['data']['username']
        full_name = response['data']['full_name']
        follows = response['data']['counts']['follows']
        followed = response['data']['counts']['followed_by']

        query = User.select().where(User.user_id == user_id)
        if len(query) > 0:
            query[0].username = username
            query[0].full_name = full_name
            query[0].follows_count = follows
            query[0].followed_by_count = followed
            query[0].save()

        else:
            new_user = User(user_id=user_id, username=username, full_name=full_name, follows_count=follows,
                            followed_by_count=followed)
            new_user.save()  # Need to Specify force_insert when using manual Primary Keys.

    else:
        exit()


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']) > 0:
            for data_item in user_media['data']:
                media_id = data_item['id']
                media_type = data_item['type']

                media_link = data_item[media_type]['standard_resolution']['url']

                query = Media.select().where(Media.media_id == media_id)
                if len(query) > 0:
                    query[0].media_type = media_type
                    query[0].media_link = media_link
                    query[0].save()

                else:

                    new_media = Media(user_id=user_id, media_id=media_id, media_type=media_type, media_link=media_link)
                    new_media.save()
            return user_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


def add_comments(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']) > 0:
            for index in range(len(user_media['data'])):

                media_id = user_media['data'][index]['id']

                comment_request = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
                print 'GET request url : %s' % (comment_request)
                response = requests.get(comment_request).json()

                if response['meta']['code'] == 200:
                    for index in range(len(response['data'])):
                # Retrieve Comment Details
                # Add to Database


initialize_db()