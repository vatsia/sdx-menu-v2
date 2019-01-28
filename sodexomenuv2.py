from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import redirect, url_for
import sodexo_api_service as sdx
import time

app = Flask(__name__)

## SETTINGS
RESTAURANT_COOKIE_NAME = 'SDX_MENU_v2_REST'
DEFAULT_LANG = 'fi'
# restaurant id : name
AVAILABLE_RESTAURANTS = {
    '31332' : 'HAMK Riihimäki',
    '31314' : 'HAMK Hämeenlinna'
}

## END OF SETTINGS

## LINKS IN NAVIGATION BAR
with app.app_context():
    NAVIGATION_LINKS = {
        # 'controller name'    : 'Link text' 
        'restaurants_index'  : 'Restaurants',
        'info'               : 'Info',
        'destroy_cookie'     : 'Reset default restaurant'
    }

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
    
    menu_json = sdx.get_daily_menu(time.strftime('%d'), time.strftime('%m'), time.strftime('%Y'), DEFAULT_LANG, restaurant_id)
    return render_template('restaurant.html', menu=menu_json, restid=restaurant_id, ck=cookie, navigation_links=NAVIGATION_LINKS)

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