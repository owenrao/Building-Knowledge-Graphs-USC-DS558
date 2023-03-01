import scrapy
from scrapy.crawler import CrawlerProcess
from MovieCrawler.spiders.top250_movies_spider import MovieSpider
from scrapy.settings import Settings
import MovieCrawler.settings as my_settings
from os import listdir

def init():
  for file in listdir(".") and ["Ruijie_Rao_hw01_movielist.jsonl","Ruijie_Rao_hw01_movie.jsonl","Ruijie_Rao_hw01_director.jsonl"]:
    open(file,'w').close()
    

if __name__ == "__main__":
  init()
  crawler_settings = Settings()
  crawler_settings.setmodule(my_settings)
  process = CrawlerProcess(settings=crawler_settings)
  process.crawl(MovieSpider)
  process.start()