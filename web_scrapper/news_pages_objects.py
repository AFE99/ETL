import bs4
import requests
from common import config

#Declaro una clase PADRE con metodos reutilizables en las diferentes paginas a visitar
class NewsPage:
    #Funcion que inicializa la clase
    def __init__(self, site_uid, url): 
        self._config = config()['sites'][site_uid]
        self._queries = self._config['queries']
        self._html= None
        self._url = url

        self._visit(self._url) #Llamo a la funcion _visit para que visite y parsee la url

    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):
        # Esto nos va a devolver un objeto response que almacena el codigo fuente de la pagina, con el cual podemos interactuar luego.
        response = requests.get(url)
        #Devuelve HTTPError si algo sale mal
        response.raise_for_status() 
        #response.text devuelve el codigo html completo
        self._html = bs4.BeautifulSoup(response.text, 'html.parser') 

class HomePage(NewsPage): #representa la pagina principal de nuestra web, clase HIJA de NewsPage
    def __init__(self, site_uid, url): #Funcion que inicializa la clase
        super().__init__(site_uid, url) #Heredamos de NewsPage la inicializacion de clase

    @property
    def article_links(self):
        link_list = [] #Inicializo una list donde voy a guardar los enlaces que halle a articulos
        for link in self._select(self._queries['homepage_article_links']): #Hago un select de las cosas que encuentre en el codigo html que coincida con lo que especifiqué en homepage_article_links (config.yaml)
            if link and link.has_attr('href'): #Si lo que encontré tiene un href lo tomo y agrego a la lista de links
                link_list.append(link)
            #Ocupo 'set' para que no me devuelva links repetidos en la lista link_list
        return set(link['href'] for link in link_list) 

class ArticlePage(NewsPage): #representa la interaccion con cada articulo, clase HIJA de NewsPage

    def __init__(self, site_uid, url): #Funcion que inicializa la clase
        super().__init__(site_uid, url) #Heredamos de NewsPage la inicializacion de clase

    @property
    def url(self):
        return self._url

    @property
    def score(self):
        result = self._select(self._queries['article_score']) #Hago un select de las cosas que encuentre en el codigo html que coincida con lo que especifiqué en article_body (config.yaml)
        return result[0].text if len(result) else '' #Cuando ingreso al link de un articulo, el select me devuelve una lista, suponiendo que el primer elemento es el body, lo tomo y lo retorno, si esta vacio, devuelvo nada ''

    @property
    def title(self):
        result = self._select(self._queries['article_title']) #Hago un select de las cosas que encuentre en el codigo html que coincida con lo que especifiqué en article_title (config.yaml)
        return result[0].text if len(result) else '' #Como este metodo se ejecuta por cada link, y el select nos devuelve una lista, tomamos unicamente la primer posicion de la misma, que deberá contener el titulo del articulo, si no existe devuelvo vacio ''.