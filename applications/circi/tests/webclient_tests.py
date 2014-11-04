from gluon.contrib.webclient import WebClient

client = WebClient('http://127.0.0.1:8000/circi/default/',
                   postbacks=True)

client.get('index')
# register
data = dict(first_name='John',
            last_name='Sample',
            email='john@sample.com',
            password='test',
            password_two='test',
            _formname='register')
client.post('user/register', data=data)

# logout
client.get('user/logout')

# login again
data = dict(email='john@sample.com',
            password='test',
            _formname='login')
client.post('user/login', data=data)

# check registration and login were successful
client.get('index')
assert('Welcome John' in client.text)
