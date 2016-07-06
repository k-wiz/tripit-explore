from flask import Flask,redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from bs4 import BeautifulSoup
from jinja2 import StrictUndefined
from model import connect_to_db, db
import tripit
import xmltodict
import os

app = Flask(__name__)
app.secret_key = "efi8y9jduyo2"
app.jinja_env.undefined = StrictUndefined




#Import consumer credentials.
consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']

#Generate request token.
oauth_credential = tripit.OAuthConsumerCredential(oauth_consumer_key=consumer_key, oauth_consumer_secret=consumer_secret)
t = tripit.TripIt(oauth_credential)
token_data = t.get_request_token()

#Generate oauth token.
oauth_token = token_data["oauth_token"]
oauth_token_secret = token_data["oauth_token_secret"]




@app.route('/')
def hello():
    return redirect('https://www.tripit.com/oauth/authorize?oauth_token=%s&oauth_callback=http://127.0.0.1:5000/callback/?oauth_token_secret=%s&' % (oauth_token, oauth_token_secret))



@app.route('/callback/')
def process_token():
    oauth_token = request.args.get('oauth_token')
    oauth_token_secret = request.args.get('oauth_token_secret')


    oauth_credential = tripit.OAuthConsumerCredential(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    t = tripit.TripIt(oauth_credential, api_url='https://api.tripit.com')
    tokens = t.get_access_token()

    authorized_oauth_token = tokens["oauth_token"]
    authorized_oauth_token_secret = tokens["oauth_token_secret"]

    # Get profile info and store validated tokens and tripid user_id in sessions
    oauth_credential = tripit.OAuthConsumerCredential(consumer_key, consumer_secret, authorized_oauth_token, authorized_oauth_token_secret)
    t = tripit.TripIt(oauth_credential, api_url='https://api.tripit.com')
    t.list_trip()

    # Parse API response. 
    soup = BeautifulSoup(t.response, "lxml")
    start_date = soup.trip.start_date.string
    print "TRIP START_DATE", start_date
    end_date = soup.trip.end_date.string
    print "TRIP END_DATE", end_date
    trip_name = soup.trip.display_name.string
    print "TRIP NAME", trip_name
    location = soup.trip.primary_location.string
    print "TRIP LOCATION", location

    # Print list of all trips. 
    # For trip object in trips, print name, location, start_date, end_date
    print "ALL TRIPS", soup.find_all('trip')
    trips = soup.find_all('trip')

    for trip in trips:
        start_date = trip.start_date.string
        print "TRIP START_DATE", start_date
        end_date = trip.end_date.string
        print "TRIP END_DATE", end_date
        trip_name = trip.display_name.string
        print "TRIP NAME", trip_name
        location = trip.primary_location.string
        print "TRIP LOCATION", location


    
    return "Your trip, %s, to %s starts on %s and ends on %s" % (trip_name, 
                                                                location,
                                                                start_date,
                                                                end_date)


if __name__ == "__main__":

    app.debug = True
    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
