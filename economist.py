import requests
from bs4 import *
import sqlite3
from outbox import Outbox, Email
from pyh import *
from datetime import datetime
import time
import config

def send_email():
	outbox = Outbox(username=config.username, password=config.password,server=config.server, port=config.port)

	conn = sqlite3.connect(config.database_directory+'article_db')
	cursor = conn.cursor()
	to_send = cursor.execute('SELECT headline,rubric,body,rowid FROM article_tbl WHERE delivered = "False"').fetchall()
	
	if len(to_send) > 0:

		html_email = PyH('Economist Articles')
		
		html_email << a(img(src="http://www.economist.com/rights/images/logo+economist.gif"),name="top")
		
		contents = html_email << div()

		for i, thing in enumerate(to_send):
			content_object = contents << div()
			content_object << a(thing[0],href="#%i" % i,style="font-family:Verdana;color:blue")
			content_object << br()
			content_object << span("&nbsp;&nbsp;&nbsp;&nbsp;%s" % thing[1],style="font-family:Verdana;")
			content_object << p('')

			html_email << h2(thing[0],style="font-family:Verdana;") << a(name="%i" % i)
			html_email << h3(thing[1],style="font-family:Verdana;")
			html_email << p(thing[2],style="font-family:Verdana;")
			html_email << p('') << a("Top",href="#top",style="font-family:Verdana;")
		html_email << p('')
		html_email << p('Made with <3 by oneschirm',style="font-family:Verdana;")

		outbox.send(Email(subject='Economist Articles - %s' % datetime.strftime(datetime.today(),'%m/%d/%Y, %H:%M %Z'), html_body=html_email.render(),recipients=config.recipients))
		
		for thing in to_send:
			cursor.execute('UPDATE article_tbl SET delivered="True" WHERE rowid = ?', (thing[3],))

		conn.commit()
		conn.close()

def get_articles():
	headers = {'User-Agent':config.user_agent}
	response = requests.get('http://www.economist.com/',headers=headers).text
	soup = BeautifulSoup(response)

	articles = soup.select('article')

	links = []

	article_data = []

	for article in articles:
		anchor = article.select('a')[0]['href']
		if anchor not in links:
			links.append(anchor)

	for link in links:
		time.sleep(5)
		try:
			#make sure it's a real article and not a blog post
			if 'blogs/' not in link:
				article_soup = BeautifulSoup(requests.get('%s%s' % ('http://www.economist.com/',link),headers=headers).text)
				#this checks to see whether the article is just a video
				if len(article_soup.select("[type='application/x-shockwave-flash']")) == 0:
					headline = article_soup.select('.headline')[0].getText().strip().upper()
					rubric = article_soup.select('.rubric')[0].getText().strip()
					paragraphs = article_soup.select('.main-content p')
					parsed_paragraphs = []
					for paragraph in paragraphs:
						if len(paragraph.getText().strip()) > 0:
							parsed_paragraphs.append('<p>%s</p>' %paragraph.getText().strip())
					article_data.append({'headline':headline,'rubric':rubric,'body':''.join(parsed_paragraphs),'link':link})
		except:
			pass
	
	return article_data

def write_articles(article_data):
	conn = sqlite3.connect(config.database_directory+'article_db')
	cursor = conn.cursor()

	if len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()) == 0:
		cursor.execute("CREATE TABLE article_tbl (headline TEXT, rubric TEXT, body TEXT, link TEXT, delivered TEXT)")

	existing_links = cursor.execute('SELECT link FROM article_tbl').fetchall()
	parsed_links = [x[0] for x in existing_links]
	for article in article_data:
		if article['link'] not in parsed_links:
			print('adding %s' % article['link'])
			cursor.execute('INSERT INTO article_tbl VALUES (?,?,?,?,?)', (article['headline'],article['rubric'],article['body'],article['link'],'False'))
	conn.commit()
	conn.close()

if __name__ == '__main__':
	write_articles(get_articles())
	send_email()
