from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector


class pregunta(Item):
    pregunta = Field()
    descripcion = Field()