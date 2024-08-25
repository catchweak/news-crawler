
from datetime import datetime

def iso_to_datetime(iso_string):
    """
    ISO 8601 문자열을 MySQL DATETIME 형식으로 변환
    """
    if iso_string:
        return datetime.strptime(iso_string.replace('Z', '+00:00'), '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S')
    return None