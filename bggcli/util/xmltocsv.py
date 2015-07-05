"""
bgg.xmltocsv
~~~~~~~~~~~~

Utility in charge of converting an XML export to CSV

"""


class _EmptyNode:
    def __init__(self):
        self.text = ''
        self.attrib = {}

    # noinspection PyUnusedLocal
    def find(self, pattern):
        return self

    # noinspection PyUnusedLocal
    def get(self, key):
        return None


class XmlToCsv:
    empty_node = _EmptyNode()
    
    def __init__(self):
        pass

    @staticmethod
    def _wrap(node):
        if node is None:
            return XmlToCsv.empty_node
        return node

    @staticmethod
    def _to_str(value):
        if value is None:
            return ""
        return value.encode('utf8')

    @staticmethod
    def _to_int(value):
        if value is None:
            return "0"
        return value

    @staticmethod
    def _zero_if_na(value):
        if value == 'N/A':
            return 0
        return value

    # noinspection PyTypeChecker
    @staticmethod
    def convert_item(el):
        # Language is not exported for custom version!
    
        status_atts = XmlToCsv._wrap(el.find('status')).attrib
        version_el = XmlToCsv._wrap(el.find('version'))
        private_info_el = XmlToCsv._wrap(el.find('privateinfo'))

        publisher_atts = XmlToCsv._wrap(version_el.find('publisher')).attrib
    
        return {
            'objectname': XmlToCsv._to_str(el.find('name').text),
            'objectid': el.attrib.get('objectid'),
            'rating': XmlToCsv._zero_if_na(XmlToCsv._wrap(el.find('stats/rating')).get('value')),
            'own': XmlToCsv._to_int(status_atts.get('own')),
            'fortrade': XmlToCsv._to_int(status_atts.get('fortrade')),
            'want': XmlToCsv._to_int(status_atts.get('want')),
            'wanttobuy': XmlToCsv._to_int(status_atts.get('wanttobuy')),
            'wanttoplay': XmlToCsv._to_int(status_atts.get('wanttoplay')),
            'prevowned': XmlToCsv._to_int(status_atts.get('prevowned')),
            'preordered': XmlToCsv._to_int(status_atts.get('preordered')),
            'wishlist': XmlToCsv._to_int(status_atts.get('wishlist')),
            'wishlistpriority': XmlToCsv._to_str(status_atts.get('wishlistpriority')),
            'wishlistcomment': XmlToCsv._to_str(XmlToCsv._wrap(el.find('wishlistcomment')).text),
            'comment': XmlToCsv._to_str(XmlToCsv._wrap(el.find('comment')).text),
            'conditiontext': XmlToCsv._to_str(XmlToCsv._wrap(el.find('conditiontext')).text),
            'haspartslist': XmlToCsv._to_str(XmlToCsv._wrap(el.find('haspartslist')).text),
            'wantpartslist': XmlToCsv._to_str(XmlToCsv._wrap(el.find('wantpartslist')).text),
            'publisherid': XmlToCsv._to_str(publisher_atts.get('publisherid')),
            'year': XmlToCsv._to_str(XmlToCsv._wrap(version_el.find('year')).text),
            'imageid': XmlToCsv._to_str(XmlToCsv._wrap(version_el.find('imageid')).get('value')),
            'other': XmlToCsv._to_str(XmlToCsv._wrap(version_el.find('other')).text),
            'pricepaid': XmlToCsv._to_str(private_info_el.get('pricepaid')),
            'pp_currency': XmlToCsv._to_str(private_info_el.get('pp_currency')),
            'currvalue': XmlToCsv._to_str(private_info_el.get('currvalue')),
            'cv_currency': XmlToCsv._to_str(private_info_el.get('cv_currency')),
            'acquisitiondate': XmlToCsv._to_str(private_info_el.get('acquisitiondate')),
            'acquiredfrom': XmlToCsv._to_str(private_info_el.get('acquiredfrom')),
            'quantity': XmlToCsv._to_str(private_info_el.get('quantity')),
            'privatecomment': XmlToCsv._to_str(private_info_el.find('privatecomment').text),
            '_versionid': XmlToCsv._to_str(XmlToCsv._wrap(version_el.find('item')).get('id'))
        }
