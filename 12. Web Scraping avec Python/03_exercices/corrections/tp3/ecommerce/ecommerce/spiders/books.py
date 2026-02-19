import scrapy
from ecommerce.items import BookItem, CategoryItem
import re


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

    def parse(self, response):
        """Parse page categories"""
        # Navigation vers détail livre
        for book in response.css('article.product_pod'):
            book_url = book.css('h3 a::attr(href)').get()
            yield response.follow(book_url, self.parse_book)
        
        # Pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        """Parse page détail livre"""
        item = BookItem()
        
        # Informations principales
        item['title'] = response.css('h1::text').get()
        
        price_text = response.css('p.price_color::text').get()
        item['price'] = float(re.findall(r'[\d.]+', price_text)[0])
        
        rating_class = response.css('p.star-rating::attr(class)').get()
        rating_text = rating_class.split()[1]
        item['rating'] = self.rating_map.get(rating_text, 0)
        
        item['availability'] = response.css('p.instock.availability::text').getall()[1].strip()
        
        # Description
        desc = response.css('#product_description + p::text').get()
        item['description'] = desc.strip() if desc else ''
        
        # Catégorie (breadcrumb)
        breadcrumb = response.css('ul.breadcrumb li')
        if len(breadcrumb) >= 3:
            item['category'] = breadcrumb[2].css('a::text').get()
        
        # Image
        img_url = response.css('img::attr(src)').get()
        item['image_url'] = response.urljoin(img_url)
        
        # URL produit
        item['product_url'] = response.url
        
        # UPC (table)
        upc = response.xpath('//th[text()="UPC"]/following-sibling::td/text()').get()
        item['upc'] = upc
        
        yield item