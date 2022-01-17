import argparse
import csv #Para exportar csv's
import datetime #Para darle nombre de la fecha actual a mi archivo a exportar
import logging
from urllib.error import HTTPError
logging.basicConfig(level=logging.INFO)
import re #re=expresiones regulares

#Importo los errores ocupados en _fetch_article
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

import news_pages_objects as news
from common import config #Aca leo la configuracion a traves del archivo common

logger = logging.getLogger(__name__)
#declaro expresiones regulares:
is_well_formed_link = re.compile(r'^https?://.+/.+$') #Esta expresion regular se fija si el link tiene cierto formato para 'aceptarlo', por ejemplo: https://example.com/hello
is_root_path = re.compile(r'^/.+$') #Esta expresion 'acepta' los enlaces que hacen referencia a un path, por ej: /some-text

def _news_scraper(news_site_uid):
	host = config()['news_sites'][news_site_uid]['url']

	logging.info('Beginning scraper for {}'.format(host))
	homepage = news.HomePage(news_site_uid,host)

	articles = []
	for link in homepage.article_links:
		article = _fetch_article(news_site_uid, host, link)

		if article:
			logger.info('Article fetched!!')
			articles.append(article)
			#break

	_save_articles(news_site_uid, articles)	

def _save_articles(news_site_uid, articles):
	now = datetime.datetime.now().strftime('%Y_%m_%d') #Obtengo fecha y le doy formato de año,mes,dia
	out_file_name = '{news_site_uid}_{datetime}_articles.csv'.format( #Obtenemos el nombre de archivo a exportar
		news_site_uid=news_site_uid,
		datetime=now)
	csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))
	with open(out_file_name, mode='w+') as f:
		writer = csv.writer(f)
		writer.writerow(csv_headers)

		for article in articles:
			row = [str(getattr(article,prop)) for prop in csv_headers]
			writer.writerow(row)

def _fetch_article(news_site_uid, host, link):
	logger.info('Start fetching article at {}'.format(link))

	article = None
	try:
		article = news.ArticlePage(news_site_uid, _build_link(host, link))
	except (HTTPError, MaxRetryError) as e:
		logger.warning('Error while fetching the article', exc_info=False)

	if article and not article.body:
		logger.warning('Invalid article. There is no body')
		return None

	return article	

#Con esta funcion busco construir un link con formato correcto
def _build_link(host, link): 
	if is_well_formed_link.match(link): #Ocupo la expresion regular para que se fije si mi link cumple con el formato normal standart
		return link
	elif is_root_path.match(link): #Ocupo la expresion regular para ver si estoy en presencia de un link que hace referencia al path y lo completo para obtener el enlace completo
		return '{}{}'.format(host, link)
	else: #Si obtuve algo mas que no cumple estas formas, construyo el link improvisado de la siguiente manera:
		return '{host}/{uri}'.format(host=host, uri=link)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	news_site_choices = list(config()['news_sites'].keys())
	parser.add_argument('news_site', #Tengo que pasar como argumento una pagina declarada en el config.yaml
			help='The news site that you want to scrape',
			type=str,
			choices= news_site_choices)

	args = parser.parse_args() #Aca le pido al parser que haga un objeto con las opciones
	_news_scraper(args.news_site) #Llamado a la funcion _news_scraper pasandole la url que el usuario escogio
