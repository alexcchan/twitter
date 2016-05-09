"""
API Mapping for Twitter API 1.1
"""

mapping_table = {

    'content_type': 'application/json',
    'path_prefix': '/1.1',

    'search_tweets' : {
        'path': '/search/tweets.json',
        'valid_params': ['q'],
    },

    'show_status' : {
        'path': '/statuses/show.json',
        'valid_params': ['id'],
    },

    'destroy_status': {
        'method': 'POST',
        'path': '/statuses/destroy/{{id}}.json',
        'valid_params': ['trim_user'],
    },

    'get_user_timeline': {
        'path': '/statuses/user_timeline.json',
        'valid_params': ['user_id','screen_name','since_id','count','max_id','trim_user','exclude_replies','contributor_details','include_rts',],
    },

    'get_friends': {
        'path': '/friends/list.json',
        'valid_params': ['user_id','screen_name','cursor','count','skip_status','include_user_entities'],
    },

    'get_followers': {
        'path': '/followers/list.json',
        'valid_params': ['user_id','screen_name','cursor','count','skip_status','include_user_entities'],
    },

}
