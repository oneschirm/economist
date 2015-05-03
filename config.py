import os

user_agent = os.environ.get('ECONOMIST_USERAGENT','')
username = os.environ.get('ECONOMIST_USERNAME','')
password = os.environ.get('ECONOMIST_PASSWORD','')
server =os.environ.get('ECONOMIST_SERVER','')
port = int(os.environ.get('ECONOMIST_PORT',''))
database_directory=os.environ.get('ECONOMIST_DIRECTORY','')

recipients = []
