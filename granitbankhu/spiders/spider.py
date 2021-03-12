import scrapy

from scrapy.loader import ItemLoader

from ..items import GranitbankhuItem
from itemloaders.processors import TakeFirst


class GranitbankhuSpider(scrapy.Spider):
	name = 'granitbankhu'
	start_urls = ['https://granitbank.hu/hirek']

	def parse(self, response):
		post_links = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "content", " " ))]//td')
		for post in post_links:
			date = post.xpath('./p[(((count(preceding-sibling::*) + 1) = 3) and parent::*)]/text()').get()
			description = post.xpath('./p[3]/text()').get()
			title = post.xpath('./p[1]/text()').get()


			item = ItemLoader(item=GranitbankhuItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()
