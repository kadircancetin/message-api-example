INFORMATION
===========
- [x] Login -  Logout
- [x] Messageing
- [x] Read old messages
- [x] Block - Unblock User
- [x] User activity logs (SIGN_UP, BLOCK, UN_BLOCK, MESSAGE_SEND, VALID_LOGIN, INVALID_LOGIN)
- [x] Server error and info logging (on ./log_file)
- [x] Message readtime
- [x] **%95** test covearage
- [ ] Dependency Injection

INSTALLATION
============

For installation:

```
pip install -r requirements.txt
python manage.py migrate
```

For run:

```
python manage.py runserver
```

API INFO
============
Content type should be json and specify on the header like `Content-Type: application/json`. Authentication is token based and `Authorization: Token xxxxxxxxxxxxxxx` should be on header.

END POINTS
============
## POST **/user/register/** (auth not required)
- 201 if success
- 400 if unseccess

example input
```
{"password": "specialPassword",
 "username": "kahredici"}
```
example output
```
{"username": "kahredic"}
```

## POST **/user/login/** (auth not required)
- 200 if success
- 400 if unseccess

input:
```
{"password": "specialPassword",
  "username": "kahredici"}
```
output:
```
{"token": "b4b88b698f5f40f4716194ce632edc66cb374b30"}
```

##  POST **/user/block/_username_/**
- 201 if success
- 401 if not auth

input:
```
{}
```
output:
```
{}
```
##  POST **/user/unblock/_username_/**
- 204 if success
- 401 if not auth

input:
```
{}
```
output:
```
{}
```
##  GET **/message/_username_/**
- 200 if success
- 401 if not auth
input
```
{}
```
output
```
{
  "results": [
    {
      "read_datetime": "2020-09-03T08:09:43.986559Z",
      "creation_datetime": "2020-09-03T08:04:18.145304Z",
      "content": "message str",
      "reciever": 1,
      "sender": 2,
      "id": 32
    },
    {
      "read_datetime": "2020-09-03T08:09:43.986559Z",
      "creation_datetime": "2020-09-03T08:04:17.560689Z",
      "content": "other message str",
      "reciever": 1,
      "sender": 2,
      "id": 31
    },
    ...
    ...
    ...
  ],
  "previous": null,
  "next": "http://localhost:8000/message/kahredici/?page=2",
  "count": 32
}
```

##  POST **/message/_username_/**
- 201 if success
- 401 if not auth
input:
```
{"content": "son"}
```
output:
```
{
  "read_datetime": null,
  "creation_datetime": "2020-09-03T08:12:10.760949Z",
  "content": "son",
  "reciever": 1,
  "sender": 1,
  "id": 33
}
```


TEST COVARAGE
=============
```
>> pip install coverage

>> coverage run --source='.' manage.py test

>> coverage report

Name                                               Stmts   Miss  Cover
----------------------------------------------------------------------
core/tests.py                                         13      0   100%
logs/__init__.py                                       0      0   100%
logs/admin.py                                          1      0   100%
logs/apps.py                                           3      3     0%
logs/migrations/0001_initial.py                        7      0   100%
logs/migrations/__init__.py                            0      0   100%
logs/models.py                                        14      0   100%
logs/tests.py                                          1      0   100%
logs/views.py                                          1      1     0%
manage.py                                             12      2    83%
message/__init__.py                                    0      0   100%
message/apps.py                                        3      3     0%
message/factories.py                                   9      0   100%
message/migrations/0001_initial.py                     7      0   100%
message/migrations/0002_auto_20200902_0840.py          4      0   100%
message/migrations/0003_message_read_datetime.py       4      0   100%
message/migrations/__init__.py                         0      0   100%
message/models.py                                     12      1    92%
message/serializers.py                                21      0   100%
message/tests.py                                      77      0   100%
message/views.py                                      27      0   100%
project/__init__.py                                    0      0   100%
project/asgi.py                                        4      4     0%
project/settings.py                                   20      0   100%
project/urls.py                                        5      0   100%
project/wsgi.py                                        4      4     0%
users/__init__.py                                      0      0   100%
users/apps.py                                          3      3     0%
users/factories.py                                    15      0   100%
users/migrations/0001_initial.py                       7      0   100%
users/migrations/__init__.py                           0      0   100%
users/models.py                                        4      0   100%
users/serializers.py                                  17      0   100%
users/tests.py                                       128      0   100%
users/views.py                                        60      1    98%
----------------------------------------------------------------------
TOTAL                                                483     22    95%
```
