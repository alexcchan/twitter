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
}
