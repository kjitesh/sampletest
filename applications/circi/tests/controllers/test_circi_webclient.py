#!/usr/bin/env python


def test_tweet_posting(client, web2py):
    '''tweet posting test
    '''

    #client.get('/default/user/register') # get a page
    #register a user
    data = dict(first_name='Homer',
                last_name='Simpson',
                email='homer@simpson.com',
                password='test',
                password_two='test')
    client.post('/default/user/register', data=data)

    assert "Super Awesome Twitter in Web2py" in client.text


def register_new_user(client):
    data = dict(first_name='Homer2',
                last_name='Simpson',
                email='homer2@simpson.com',
                password='test',
                password_two='test')
    client.post('/default/user/register', data=data)

   
def test_validate_new_person(client, web2py):
    '''Is the form validating?
    '''
    register_new_user(client)

    data = dict(body='',)
    client.post('/tweet/home', data=data) # post tweet
    assert client.status == 200

    #assert 'Enter from 1 to 140 characters' in client.text

    assert web2py.db(web2py.db.tweets).count() == 0


