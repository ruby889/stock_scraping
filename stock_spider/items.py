# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field

class categoryItem(Item):
    industry = Field()
    category = Field()
    changePercent = Field()
    prevChangePercent = Field()
    turnover = Field()
    averageTurnover = Field()
    averagePE = Field()

class overviewTabItem(Item):
    category = Field()
    stockNo = Field()
    stockName = Field()
    lastPrice = Field()
    change = Field()
    changePercent = Field()
    volumn = Field()
    turnover = Field()
    PE = Field()
    PB = Field()
    earningYield = Field()
    marketCap = Field()

class rangeTabItem(Item):
    category = Field()
    stockNo = Field()
    stockName = Field()
    lastPrice = Field()
    month1 = Field()
    month2 = Field()
    month3 = Field()
    week52 = Field()

class performanceTabItem(Item):
    category = Field()
    stockNo = Field()
    stockName = Field()
    lastPrice = Field()
    year3 = Field()
    year1 = Field()
    month6 = Field()
    month3 = Field()
    month1 = Field()
    week1 = Field()
    YTD = Field()
    
class financialRatioTabItem(Item):
    category = Field()
    stockNo = Field()
    stockName = Field()
    lastPrice = Field()
    currentRatio = Field()
    quickRatio = Field()
    ROA = Field()
    ROE = Field()
    grossProfitMargin = Field()
    netProgitMargin = Field()
    payout = Field()
    debtEquityRatio = Field()    
    yrEnd = Field()

class ratioBankingTabItem(Item):
    category = Field()
    stockNo = Field()
    stockName = Field()
    lastPrice = Field()
    currentRatio = Field()
    trading = Field()
    profitability = Field()
    yrEnd = Field()

class earningsTabItem(Item):
    category = Field()
    stockNo = Field()
    stockName = Field()
    lastPrice = Field()
    revenue = Field()
    revenueGrowthYOY = Field()
    operatingProfit = Field()
    operatingProfitMargin = Field()
    netProfit = Field()
    netProfitMargin = Field()
    EPS = Field()
    EPSGrowthYOYPercent = Field()
    yrEnd = Field()







