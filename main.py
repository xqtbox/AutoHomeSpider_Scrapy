from scrapy import cmdline
cmdline.execute("scrapy crawl autohome_spider -o cars.csv".split())