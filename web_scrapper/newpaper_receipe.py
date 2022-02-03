#Importo las librerias
import argparse #Para parsear
import logging #Para informar al user lo que está pasando
logging.basicConfig(level=logging.INFO) #Configuro el logging con la configuracion basica y el nivel logging.INFO
from urllib.parse import urlparse

import pandas as pd

logger = logging.getLogger(__name__) #Obtengo una referencia al logger, pasandole como parametro el nombre interno que tiene python de nuestro archivo (variable global 'name')

def main(filename): #Nuestra funcion main recibe como parametro un string que indica el nombre del archivo
    logger.info('Starting cleaning process') #Indicamos por consola que se esta iniciando el proceso de limpieza
    df = _read_data(filename) #Utilizo la funcion que declaré mas abajo para leer archivos con pandas y lo almaceno en la variable 'df'
    page_id = _extract_page_id(filename) #Extraigo el id de cada pagina visitada
    df = _add_page_id_column(df, page_id) #Incluyo el dato id en una columna
    df = _extract_host(df) #Extraigo el host del DataFrame
    return df

def _read_data(filename):
    #Al principio de cada funcion decimos que estamos haciendo por consola
    logger.info('Reading file {}'.format(filename))
    #Ocupo pandas para leer el archivo csv. Recibiendo la ruta con el nombre del archivo (contenido en filename) como parametro
    return pd.read_csv(filename) #Devuelvo el archivo

def _extract_page_id(filename): #Funcion que extrae el id de una pagina, recibiendo como parametro la ruta+nombre del archivo con el que se está trabajando
    logger.info('Extracting page id') #Informo por consola lo que voy a hacer
    page_id = filename.split('_')[0] #Aprovechando la estructura, se que en la primer posicion (0), separados por '_' se encuentra el id, lo tomo
    logger.info('Page id detected: {}'.format(page_id))
    return page_id

def _add_page_id_column(df, page_id): #Funcion que agrega la columna con el dato del id de una pagina a la tabla df
    logger.info('Filling page_id column with {}'.format(page_id)) #Informo por consola lo que estoy haciendo
    df['page_id'] = page_id #En la columna 'page_id' agregame el contenido de la variable 'page_id', si no existe crea la columna
    return df
 
def _extract_host(df):
    logger.info('Extracting host from urls')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc) #parseo la url con una funcion lambda
    return df

if __name__ == '__main__': #Punto de entrada
    #Primero le preguntamos al user cual es el archivo dataset con el que queremos trabajar
    parser = argparse.ArgumentParser()
    #Añadimos un argumento llamado 'filename'
    parser.add_argument('filename',
                        help='The path to the dirty data', #le damos un texto de ayuda "Pasame el path/direccion a los datos sucios (dataset a utilizar)
                        type=str) #Lo que nos va a devolver el usuario es un string
    #Parseamos los argumentos ocupando el parser
    args = parser.parse_args() #args almacena todos los argumentos que nos envia el user
    #Una vez que ya tenemos los argumentos, le pasamos como parametros a la funcion main
    df = main(args.filename)

    print(df) #Muestro la tabla resultante