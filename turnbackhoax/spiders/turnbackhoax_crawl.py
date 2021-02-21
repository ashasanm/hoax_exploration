import scrapy
from time import sleep
from ..splitter import Splitter

class TurnbackhoaxCrawler(scrapy.Spider):
    name = 'turnbackhoax'
    allowed_domains = ['turnbackhoax.id']


    def start_requests(self):
        """ Starts request based on page """
        for i in range(1, 327):
            yield scrapy.Request('https://turnbackhoax.id/page/{}/'.format(i), callback=self.get_article)

    def get_article(self, response):
        """ Extracts article's urls """
        article_urls = response.xpath('//*[@id="main-content"]/article/div/header/h3/a/@href').extract()
        for article in article_urls:
            yield scrapy.Request(article, callback=self.parse)


    def parse(self, response):
        """ Parse article """
        title = response.xpath('//article/header/h1/text()').extract_first()
        post_date = response.xpath('//article/header/p/span[1]/a/text()').extract_first()
        author = response.xpath('//article/header/p/span[2]/a/text()').extract_first()
        # raw content, need to be processed
        raw_content = response.xpath('//article/div[1]/p//text()').extract() # List
        references_sub = response.xpath('//article/div/figure/div/text()').extract()
        raw_content = ' '.join(raw_content)
        references_sub = ' '.join(raw_content)
        splitter = Splitter(raw_content)
        content = splitter.start_split()
        scraped_hoax = {
            'title': title,
            'post_date': post_date,
            'author': author,
            'category': content['category'],
            'source_hoax': content['source_hoax'],
            'narration': content['narration'],
            'explanation_detail': content['explanation_detail'],
            'source_validation': content['source_validation'],
            'source_data': response.url
        }
        print('\n', scraped_hoax, '\n')
        yield scraped_hoax