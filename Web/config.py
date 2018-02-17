WTF_CSRF_ENABLED = True
SECRET_KEY = 'watchdog-secret-key'
#SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@localhost:3306/watchdog'
SQLALCHEMY_DATABASE_URI = 'mysql://aravindbs@watchdogserver:Watchdog123@watchdogserver.mysql.database.azure.com:3306/watchdog'

UPLOADS_DEFAULT_DEST = 'app/static/img/'
UPLOADS_DEFAULT_URL = '../static/img/'
UPLOADED_IMAGES_ALLOW = set(['png', 'jpg', 'jpeg'])

UPLOADED_IMAGES_DEST ='app/static/img/'
UPLOADED_IMAGES_URL = '../static/img/'

AZURE_STORAGE_ACCOUNT_NAME = "sokvideoanalyze8b05"
AZURE_STORAGE_ACCOUNT_KEY = "4SdxwWwId8+nPEhD6yY4f6om1BGnlbFAp7EnUcyrKcxKNOVTtDwJ6syOQz7ZMrvewWTyQWBBYd5Jc7WcBE1D9g=="
AZURE_STORAGE_CONTAINER_NAME = "static"  # make sure the container is created. Refer to the previous examples or to the Azure admin panel
AZURE_STORAGE_DOMAIN = 'https://sokvideoanalyze8b05.blob.core.windows.net'