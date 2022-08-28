import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//text-fill/a/@href'
#XPATH_LINK_TO_ARTICLE = '//*[@id="vue-container"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/text-fill/a/@href'
#XPATH_TITLE = '//div[@class="mb-auto"]/h2/span/text()'
XPATH_TITLE = '/html/head/title/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p//text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)

        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]

                #reemplazar las comillas doble por nada
                #title.replace('\"', '')

                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
                #content = "".join(body)
            except IndexError:
                return

            '''
            with: manejador contextual de python, evita que se corrompa el archivo que se esta manipulando
            '''
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

            #return print(title, '\n', summary, '\n', content)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        #trae todo el documento http
        response = requests.get(HOME_URL) 

        #analiza que la respuesta es positiva cod 200
        if response.status_code == 200:

            #obtiene todo el codigo html y con decode el código de carácteres
            home = response.content.decode('utf-8') 

            #convierte el codigo html y lo transforma en un documento que se puede hacer xpath
            parsed = html.fromstring(home) 
            #return print(home)

            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #return print(links_to_notices)

            #crea un string de la fecha actual
            today = datetime.date.today().strftime('%d-%m-%Y') 

            #crea una carpeta con la fecha actual, siempre cuando no esté creada con anterioridad
            if not os.path.isdir(today):
                os.mkdir(today)

            #recorre cada link con la funcion parse_notice
            for link in links_to_notices:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}') #captura el código de error de la requests
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()