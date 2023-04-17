import datetime
from os.path import splitext


def get_timestamp_path(instance, filename):
    return '{!s:s}{!s:s}'.format(datetime.now().timestamp(), splitext(filename)[1])
