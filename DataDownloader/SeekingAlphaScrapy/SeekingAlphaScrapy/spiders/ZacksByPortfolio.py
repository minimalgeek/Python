# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector

class ZacksbyportfolioSpider(scrapy.Spider):
    name = "ZacksByPortfolio"
    allowed_domains = ["zacks.com"]
    start_urls = [
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1110794&enc_cust_id==AFVxIlVGpVYWZlWWN2R1IlVwA3VV5GaWZlRkNzUUZUV&tab_name=growth&port_name=SPX_AB&call_counter=2&_=1452764694756',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1110799&enc_cust_id==AFVxIlVGpVYWZlWWN2R1IlVwA3VV5GaWZlRkNzUUZUV&tab_name=growth&port_name=SPX_CD&call_counter=2&_=1452764694758',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1110801&enc_cust_id==AFVxIlVGpVYWZlWWN2R1IlVwA3VV5GaWZlRkNzUUZUV&tab_name=growth&port_name=SPX_EH&call_counter=2&_=1452764694760',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1110802&enc_cust_id==AFVxIlVGpVYWZlWWN2R1IlVwA3VV5GaWZlRkNzUUZUV&tab_name=growth&port_name=SPX_IM&call_counter=2&_=1452764694762',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1110803&enc_cust_id==AFVxIlVGpVYWZlWWN2R1IlVwA3VV5GaWZlRkNzUUZUV&tab_name=growth&port_name=SPX_NR&call_counter=2&_=1452764694764',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1110808&enc_cust_id==AFVxIlVGpVYWZlWWN2R1IlVwA3VV5GaWZlRkNzUUZUV&tab_name=growth&port_name=SPX_SZ&call_counter=2&_=1452764694766',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1109917&enc_cust_id==AFVxIlVGpVYWZlWWN2R1IlVwA3VV5GaWZlRkNzUUZUV&tab_name=growth&port_name=LargeCap&call_counter=2&_=1452764694768',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1079535&enc_cust_id==AFVxIlVGpVYWZlWWN2R1IlVwA3VV5GaWZlRkNzUUZUV&tab_name=growth&port_name=Nas100&call_counter=2&_=1452764694770',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1306512&enc_cust_id==AFVxI1VsRWYWxmWWN2R1YlVwkVeZRlRSVGbWlVUq5UV&tab_name=growth&port_name=MID_WZ&call_counter=2&_=1453802356526',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1306509&enc_cust_id==AFVxI1VsRWYWxmWWN2R1YlVwkVeZRlRSVGbWlVUq5UV&tab_name=growth&port_name=MID_RV&call_counter=2&_=1453802356528',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1306508&enc_cust_id==AFVxI1VsRWYWxmWWN2R1YlVwkVeZRlRSVGbWlVUq5UV&tab_name=growth&port_name=MID_KP&call_counter=2&_=1453802356532',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1306506&enc_cust_id==AFVxI1VsRWYWxmWWN2R1YlVwkVeZRlRSVGbWlVUq5UV&tab_name=growth&port_name=MID_DJ&call_counter=2&_=1453802356536',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1306501&enc_cust_id==AFVxI1VsRWYWxmWWN2R1YlVwkVeZRlRSVGbWlVUq5UV&tab_name=growth&port_name=MID_AC&call_counter=2&_=1453802356538',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1801010&enc_cust_id==AFVxI1VsRWYWdlTWN2RxQVUwA3VVpmU2dlRsZTUXVTV&tab_name=growth&port_name=SML_AB&call_counter=2&_=1461056696458',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1801016&enc_cust_id==AFVxI1VsRWYWdlTWN2RxQVUwA3VVpmU2dlRsZTUXVTV&tab_name=growth&port_name=SML_CD&call_counter=2&_=1461056696460',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1801021&enc_cust_id==AFVxI1VsRWYWdlTWN2RxQVUwA3VVpmU2dlRsZTUXVTV&tab_name=growth&port_name=SML_EG&call_counter=2&_=1461056696462',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1801025&enc_cust_id==AFVxI1VsRWYWdlTWN2RxQVUwA3VVpmU2dlRsZTUXVTV&tab_name=growth&port_name=SML_HL&call_counter=2&_=1461056696464',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1801030&enc_cust_id==AFVxI1VsRWYWdlTWN2RxQVUwA3VVpmU2dlRsZTUXVTV&tab_name=growth&port_name=SML_MP&call_counter=2&_=1461056696466',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1801035&enc_cust_id==AFVxI1VsRWYWdlTWN2RxQVUwA3VVpmU2dlRsZTUXVTV&tab_name=growth&port_name=SML_QS&call_counter=2&_=1461056696468',
        'https://www.zacks.com/portfolios/my-stock-portfolio/myportfoliofunction.php?portfolios_id=1801043&enc_cust_id==AFVxI1VsRWYWdlTWN2RxQVUwA3VVpmU2dlRsZTUXVTV&tab_name=growth&port_name=SML_TZ&call_counter=2&_=1461056696470'
    ]

    def parse(self, response):
        jsonresp = json.loads(response.body_as_unicode())
        for data in jsonresp['data']:
            yield {
                'ticker' : Selector(text=data[0]).xpath('//a/@rel').extract_first(),
                'earnings_date' : data[-1]
            }
