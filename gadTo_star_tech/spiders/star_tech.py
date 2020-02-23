# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from gadTo_star_tech.items import GadtoStarTechItem


class StarTechSpider(scrapy.Spider):
    name = 'star_tech'
    allowed_domains = ['startech.com.bd']
    start_urls = ['https://www.startech.com.bd/desktops', 'https://www.startech.com.bd/laptop-notebook',
                  'https://www.startech.com.bd/component']

    rules = (
        Rule(LxmlLinkExtractor(allow_domains=allowed_domains)),
    )

    def parse(self, response):
        titles = response.xpath(".//*/div[@class='product-thumb']")
        for title in titles:
            item_links = title.xpath(".//*/h4[@class='product-name']/a/@href").extract()
            for item_link in item_links:
                yield response.follow(item_link, callback=self.parse_details)
        next_page = response.xpath(".//ul/ul/li/a[text()='NEXT']/@href").extract_first()
        print(next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_details(self, response):
        item = GadtoStarTechItem()
        page = response.xpath(".//*/div[@class='product-thumb']")
        item['website_name'] = 'Star Tech'
        item['parent_catagory_name'] = [
            response.xpath(".//ul[@class='breadcrumb']/li[2]/a/span/text()").extract_first()]
        item['child_catagory_name'] = [
            response.xpath(".//ul[@class='breadcrumb']/li[3]/a/span/text()").extract_first()]
        item['brand_name'] = [
            response.xpath(".//ul[@class='breadcrumb']/li[4]/a/span/text()").extract_first()]
        item['item_name'] = [
            response.xpath(".//h1[@class='product-name']/text()").extract_first()]
        item['price'] = [
            response.xpath(".//*[@id='product']/div[@class='price-wrap']/ins").extract_first()]
        item['image_urls'] = [response.xpath(".//div[@class='product-img-holder']/a/img/@src").extract_first()]
        table_rows = response.xpath('.//*[@id="specification"]/table[@class="data-table"]/tbody/tr/td').extract()
        # spec = {}
        # for table_row in table_rows:
        #     table_header = table_row.xpath('.//td[@class = "name"]').extract_first()
        #     table_header_value = table_row.xpath('.//td[@class = "value"]').extract_first()
        #     spec[table_header] = table_header_value
        item['specification'] = table_rows
        item['description'] = [response.xpath('.//*[@id="description"]/div').extract_first()]
        yield item
