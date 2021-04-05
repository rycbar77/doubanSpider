import scrapy
from scrapy import Selector

from ..items import BookDoubanItem
from ..preprocessing.process import process_while_crawling


class Spider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/']
    bookid = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, meta={'proxy': 'http://127.0.0.1:7890'}, callback=self.parse)

    def parse(self, response):
        links = response.xpath("//*[@class='tagCol']/descendant::a/@href").extract()
        # print(links)
        # for href in links:
        #     for pageNum in np.linspace(0, 180, 10):  # 抓取每个Tag的前10页书籍
        #         full_url = response.urljoin(href + "/?start=" + str(int(pageNum)) + "&type=S")  # ?type=S  目的是按评价排序
        #         yield scrapy.Request(full_url, callback=self.parse_tag_per_page)
        for start in range(0, 41, 20):
            full_url = response.urljoin(links[0] + "/?start=%d&type=T" % start)
            yield scrapy.Request(full_url, meta={'proxy': 'http://127.0.0.1:7890'}, callback=self.parse_tag_per_page)

    def parse_tag_per_page(self, response):
        links = response.xpath("//ul[@class = 'subject-list']/descendant::a[@class = 'nbg']/@href").extract()
        for book in links:
            yield scrapy.Request(book, meta={'proxy': 'http://127.0.0.1:7890'}, callback=self.parse_book)
        # print(book)
        # yield scrapy.Request(links[0], meta={'proxy': 'http://127.0.0.1:7890'}, callback=self.parse_book)

    def parse_book(self, response):
        item = BookDoubanItem()
        sel = Selector(response)
        e = sel.xpath("//div[@id='wrapper']")
        self.bookid += 1
        item['bookid'] = self.bookid
        item['name'] = ''.join(e.xpath("./descendant::h1/descendant::span/text()").extract())

        classes = e.xpath("//*[@id='info']/span[@class='pl']/text()").extract()
        if '作者:' in classes:
            item['author'] = ';'.join(
                [i.replace('\n', '').replace(' ', '').strip() for i in
                 e.xpath("//*[@id='info']/a[1]/text()").extract()])
        else:
            item['author'] = ';'.join(e.xpath("//*[@id='info']/span[1]/a/text()").extract()).replace(' ', '')

        contents = e.xpath("//*[@id='info']/text()").extract()
        classes = [i.strip() for i in classes if '作者' not in i and '出品方' not in i and '译者' not in i and '丛书' not in i]
        real_contents = [i.strip() for i in contents if i.strip() != '']
        item['publisher'] = ''
        item['subtitle'] = ''
        item['date'] = ''
        item['price'] = ''
        for i in range(len(classes)):
            if '出版社' in classes[i]:
                item['publisher'] = ''.join(real_contents[i])
            elif '副标题' in classes[i]:
                item['subtitle'] = ''.join(real_contents[i])
            elif '出版年' in classes[i]:
                item['date'] = ''.join(real_contents[i])
            elif '定价' in classes[i]:
                item['price'] = ''.join(real_contents[i])

        item['bookintro'] = ''.join(
            e.xpath("//div[@id='link-report']/*/div[@class='intro']/p/text()").extract()).strip()
        item['score'] = e.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()').extract()
        item['commentNum'] = e.xpath(
            '//*[@id="interest_sectl"]/descendant::span[@property = "v:votes"]/text()').extract()
        item['tag'] = ','.join(response.xpath("//*[@id = 'db-tags-section']/descendant::a/text()").extract())
        item['short_comment1'] = ''.join(
            e.xpath("//div[@id='new_score']/ul/li[1]//span[@class='short']/text()").extract())
        item['short_comment2'] = ''.join(
            e.xpath("//div[@id='new_score']/ul/li[2]//span[@class='short']/text()").extract())

        comments = response.xpath("//div[@class='main-bd']/h2/a/@href").extract()[:2]

        yield scrapy.Request(comments[0], meta={'proxy': 'http://127.0.0.1:7890', 'item': item.deepcopy(),
                                                'next': comments[1]},
                             callback=self.parse_comment1)

    # yield item

    def parse_comment1(self, response):
        text = ''.join([i.replace('\n', '').strip() for i in
                        response.xpath("//div[@class='review-content clearfix']/text()").extract()])
        if text == '':
            text = ''.join(
                [i.replace('\n', '').strip() for i in
                 response.xpath("//div[@class='review-content clearfix']/p/text()").extract()])
        item = response.meta['item']
        next_comment = response.meta['next']
        item['comment1'] = text
        item['features1'] = process_while_crawling(text)
        yield scrapy.Request(next_comment, meta={'proxy': 'http://127.0.0.1:7890', 'item': item.deepcopy()},
                             callback=self.parse_comment2)

    def parse_comment2(self, response):
        text = ''.join([i.replace('\n', '').strip() for i in
                        response.xpath("//div[@class='review-content clearfix']/text()").extract()])
        if text == '':
            text = ''.join(
                [i.replace('\n', '').strip() for i in
                 response.xpath("//div[@class='review-content clearfix']/p/text()").extract()])
        item = response.meta['item']
        item['comment2'] = text
        item['features2'] = process_while_crawling(text)
        yield item
