import re

import scrapy

from ..items import DdttItem


class MvSpider(scrapy.Spider):
    name = "mv"
    allowed_domains = ["www.ygdy8.net", "movie.douban.com"]
    start_urls = ["https://www.ygdy8.net/html/gndy/dyzz/list_23_1.html"]
    base_url = "https://www.ygdy8.net/html/gndy/dyzz/list_23_"
    page = 1

    def parse(self, response):
        # //div[@class="co_content8"]//td[2]//a/@href
        a_list = response.xpath('//div[@class="co_content8"]//td[2]//a')
        namepattern = r'《(.*?)》'
        for a in a_list:
            origin_name = a.xpath('./text()').extract_first()
            name = re.search(namepattern, origin_name).group(1)
            year = origin_name[:4]
            href = a.xpath('./@href').extract_first()
            # 热烈/惊叹号 /html/gndy/dyzz/20240526/65025.html
            # print(type(name), type(href))
            # https://www.ygdy8.net/
            # https://www.ygdy8.net/html/gndy/dyzz/20240526/65024.html
            # print(name)
            url = "https://www.ygdy8.net" + href
            # 相当于请求urllib.request，需要将name传参
            yield scrapy.Request(url=url, callback=self.parse_2, meta={"name": name, "year": year})

    # //div[@id="Zoom"]/span/text()[3]
    # //div[@id="Zoom"]/span/img/@src
    def parse_2(self, response):
        src = response.xpath('//div[@id="Zoom"]//img/@src').extract_first()
        name = response.meta["name"]
        pattern = re.compile(r'([\u4e00-\u9fa5]+)(/|$)')
        match = pattern.search(name)
        print("====================================================")
        if match:
            name = match.group(1)
            print(name)  # 输出：第二十条
        else:
            print("未找到匹配项")
        year = response.meta["year"]
        content = response.xpath('//div[@id="Zoom"]//text()').extract()

        # print(name)
        qian = len("◎产　　地　")
        area = content[5][qian:]
        genre = content[6][qian:]
        language = content[7][qian:]
        qian2 = len("◎上映日期　")
        date = content[9][qian2:][:10]

        data_list = content[10:]

        pattern1 = re.compile(r'◎豆瓣评分　(\d+\.\d+)/10 from (\d+) users')
        duration_pattern = re.compile(r'片　　长\s+(\d+)分钟')
        pattern2 = re.compile(r'演　([\u4e00-\u9fa5·]+)')

        vote = 0.0
        vote_cnt = 0
        director = None
        actor = None
        runtime = 0

        for data in data_list:
            match1 = pattern1.search(data)
            if match1:
                vote = float(match1.group(1))
                vote_cnt = int(match1.group(2))

            dmatch = duration_pattern.search(data)
            if dmatch:
                runtime = int(dmatch.group(1))

            match2 = pattern2.search(data)
            if match2:
                if not director:
                    director = match2.group(1)
                elif not actor:
                    actor = match2.group(1)

        print(area, genre, language, date, runtime)
        print("导演:", director)
        print("主演:", actor)

        movie = DdttItem(name=name, year=year, src=src, area=area, genre=genre, language=language, vote=vote,
                         vote_cnt=vote_cnt, date=date,
                         actor=actor, director=director, runtime=runtime)

        yield movie
        # 公用变量，每次下载完一页就到下一页
        if self.page <= 3:
            self.page = self.page + 1
            url = self.base_url + str(self.page) + ".html"
            # callback是需要调用的函数，这里继续调用自身函数
            yield scrapy.Request(url=url, callback=self.parse)
