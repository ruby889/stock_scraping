import scrapy
import re
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from stock_spider.items import *

class DefaultItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class stockSpider(scrapy.Spider):
    name = 'aastocksIndustrySpider'
    # allowed_domains = []
    start_urls = ['http://www.aastocks.com/en/stocks/market/industry/sector-industry-details.aspx']
    crawlAll = True

    def parse(self, response):
        for industry in response.xpath('//*[@id="IndustyMain"]/div[4]/div/div[1]//div[contains(@class, "IndustryBox")]'):
            industry_name = industry.xpath('./div[1]/text()').get()
            for category in industry.xpath('./div[2]//div[@class="IBMenuItem"]'):
                category_name = category.xpath('./text()').get()
                onclick = category.xpath('./@onclick').re_first(r'\d+')
                item=categoryItem()
                item['industry'] = industry_name
                item['category'] = category_name
                url = f'{self.start_urls[0]}?industrysymbol={onclick}&t=1&hk=0'
                yield scrapy.Request(url=url, callback=self.category_pasre, meta={'item': item}, dont_filter=True)

                if self.crawlAll:
                    for tab in range(1,7):
                        thisUrl = f'{self.start_urls[0]}?industrysymbol={onclick}&t={tab}&hk=0'
                        yield scrapy.Request(url=thisUrl, callback=self.getTabCallback, meta={'category':category_name}, dont_filter=True)

    def getTabCallback(self, response):
        callbackDict = {
            '1' : self.overview_parse,
            '2' : self.range_parse,
            '3' : self.performance_parse,
            '4' : self.financialRatio_parse,
            '5' : self.ratioBanking_parse,
            '6' : self.earnings_parse,
        }
        tab = re.search('t=(\d)', response.url).group(1)
        return callbackDict[tab](response)

    def category_pasre(self, response):        
        categoryItem = response.meta['item']
        categoryItem['changePercent'] = response.xpath('//*[@id="ETFLast"]/table/tr/td[2]/span/text()').re_first('\xa0(.+)')
        categoryItem['turnover'] = response.xpath('//*[@id="IndustyMain"]/div[4]/div/div[3]/table[1]/tbody/tr[1]/td[2]/div[2]/text()').re_first('\r(.+)\r')
        categoryItem['averagePE'] = response.xpath('//*[@id="IndustyMain"]/div[4]/div/div[3]/table[1]/tbody/tr[1]/td[3]/div[2]/text()').re_first('\r(.+)\r')
        categoryItem['averageTurnover'] = response.xpath('//*[@id="IndustyMain"]/div[4]/div/div[3]/table[1]/tbody/tr[2]/td[2]/div/table/tr/td[2]/font/text()').re_first('\r(.+)')
        categoryItem['prevChangePercent'] = response.xpath('//*[@id="IndustyMain"]/div[4]/div/div[3]/table[1]/tbody/tr[2]/td[1]/div/table/tr/td[2]/span/text()').get()
        yield categoryItem

    def overview_parse(self, response):
        category_name = response.meta['category']
        dataColumn = len(response.xpath('//*[@id="tblTS2"]/tbody/tr[1]//td'))
        if dataColumn <= 1:
            return
        for stock in response.xpath('//*[@id="tblTS2"]/tbody//tr'):
            loader = DefaultItemLoader(item=overviewTabItem(), selector=stock)
            loader.add_value('category', category_name)
            loader.add_xpath('stockNo', './td[1]/div[2]/div[1]/a/text()')
            loader.add_xpath('stockName', './td[1]/div[1]/div[1]/span/text()')
            loader.add_xpath('lastPrice', './td[2]/text()')
            loader.add_xpath('change', './td[3]/span/text()')
            loader.add_xpath('changePercent', './td[4]/span/text()')
            loader.add_xpath('volumn', './td[5]/text()')
            loader.add_xpath('turnover', './td[6]/text()')
            loader.add_xpath('PE', './td[7]/text()')
            loader.add_xpath('PB', './td[8]/text()')
            loader.add_xpath('earningYield', './td[9]/text()')
            loader.add_xpath('marketCap', './td[10]/text()')
            yield loader.load_item()
            
    def range_parse(self,response):
        category_name = response.meta['category']
        dataColumn = len(response.xpath('//*[@id="tblTS2"]/tbody/tr[1]//td'))
        if dataColumn <= 1:
            return
        for stock in response.xpath('//*[@id="tblTS2"]/tbody//tr'):
            loader = DefaultItemLoader(item=rangeTabItem(), selector=stock)
            loader.add_value('category', category_name)
            loader.add_xpath('stockNo', './td[1]/a/text()')
            loader.add_xpath('stockName', './td[2]/span/text()')
            loader.add_xpath('lastPrice', './td[3]/div/text()')
            loader.add_xpath('month1', './td[4]/text()')
            loader.add_xpath('month2', './td[5]/text()')
            loader.add_xpath('month3', './td[6]/text()')
            loader.add_xpath('week52', './td[7]/text()')
            yield loader.load_item()

    def performance_parse(self,response):
        category_name = response.meta['category']
        dataColumn = len(response.xpath('//*[@id="tblTS2"]/tbody/tr[1]//td'))
        if dataColumn <= 1:
            return
        for stock in response.xpath('//*[@id="tblTS2"]/tbody//tr'):
            loader = DefaultItemLoader(item=performanceTabItem(), selector=stock)
            loader.add_value('category', category_name)
            loader.add_xpath('stockNo', './td[1]/a/text()')
            loader.add_xpath('stockName', './td[2]/span/text()')
            loader.add_xpath('lastPrice', './td[3]/text()')
            loader.add_xpath('year3', './td[5]/span/text()')
            loader.add_xpath('year1', './td[6]/span/text()')
            loader.add_xpath('month6', './td[7]/span/text()')
            loader.add_xpath('month3', './td[8]/span/text()')
            loader.add_xpath('month1', './td[9]/span/text()')
            loader.add_xpath('week1', './td[10]/span/text()')
            loader.add_xpath('YTD', './td[11]/span/text()')
            yield loader.load_item()

    def financialRatio_parse(self,response):
        category_name = response.meta['category']
        dataColumn = len(response.xpath('//*[@id="tblTS2"]/tbody/tr[1]//td'))
        if dataColumn <= 1:
            return
        for stock in response.xpath('//*[@id="tblTS2"]/tbody//tr'):
            loader = DefaultItemLoader(item=financialRatioTabItem(), selector=stock)
            loader.add_value('category', category_name)
            loader.add_xpath('stockNo', './td[1]/div[2]/div/a/text()')
            loader.add_xpath('stockName', './td[1]/div[1]/div/span/text()')
            loader.add_xpath('lastPrice', './td[2]/text()')
            loader.add_xpath('currentRatio', './td[3]/text()')
            loader.add_xpath('quickRatio', './td[4]/text()')
            loader.add_xpath('ROA', './td[5]/text()')
            loader.add_xpath('ROE', './td[6]/text()')
            loader.add_xpath('grossProfitMargin', './td[7]/text()')
            loader.add_xpath('netProgitMargin', './td[8]/text()')
            loader.add_xpath('payout', './td[9]/text()')
            loader.add_xpath('debtEquityRatio', './td[10]/text()')
            loader.add_xpath('yrEnd', './td[11]/text()')
            yield loader.load_item()

    def ratioBanking_parse(self,response):
        return
        
    def earnings_parse(self,response):
        category_name = response.meta['category']
        dataColumn = len(response.xpath('//*[@id="tblTS2"]/tbody/tr[1]//td'))
        if dataColumn <= 1:
            return
        for stock in response.xpath('//*[@id="tblTS2"]/tbody//tr'):
            loader = DefaultItemLoader(item=earningsTabItem(), selector=stock)
            loader.add_value('category', category_name)
            loader.add_xpath('stockNo', './td[1]/div[2]/div/a/text()')
            loader.add_xpath('stockName', './td[1]/div[1]/div/span/text()')
            loader.add_xpath('lastPrice', './td[2]/text()')
            loader.add_xpath('revenue', './td[3]/text()')
            loader.add_xpath('revenueGrowthYOY', './td[4]/text()')
            loader.add_xpath('operatingProfit', './td[5]/text()')
            loader.add_xpath('operatingProfitMargin', './td[6]/text()')
            loader.add_xpath('netProfit', './td[7]/text()')
            loader.add_xpath('netProfitMargin', './td[8]/text()')
            loader.add_xpath('EPS', './td[9]/text()')
            loader.add_xpath('EPSGrowthYOYPercent', './td[10]/text()')
            loader.add_xpath('yrEnd', './td[11]/text()')
            yield loader.load_item()
