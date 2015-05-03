This small repo allows you to email yourself and others with updates from the Economist website. 

#Setup

##Sensitive Credentials
You'll need to configure a few environment variables so that economist.py knows how to send emails:

* ECONOMIST_USERAGENT: For connecting to the website, i.e. "Economist Bot 0.1"
* ECONOMIST_USERNAME: Your email username, i.e. blogger_email
* ECONOMIST_PASSWORD : Your email password, i.e. Hunter2
* ECONOMIST_SERVER: Your mail server, i.e. mail.gmail.com. 
* ECONOMIST_PORT: Your mail server port, i.e. 567. 
* ECONOMIST_DIRECTORY: Where you'd like the article database/table to be saved. 

"export VARIABLE_NAME='value'" for each one of these to get started. 

##Recipients
You also need to specify recipients in the config.py file. These will all go on the "To" line of the email. 

#Running the program

I have my script configured to run once every morning via a cronjob. I.e. 15 9 * * * /usr/bin/python3.2 ~/economist.py

You can run the script as often as you'd like, but there are only so many new articles per day, particularly on the weekend. 

##Requirements

I'm using [Outbox](https://github.com/nathan-hoad/outbox), [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) and [Requests](http://docs.python-requests.org/en/latest/) with Python 3.4.


