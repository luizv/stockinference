import time
import datetime

class SIDatetimeFormatter:

    @staticmethod
    def stringToTimestamp(data_string):
        return time.mktime(datetime.datetime.strptime(data_string, "%Y-%m-%d %H:%M:%S").timetuple())

    @staticmethod
    def timestampToString(timestamp):
        print(timestamp)
        d = datetime.datetime.fromtimestamp(timestamp)
        return d.strftime("%Y-%m-%d %H:%M:%S")