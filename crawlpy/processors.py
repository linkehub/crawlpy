from six import string_types
from crawlpy import parsers
from w3lib.html import remove_tags

from .tools.api import send_to_api


class DefaultInputProcessor(object):
    
    def __call__(self, values):
        try:
            new_values = []
            for value in values:
                value = self._clear_value(value)
                if value is not None and value != u'':
                    new_values.append(value)
            return new_values
        except:
            return values

    def _clear_value(self, value):
        if isinstance(value, string_types):
            unicode = lambda s: str(s)
            try:
                cleared_value = unicode(remove_tags(value))
                return parsers.normalize_spaces(cleared_value)
            except:
                return value
        else:
            return value


class DefaultOutputProcessor(object):

    def __call__(self, values):
        try:
            if isinstance(values, string_types):
                return unicode(values).strip()
            elif len(values) > 1:
                return u' '.join(unicode(v).strip() for v in values)
            else:
                return values[0]
        except:
            return values


class TakeLast(object):
    
    def __call__(self, values):
        for value in reversed(values):
            if value is not None and value != '':
                return value


class HandleAPI(object):

    def __init__(self, cursor):
        self.items = self.config(cursor)

    def send(self):
        send_to_api(self.items, '/job/create/', 'post')

    def config(self, cursor):
        return [item for item in cursor]
