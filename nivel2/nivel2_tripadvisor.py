from scrapy.item import Item
from scrapy.item import Field
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()


class TripAdvisor(CrawlSpider):
    name = "Hoteles"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']
    download_delay = 2


    rules = (
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-'
            ), follow=True, callback="parse_hotel"
        ),
    )

    def quitarSimboloMoneda(self, texto):
        nuevoTexto = texto.replace("$", "")
        nuevoTexto = nuevoTexto.replace('\n', '').replace('\r', '').replace('\t', '')
        return nuevoTexto

    def parse_hotel(self, response):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)
        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('precio', '//div[@class = "ui_column is-4 _1j6xaJwD"]//div/text()', MapCompose(self.quitarSimboloMoneda))
        item.add_xpath('descripcion', '//div[@class = "_2f_ruteS _1bona3Pu _2-hMril5 _2uD5bLZZ"]//div[1]//p/text()')
        item.add_xpath('amenities', '//div[contains(@data-test-target,"amenity_text")]/text()')

        yield item.load_item()


