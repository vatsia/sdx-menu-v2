from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import redirect, url_for
from flask_scss import Scss
from werkzeug.contrib.cache import SimpleCache
import sodexo_api_service as sdx
import time

app = Flask(__name__)
cache = SimpleCache()
Scss(app, static_dir='static', asset_dir='assets')
## SETTINGS
RESTAURANT_COOKIE_NAME = 'SDX_MENU_v2_REST'
DEFAULT_LANG = 'fi'

AVAILABLE_RESTAURANTS = {
    # 'id'  : 'name'
    '31332' : ['HAMK Riihimäki RoBotti', "050 439 4525", "HAMK.riihimaki.FMS.FI@sodexo.com","Kaartokatu 2", "11100 Riihimäki", ["Ma-Pe", "07.45 - 16.00", "La-Su", "suljettu"],[["Aamupala", "Ma-Pe", "08.00 - 09.30 ","La-Su", "suljettu "],["Kahvila","Ma-Pe", "07.45 - 16.00","La-Su", "suljettu"],["Lounasajat","Ma-Pe", "10.30 - 13.30","La-Su", "suljettu"]],"Huom! Monimuoto-opiskelu viikonloppuisin( koskee perjantai-illan ja lauantain aukioloaikoja) olemme avoinna perjantaisin klo 19.00 asti ja lauantaina ravintola on avoinna klo 8:00 - 13:30(lounas klo 11.00-12.30)." ],
    '31314' : ['HAMK Hämeenlinna', "050 400 1747", "HAMK.korkeakoulukeskus.FMS.FI@sodexo.com", "Visamäentie 35", "13500 Hämeenlinna", ["Ma-Pe", "07.45 - 16.00", "La-Su", "suljettu"],[["Aamupala","Ma-Pe", "07.45 - 10.00","La-Su", "suljettu"],["Kahvila","Ma-Pe", "07.45 - 18.00","La-Su", "suljettu"],["Lounasajat","Ma-Pe", "10.30 - 14.00","La-Su", "suljettu"]], "Huom! Monimuoto-opiskelu viikonloppuisin (listattuna alle) olemme auki perjantai-iltana klo 19 asti ja lauantaina kahvila on auki klo 8:00 - 15:00, lounasta 11.00-12.30. Kahvilan palvelut on sijoitettu viikonloppuna ravintolan linjastoon. Olemme auki: 26.1., 9.2., 3.2., 9.3., 23.3., 6.4., 13.4"],
}               # 0                   1                 2                                           3                   4                   5 0     5 1             5 2       5 3               6 0 0       601                 602                 610         611                 612             620         621                     622                               7

## END OF SETTINGS

## LINKS IN NAVIGATION BAR
NAVIGATION_LINKS = {
    # 'controller name'    : 'Link text' 
    'restaurants_index'  : 'Restaurants',
    'info'               : 'Info',
    'destroy_cookie'     : 'Reset default restaurant'
}

# enable caching for api requests
def get_menu_from_cache(restaurant_id, day, month, year):
    cached_menu = cache.get(str(day) + str(month) + str(year) + "-" + str(restaurant_id) + "-menu")
    if cached_menu is None:
        cached_menu = sdx.get_daily_menu(day, month, year, DEFAULT_LANG, restaurant_id)
        cache.set(str(day) + str(month) + str(year) + "-" + str(restaurant_id) + "-menu", cached_menu, timeout=5 * 60)
    return cached_menu

# index-page; if no session set, redirect to restaurant -page
@app.route('/')
def index():
    rs_id = 0
    
    try:
        rs_id = request.cookies.get(RESTAURANT_COOKIE_NAME)
    except KeyError:
        rs_id = -1

    if rs_id == None or int(rs_id) < 0:
        # cookie not found, show restaurant listing
        return redirect(url_for('restaurants_index'))
    else:
        # cookie found, redirect to restaurant menu
        return redirect(url_for('restaurant_menu', restaurant_id=rs_id))

# restaurants
@app.route('/restaurants')
def restaurants_index():
    return render_template('restaurant_listing.html', restaurants=AVAILABLE_RESTAURANTS, navigation_links=NAVIGATION_LINKS)

# restaurant-page, a.k.a menu for the day
@app.route('/restaurant/<restaurant_id>')
def restaurant_menu(restaurant_id):
    cookie = -1
    raw_cookie = request.cookies.get(RESTAURANT_COOKIE_NAME)
    if raw_cookie != None:
        cookie = int(raw_cookie)
    
    menu_json = get_menu_from_cache(restaurant_id, time.strftime('%d'), time.strftime('%m'), time.strftime('%Y'))
    return render_template('restaurant.html', menu=menu_json, restid=restaurant_id, ck=cookie, navigation_links=NAVIGATION_LINKS, restaurants=AVAILABLE_RESTAURANTS)

# set default restaurant cookie
@app.route('/restaurant/<restaurant_id>/setdefault')
def set_default_restaurant(restaurant_id):
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie(RESTAURANT_COOKIE_NAME, restaurant_id)
    return resp

# info-page
@app.route('/info')
def info():
    return render_template('info.html', navigation_links=NAVIGATION_LINKS)

# make cookie null
@app.route('/destroy_cookie')
def destroy_cookie():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie(RESTAURANT_COOKIE_NAME, '-1')
    return resp

## ERROR HANDLERS
@app.errorhandler(404)
def errorhandler_not_found(err):
    return render_template('err_not_found.html', navigation_links=NAVIGATION_LINKS)

@app.errorhandler(500)
def errorhandler_internal_server_error(err):
    return render_template('err_internal_server_error.html', navigation_links=NAVIGATION_LINKS)