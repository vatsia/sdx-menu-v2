import urllib.request
import json
import time

API_BASE_URI = 'https://www.sodexo.fi/ruokalistat/output/daily_json/'
LANG = 'fi'
DEFAULT_LOCATION_ID = '31332'

def get_daily_menu(dd, mm, yyyy, lang, location):
    data = fetch_data_from_api(dd, mm, yyyy, lang, location)
    parsed = json.loads(data)
    return parsed

def fetch_data_from_api(dd, mm, yyyy, lang, location):
    req = urllib.request.Request(construct_uri(lang, location, dd, mm, yyyy))
    resp = ''
    try:
        resp = urllib.request.urlopen(req)
    except urllib.error.HTTPError as http_e:
        print("HTTPError: " + http_e)

    return resp.read()

def construct_uri(lang, location_id, day, month, year):
    return API_BASE_URI + location_id + '/' + year + '/' + month + '/' + day + '/' + lang

########## TESTS
def test_is_construct_uri_working():
    uri = construct_uri('fi', '31332', '01', '01', '1970')
    return uri == 'https://www.sodexo.fi/ruokalistat/output/daily_json/31332/1970/01/01/fi'

def test_fetch_data_from_api_returns_something():
    content = fetch_data_from_api(LANG, DEFAULT_LOCATION_ID, time.strftime('%d'), time.strftime('%m'), time.strftime('%Y'))
    return len(content) > 0

########## END OF TESTS

def test():
    print("Running tests")
    print("test_is_construct_uri_working: ")
    if test_is_construct_uri_working():
        print("OK")
    else:
        print("FAIL")

    print("test_fetch_data_from_api_returns_something: ")
    if test_fetch_data_from_api_returns_something():
        print("OK")
    else:
        print("FAIL")

    print(get_daily_menu('21', '01', '2019', 'fi', '31332'))

if __name__ == '__main__':
    test()
