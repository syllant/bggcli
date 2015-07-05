import os

if os.environ.get('CI') == 'true':
    # Issues with Sauce Labs and HTTPS
    BGG_BASE_URL = "http://www.boardgamegeek.com"
else:
    BGG_BASE_URL = "http://www.boardgamegeek.com"

UI_ERROR_MSG = "Unexpected error while controlling the UI!\nEither the web pages have " \
               "changed and bggcli must be updated, or the site is down for " \
               "maintenance."

BGG_SUPPORTED_FIELDS = ['objectname', 'objectid', 'rating', 'own',
                        'fortrade', 'want', 'wanttobuy', 'wanttoplay', 'prevowned',
                        'preordered', 'wishlist', 'wishlistpriority', 'wishlistcomment',
                        'comment', 'conditiontext', 'haspartslist', 'wantpartslist',
                        'publisherid', 'imageid', 'year', 'language', 'other', 'pricepaid',
                        'pp_currency', 'currvalue', 'cv_currency', 'acquisitiondate',
                        'acquiredfrom', 'quantity', 'privatecomment',
                        '_versionid']
