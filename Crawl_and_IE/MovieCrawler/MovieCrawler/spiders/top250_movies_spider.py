from pydoc import stripid
import scrapy
from bs4 import BeautifulSoup
from ..items import Movie, MovieInfo, Director
import re

class MovieSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        seed_url = "https://www.imdb.com/chart/top"
        yield scrapy.Request(url=seed_url, callback=self.parse_movie)

    def parse_movie(self, response):
        base_url = "https://www.imdb.com"
        content = response.text
        soup = BeautifulSoup(content, 'lxml')
        for movie in soup.find_all("tr"):
            title_col = movie.find("td","titleColumn")
            if title_col is not None:
                title = title_col.a.get_text()
                year = title_col.span.contents[0][1:-1]
                rank = title_col.get_text().split(".")[0].strip()
                url = base_url+title_col.a["href"]
                movie = Movie({
                'title': title,
                'year': year,
                'rank': rank,
                'url': url
                })
                yield movie
                yield scrapy.Request(url=movie['url'], callback=self.parse_movieinfo)

    def parse_movieinfo(self, response):
        base_url = "https://www.imdb.com"
        content = response.text
        soup = BeautifulSoup(content, 'lxml')
        title = soup.h1.get_text()
        plot = soup.find("div",{"data-testid":"plot"}).get_text()
        list_ele = soup.find("div",{"data-testid":"title-pc-wide-screen"}).ul.find_all("li", recursive=False)
        directors = []
        directors_url =[]
        for li in list_ele[0].ul.find_all("li"):
            directors.append(li.a.get_text())
            directors_url.append(base_url+li.a["href"])
        actors =[]
        for li in list_ele[2].ul.find_all("li"):
            actors.append(li.a.get_text())
        movie_info = MovieInfo({
            'title': title,
            'directors': directors,
            'directors_url': directors_url,
            'plot': plot,
            'actors': actors
        })
        yield movie_info
        for d_url in movie_info['directors_url']:
            yield scrapy.Request(url=d_url, callback=self.parse_director)
    
    def parse_director(self, response):
        base_url = "https://www.imdb.com"
        content = response.text
        soup = BeautifulSoup(content, 'lxml')
        name = soup.find("h1","header").span.get_text()
        try: birthDate = soup.find("div",{"id":"name-born-info"}).time.get_text(strip=True)
        except: birthDate = None
        try: deathDate = soup.find("div",{"id":"name-death-info"}).time.get_text(strip=True)
        except: deathDate = None
        try: bio_url = soup.find('div', {"id":"name-bio-text"}).find("span","see-more").a["href"]
        except: bio_url = None
        biography = None
        director = Director({
            'name': name,
            'birthDate': birthDate,
            'deathDate': deathDate,
            'biography': biography
        })
        if bio_url:
            director = response.follow(base_url+bio_url, self.parse_director_bio, cb_kwargs=dict(director=director))
        yield director

    def parse_director_bio(self, response, director):
        base_url = "https://www.imdb.com"
        content = response.text
        soup = BeautifulSoup(content, 'lxml')
        temp = [h4 for h4 in soup.find_all("h4") if "Mini Bio" in h4.get_text()]
        if len(temp)>0:
            mini_bio = temp[0]
            biography = mini_bio.find_next_sibling().get_text(strip=False)
            biography = re.sub("\s+"," ",biography).strip()
            director["biography"] = biography
        return director