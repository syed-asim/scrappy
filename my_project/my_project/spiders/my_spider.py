import scrapy

class MySpider(scrapy.Spider):
    name = 'my_spider'
    
    def start_requests(self):
        # Define the range of pages you want to scrape
        page_range = range(1, 8)  # Change the range as needed
        
        for page_number in page_range:
            url = f"https://www.oneperfectstay.com/inspiring-homes?page={page_number}"
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        # Extract URLs from div elements with class "apartments-list-item"
        apartment_divs = response.css('div.apartments-list-item')

        for apartment_div in apartment_divs:
            data_href = apartment_div.css('div:first-child::attr(data-href)').get()  # Extract the data-href URL
            if data_href:
                yield response.follow(data_href, callback=self.parse_apartment)

    def parse_apartment(self, response):
        # Extract h3 text from the apartment page
        h3_element = response.css('div.map-details div:last-child h3::text').get()
        
        yield {
            'listing_title': h3_element,
        }
