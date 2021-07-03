#!/usr/bin/env python3
import os
from datetime import datetime
import json
import pandas as pd
from run_spider import run_spider

DIRECTORY = 'data/aastocksIndustry/'
ALL_UPDATE_TYPE = "all"
CATEGORY_UPDATE_TYPE = "category" 

CATEGORY = 'category'
OVERVIEW_TAB = 'overviewTab'
RANGE_TAB = 'rangeTab'
PERFORMANCE_TAB = 'performanceTab'
FINANCIAL_RATIO_TAB = 'financialRatioTab'
RATIO_BANKING_TAB = 'ratioBankingTab'
EARNINGS_TAB = 'earningsTab'
class webScraper:
    def __init__(self) -> None:
        self.config = f'{DIRECTORY}config.json'
        self.data = {}
        self.initial()

    def initial(self):
        configFile = self.config
        if not os.path.exists(configFile):
            self._writeConfig()     #Initial a config file first, since spider need information from config.
            self.updateData(ALL_UPDATE_TYPE)
                
        dataFiles = [CATEGORY,OVERVIEW_TAB,RANGE_TAB,PERFORMANCE_TAB,FINANCIAL_RATIO_TAB,RATIO_BANKING_TAB,EARNINGS_TAB]
        for name in dataFiles:
            path = DIRECTORY + name + '.csv'
            try:
                self.data[name] = pd.read_csv(path)
            except pd.errors.EmptyDataError:
                pass
            
    def getAllIndustries(self):
        df = self.data[CATEGORY]
        return df['industry'].unique()
    
    def getAllCategories(self, industry):
        df = self.data[CATEGORY]
        return list(df.loc[df['industry'] == industry, 'category'])

    def getCategoryDetails(self, category):
        df = self.data[CATEGORY]
        return df.loc[df['category'] == category].iloc[1,2]

    def getAllCriterion(self, tab):
        df = self.data[tab]
        return list(df.columns)

    #Example: getStocksFromCategory('Gas Supply', 3, ['changePercent'], True)
    def getStocksFromCategory(self, category, quantity, columnName, ascending):
        for name in self.data.keys():
            if 'Tab' in name:
                tabColumns = self.getAllCriterion(name)
                if all(x in tabColumns for x in columnName):
                    df = self.data[name]
                    stocks = df.loc[df['category'] == category]
                    stortedStocks = stocks.sort_values(by=columnName, ascending=ascending)
                    return stortedStocks.head(quantity)
    
    def getStockDetails(self, stockNo, tab):
        df = self.data[tab]
        return df.loc[df['stockNo'] == stockNo]

    def getLastUpdateDate(self, updateType):
        filename = self.config
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                config = json.load(f)
            return config['lastUpdate'][updateType]
        return None

    #Update for catergory only or for all details.
    def updateData(self, updateType=ALL_UPDATE_TYPE):
        today = datetime.today().strftime('%Y-%m-%d')
        lastUpdate = self.getLastUpdateDate(updateType)
        crawlAll = True if updateType == ALL_UPDATE_TYPE else False
        if not today == lastUpdate:
            print("Start Crawling...")
            run_spider(crawlAll)
            print("Finished Crawling.")
            self._writeConfig()
            self.initial()
            return True
        else:
            print("Data is update to date.")
            return False

    def _writeConfig(self):
        today = datetime.today().strftime('%Y-%m-%d')
        data = {}
        data['itemList'] = {
            'categoryItem':             ['industry', 'category', 'changePercent', 'prevChangePercent','turnover','averageTurnover','averagePE'],
            'overviewTabItem':          ['category','stockNo','stockName','lastPrice','change','changePercent','volumn',
                                        'turnover','PE','PB','earningYield','marketCap'],
            'rangeTabItem':             ['category','stockNo','stockName','lastPrice', 'month1','month2','month3','week52'],
            'performanceTabItem':       ['category','stockNo','stockName','lastPrice','year3','year1','month6','month3','month1','week1','YTD'],
            'financialRatioTabItem':    ['category','stockNo','stockName','lastPrice','currentRatio','quickRatio','ROA','ROE',
                                        'grossProfitMargin','netProgitMargin','payout','debtEquityRatio','yrEnd'],
            'ratioBankingTabItem':      ['category','stockNo','stockName','lastPrice','currentRatio','trading','profitability','yrEnd'],
            'earningsTabItem':          ['category','stockNo','stockName','lastPrice','revenue','revenueGrowthYOY','operatingProfit',
                                        'operatingProfitMargin','netProfit','netProfitMargin','EPS','EPSGrowthYOYPercent','yrEnd'],
        }
        data['lastUpdate'] = {
            CATEGORY_UPDATE_TYPE: today,
            ALL_UPDATE_TYPE:      today,
        }
        filename = self.config
        with open(filename, 'w') as f:
            json.dump(data, f)

def main():
    webScraper()

if __name__ == '__main__':
    main() 