from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup


class Articulo(Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()


class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadoLibre'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20
    }

    allowed_domains = ['articulo.mercadolibre.com.ec', 'listado.mercadolibre.com.ec']

    start_urls = ['https://listado.mercadolibre.com.ec/animales-mascotas/perros/']

    download_delay = 1


    rules = (
        Rule(  # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            LinkExtractor(
                allow=r'/_Desde_\d+'

            ), follow=True),
        Rule(  # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
            LinkExtractor(
                allow=r'/MEC-'
            ), follow=True, callback='parse_items'),

    )

    def parse_items(self, response):
        item = ItemLoader(Articulo(), response)


        item.add_xpath('titulo', '//h1/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('descripcion', '//div[@class="item-description__text"]/p/text()',
                       MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))

        soup = BeautifulSoup(response.body)
        precio = soup.find(class_="price-tag")
        precio_completo = precio.text.replace('\n', ' ').replace('\r', ' ').replace(' ', '')
        item.add_value('precio', precio_completo)

        yield item.load_item()

