import urllib.request
import json
import time

API_BASE_URI = 'https://www.sodexo.fi/ruokalistat/output/daily_json/'
LANG = 'fi'
DEFAULT_LOCATION_ID = '31332'

# time variables for performance testing
interaction_start = 0
interaction_end = 0

def get_daily_menu(dd, mm, yyyy, lang, location):
    data = str(fetch_data_from_api(dd, mm, yyyy, lang, location))
    parsed = json.loads(data)
    return parsed

def fetch_data_from_api(dd, mm, yyyy, lang, location):
    interaction_start = time.gmtime()
    req = urllib.request.Request(construct_uri(lang, location, dd, mm, yyyy))
    resp = ''
    try:
        resp = urllib.request.urlopen(req)
    except urllib.error.HTTPError as http_e:
        print("HTTPError: " + http_e)

    interaction_end = time.gmtime()
    return resp.read().decode('utf-8')

def construct_uri(lang, location_id, day, month, year):
    return API_BASE_URI + location_id + '/' + year + '/' + month + '/' + day + '/' + lang

## FUNCTION FOR CHECKING PERFORMANCE
def get_interaction_time():
    return interaction_end - interaction_start

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
        print("Interaction_time: " + str(get_interaction_time()))
    else:
        print("FAIL")

    print(get_daily_menu('21', '01', '2019', 'fi', '31332'))

if __name__ == '__main__':
    test()