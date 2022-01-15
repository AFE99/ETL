import argparse
import logging
logging.basicConfig(level=logging.INFO)

from common import config #Aca leo la configuracion a traves del archivo common

logger = logging.getLogger(__name__)

def _news_scraper(news_site_uid):
	host = config()['news_sites'][news_site_uid]['url']

	logging.info('Beginning scraper for {}'.format(host))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	news_site_choices = list(config()['news_sites'].keys())
	parser.add_argument('news_site', #Tengo que pasar como argumento una pagina declarada en el config.yaml
			help='The news site that you want to scrape',
			type=str,
			choices= news_site_choices)

	args = parser.parse_args() #Aca le pido al parser que haga un objeto con las opciones
	_news_scraper(args.news_site) #Llamado a la funcion _news_scraper pasandole la url que el usuario escogio
