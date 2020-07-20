# -*- coding: utf-8 -*-
import scrapy


class DebtGdpSpider(scrapy.Spider):
    name = 'debt_GDP'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = ['https://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        countries = response.xpath("//table[@class='datatableStyles__StyledTable-ysgkm4-1 dXImya table table-striped']/tbody/tr")
        for country in countries:
            name = country.xpath(".//td/a/text()").get()
            link = country.xpath(".//td/a/@href").get()  

            yield response.follow(url=link, callback=self.country_parse, meta={'country_name':name})

    def country_parse(self,response):
        name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class='datatableStyles__StyledTable-ysgkm4-1 dXImya table table-striped'])[2]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()          
            population = row.xpath(".//td[2]/text()").get()          
            growth_rate = row.xpath(".//td[3]/span/text()").get()          
            population_rank = row.xpath(".//td[5]/text()").get()          
            density_rank = row.xpath(".//td[6]/text()").get()  


            yield {
                'name':name,
                'year':year,
                'population':population,
                'growth_rate':growth_rate,
                'population_rank':population_rank,
                'density_rank':density_rank
            }        
                     
