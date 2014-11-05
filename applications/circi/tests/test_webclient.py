from gluon.contrib.webclient import WebClient
import logging
import time

logging.basicConfig(level=logging.DEBUG)

def register(client):
    """Helper function for registration functionality"""
    client.get('default/user/register')
    data = dict(first_name='John',
                last_name='Sample',
                email='john@sample.com',
                password='test',
                password_two='test',
                _formname='register')
    client.post('default/user/register', data=data)

def test_registration():
    client = WebClient('http://127.0.0.1:8000/circi/',
                       postbacks=True)

    # register
    register(client)

    # logout
    client.get('default/user/logout')

    # login again
    data = dict(email='john@sample.com',
                password='test',
                _formname='login')
    client.post('default/user/login', data=data)

    # check registration and login were successful
    client.get('default/index')
    assert('Welcome John' in client.text)

def test_tweeting():
    client = WebClient('http://127.0.0.1:8000/circi/',
                       postbacks=True)
    tweet_text = "This is test tweet"

    # register
    register(client)

    assert('Welcome John' in client.text)
    client.get('tweet/home')
    logging.debug(client.url)
    tweet_data = dict(body=tweet_text,)
    client.post('tweet/home', tweet_data)

    #check tweet is posted on home page
    client.get('tweet/home')
    logging.debug(client.text)
    assert(tweet_text in client.text)

def test_wall():
    client = WebClient('http://127.0.0.1:8000/circi/',
                       postbacks=True)
    # register
    register(client)
    client.get('tweet/home')
    tweet_text = "This is test wall tweet"
    tweet_data = dict(body=tweet_text)
    client.post('tweet/home', tweet_data)
    #check tweet on wall page
    client.get('tweet/wall')
    logging.debug(client.text)
    #check we are on profile page
    assert("Profile" in client.text)
    #check tweet is appearing on this page
    assert(tweet_text in client.text)

def test_home_reqires_login():
    """Test if home page asking for login if not already logged in"""
    client = WebClient('http://127.0.0.1:8000/circi/',
                       postbacks=True)

    client.get('tweet/home')
    assert("Login" in client.text)
