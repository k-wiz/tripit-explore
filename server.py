from flask import Flask,redirect, request
app = Flask(__name__)
import tripit
import xmltodict
import os



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

    # get profile info and store validated tokens and tripid user_id in sessions
    oauth_credential = tripit.OAuthConsumerCredential(consumer_key, consumer_secret, authorized_oauth_token, authorized_oauth_token_secret)
    t = tripit.TripIt(oauth_credential, api_url='https://api.tripit.com')

    '''
    t.get_profile()

    profile = xmltodict.parse(t.response)
    user_id = profile['Response']['Profile']['ProfileEmailAddresses']['ProfileEmailAddresses']
    '''
    t.list_trip()
    return "%s" % t.response

if __name__ == '__main__':
    app.run()
