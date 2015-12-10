APP_SECRET_KEY = 'fake'
VERSION = 'v0.1' # Arbitrary string identifying the service (will be returned in the headers)

# these are pointing to the ADS sandbox application
ORCID_OAUTH_ENDPOINT = 'https://api.sandbox.orcid.org/oauth/token'
ORCID_API_ENDPOINT = 'https://api.sandbox.orcid.org/v1.2'
ORCID_CLIENT_ID = 'APP-P5ANJTQRRTMA6GXZ'
ORCID_CLIENT_SECRET = '989e54c8-7093-4128-935f-30c19ed9158c'

SQLALCHEMY_BINDS = {
    'orcid':        'sqlite:///'
}
SQLALCHEMY_ECHO = False

ORCID_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s\t%(process)d '
                      '[%(asctime)s]:\t%(message)s',
            'datefmt': '%m/%d/%Y %H:%M:%S',
        }
    },
    'handlers': {
        'file': {
            'formatter': 'default',
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/tmp/orcid_service_app.log',
        },
        'console': {
            'formatter': 'default',
            'level': 'INFO',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
