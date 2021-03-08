# Auth Test Service

This is a test Flask/Connexion Python3 app to implement and test the OAUTH2
authentication theme using Google as Authorization Server (provider).

It has been inspired by 
[Create a Flask Application With Google Login (realpython.com)](https://realpython.com/flask-google-login/).
but has been adapted to the author's current way of building web apps.

Adaptations:

* use SQLAlchemy + SQLITE DB
* include in a `connexion` rendered API (OpenAPI3)
* use `create_app()` factory function instead of global `app`


## Start the App

### Pre-Requisites

Create a *client ID* and *client secret* in your Google account:
[Create a Google Client](https://realpython.com/flask-google-login/#creating-a-google-client)

Also, you must run the app server using HTTPS. To allow this make sure you
have `pyOpenSSL` installed.

Further, before first use you must initialize the database:
```shell
$ export FLASK_APP=/absolute/path/to/auth_flask_app.py 
$ export FLASK_ENV=development
$ flask db init
$ flask db migrate -m 'user table'
$ flask db upgrade
```


### Start Commands
```shell
$ export GOOGLE_CLIENT_ID=<id> 
$ export GOOGLE_CLIENT_SECRET=<secret> 
$ export FLASK_APP=/absolute/path/to/auth_flask_app.py 
$ export FLASK_ENV=development
$ flask run --cert='adhoc'
```

The server now uses a self-signed SSL certificate. 
When you hit [https://localhost:5000/](https://localhost:5000/), your browser will display a warning,
telling you that the connection is not secure.
You must accept this for the time being.


### Geberate a Certificate for Development

Run this command to generate a personal certifciate.
This is not much better than the ad-hoc version but at least it is not changing
with every ``flask run`` command:

```shell
$ openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

And then change the start command to

```shell
$ export GOOGLE_CLIENT_ID=<id> 
$ export GOOGLE_CLIENT_SECRET=<secret> 
$ export FLASK_APP=/absolute/path/to/auth_flask_app.py 
$ export FLASK_ENV=development
$ flask run --cert=cert.pem --key=key.pem
```


## Improvements & TODOs

- [ ] (***HIGH PRIO***) Connexion endpoints not yet protected with OAUTH2 or JWT or ...
- [ ] Create your own certificate:
  [Running your Flask App over HTTPS (M. Grinberg)](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https)
- [ ] Check if `app_context` context manager in `__init__.register_blueprints` is necessary at all? 
  `register_blueprint()` takes care of binding it to the `app_context`, or not?
- [ ] Check what `UserMixin` does.

## Contact

* [philipp.westphal@gmx.net](mailto:philipp.westphal@gmx.net)
