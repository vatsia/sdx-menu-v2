from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import redirect, url_for

app = Flask(__name__)

## SETTINGS
RESTAURANT_COOKIE_NAME = 'SDX_MENU_v2_REST'

# index-page; if no session set, redirect to restaurant -page
@app.route('/')
def index():
    rs_id = 0
    
    try:
        rs_id = request.cookies.get(RESTAURANT_COOKIE_NAME)
    except KeyError:
        rs_id = -1

    if rs_id == None or rs_id < 0:
        # cookie not found, show restaurant listing
        return redirect(url_for('restaurants_index'))
    else:
        # cookie found, redirect to restaurant menu
        return redirect(url_for('restaurant_menu', restaurant_id=rs_id))
    

# restaurants
@app.route('/restaurants')
def restaurants_index():
    return render_template('restaurant_listing.html')

# restaurant-page, a.k.a menu for the day
@app.route('/restaurant/<restaurant_id>')
def restaurant_menu(restaurant_id):
    return render_template('restaurant.html')

# info-page
@app.route('/info')
def info():
    return render_template('info.html')

# make cookie null
@app.route('/destroy_cookie')
def destroy_cookie():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie(RESTAURANT_COOKIE_NAME, '-1')
    return resp