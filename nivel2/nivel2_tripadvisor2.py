from scrapy.item import Item
from scrapy.item import Field
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Opinion(Item):
    titulo = Field()
    calificacion = Field()
    contenido = Field()
    autor = Field()
    hotel = Field()


class TripAdvisor(CrawlSpider):
    name = 'hotelestripadvisor'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 100
    }

    allowed_domains = ['tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    download_delay = 1

    rules = (
        # Paginación de hoteles. (h)
        Rule(
            LinkExtractor(
                allow=r'oa\d+-'
            ), follow=True

        ),
        # Detalle de hoteles. (h)
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-',
                restrict_xpaths=['//div[@id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0"]']
            ), follow=True

        ),
        # Paginación de opciones dentro de hoteles. (v)
        Rule(
            LinkExtractor(
                allow=r'-or\d+-'
            ),follow=True

        ),
        #  Detalla ede perfil de usuario. (v)
        Rule(
            LinkExtractor(
                allow=r'/Profile/',
                restrict_xpaths=['//div[@data-test-target="reviews-tab"]']
            ), follow=True, callback='parse_opinion'

        ),
    )

    def parse_opinion(self, response):
        sel = Selector(response)
        opiniones = sel.xpath('//div[@id="content"]/div/div')
        autor = sel.xpath('//h1/span/text()').get()
        for opinion in opiniones:
            item = ItemLoader(Opinion(), opinion)
            item.add_value('autor', autor)
            item.add_xpath('titulo', './/div[@class="_3IEJ3tAK _2K4zZcBv"]/text()')
            item.add_xpath('hotel',
                           './/div[contains(@class, "ui_card section")]//div[@title]/text()')
            item.add_xpath('contenido', './/q/text()', MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
            item.add_xpath('calificacion',
                           './/div[contains(@class, "ui_card section")]//a/div/span[contains(@class, "ui_bubble_rating")]/@class',
                           MapCompose(lambda i: i.split('_')[-1]))
            yield item.load_item()



