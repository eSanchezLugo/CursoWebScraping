from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class Noticia(Item):
    id = Field()
    titular = Field()
    descripcion = Field()

class ElUniversoSpider(Spider):

    name = "MiSegundoSpider"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    start_urls = ['https://www.eluniverso.com/deportes']

    def parse(self, response):
        sel = Selector(response)
        noticias = sel.xpath('//div[@class="view-content"]/div[@class="posts"]')
        for i, elem in enumerate(noticias):
            item = ItemLoader(Noticia(), elem)

            item.add_xpath('titular', './/h2/a/text()')
            item.add_xpath('descripcion', './/p/text()')
            item.add_value('id', i)
            yield item.load_item()

    #def parse(self, response):
        #soup = BeautifulSoup(response.body)
        #contenedor_noticias = soup.find_all(class_='view-content')
        #id = 0
        #for contenedor in contenedor_noticias:
            #noticias = contenedor.find_all(class_='posts', recursive = False)
            #for noticia in noticias:
                #item = ItemLoader(Noticia(), response.body)
                #titular = noticia.find('h2').text.replace('\n', '').replace('\r', '')
                #descripcion = noticia.find('p')
                #if (descripcion):
                    #item.add_value('descripcion', descripcion.text.replace('\n', '').replace('\r', ''))
                #else:
                    #item.add_value('descripcion', 'N/A')
                    #item.add_value('titular', titular)
                    #item.add_value('id', id)
                    #id += 1
                    #yield item.load_item()



