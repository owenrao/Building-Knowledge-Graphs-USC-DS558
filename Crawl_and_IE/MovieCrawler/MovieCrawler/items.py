# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from turtle import title
from scrapy.item import Item, Field


class Movie(Item):
    def file_name(self):
        return 'Ruijie_Rao_hw01_movielist.jsonl'

    title = Field()
    year = Field()
    rank = Field()
    url = Field()


class MovieInfo(Item):
    def file_name(self):
        return 'Ruijie_Rao_hw01_movie.jsonl'

    title = Field()
    directors = Field()
    directors_url = Field()
    plot = Field()
    actors = Field()

class Director(Item):
    def file_name(self):
        return 'Ruijie_Rao_hw01_director.jsonl'

    name = Field()
    birthDate = Field()
    deathDate = Field()
    biography = Field()