import scrapy


class FilmSpiderSpider(scrapy.Spider):
    name = "film_spider"
    allowed_domains = ["ru.wikipedia.org",
                       "ru.m.wikipedia.org", 'www.imdb.com']

    def start_requests(self):
        URL = "https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B3%D0%BE%D0%B4%D0%B0%D0%BC"
        yield scrapy.Request(url=URL, callback=self.get_list_years)

    def get_list_years(self, response):
        for link in response.css('div.mw-category-group').css('div.CategoryTreeItem').css('a::attr(href)').getall():
            yield response.follow(link, callback=self.get_list_films)

    def get_list_films(self, response):
        for link in response.css('div.mw-category-group > ul > li > a::attr(href)').getall():
            yield response.follow(link, callback=self.parse_film)

        next_page = response.css(
            'div[id=mw-pages]').css('a::attr(href)').getall()
        if next_page:
            yield response.follow(next_page[-1], callback=self.get_list_films)

    def parse_film(self, response):
        # Parse name of film
        if response.css('th.infobox-above::text').get():
            name = response.css('th.infobox-above::text').get()
        else:
            name = response.css(
                'table.infobox.infobox-a323cc30500039ad').css('b::text').get()

        # Parse genre of film
        if response.css('span[data-wikidata-property-id="P136"]').css('a::text').getall():
            genre = response.css(
                'span[data-wikidata-property-id="P136"]').css('a::text').getall()
        else:
            genre = response.css(
                'span[data-wikidata-property-id="P136"]').css('span::text').getall()

        # Parse director of film
        if response.css('span[data-wikidata-property-id="P57"]').css('span::text').getall():
            director = response.css(
                'span[data-wikidata-property-id="P57"]').css('span::text').getall()
        else:
            director = response.css(
                'span[data-wikidata-property-id="P57"]').css('a::text').getall()

        # Parse country of film
        if response.css('span[data-wikidata-property-id="P495"]').css('span.wrap::text').getall():
            country = response.css(
                'span[data-wikidata-property-id="P495"]').css('span.wrap::text').getall()
        else:
            country = response.css(
                'span[data-wikidata-property-id="P495"]').css('a::text').getall()

        # Parse year of film
        if response.css('span.nowrap > a::text').get():
            year = response.css('span.nowrap > a::text').get()
        else:
            year = response.css('span.dtstart::text').get()

        # Combine data
        yield {
            'Название': name,
            'Жанр': genre,
            'Режиссер': director,
            'Страна': country,
            'Год': year
        }
