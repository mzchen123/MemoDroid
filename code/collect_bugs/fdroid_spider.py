import scrapy
import os
from datetime import datetime
import csv
from scrapy.exceptions import CloseSpider
from scrapy.http import Request

class FdroidInfoSpider(scrapy.Spider):
    name = 'f-droid-info-spider'
    start_urls = ['https://f-droid.org/en/categories/connectivity/', 'https://f-droid.org/en/categories/connectivity/2/index.html', 'https://f-droid.org/en/categories/connectivity/3/index.html', 'https://f-droid.org/en/categories/connectivity/4/index.html', 'https://f-droid.org/en/categories/connectivity/5/index.html', 'https://f-droid.org/en/categories/development/', 'https://f-droid.org/en/categories/development/2/index.html', 'https://f-droid.org/en/categories/development/3/index.html', 'https://f-droid.org/en/categories/development/4/index.html', 'https://f-droid.org/en/categories/development/5/index.html', 'https://f-droid.org/en/categories/games/', 'https://f-droid.org/en/categories/games/2/index.html', 'https://f-droid.org/en/categories/games/3/index.html', 'https://f-droid.org/en/categories/games/4/index.html', 'https://f-droid.org/en/categories/games/5/index.html', 'https://f-droid.org/en/categories/graphics/', 'https://f-droid.org/en/categories/graphics/2/index.html', 'https://f-droid.org/en/categories/graphics/3/index.html', 'https://f-droid.org/en/categories/graphics/4/index.html', 'https://f-droid.org/en/categories/graphics/5/index.html', 'https://f-droid.org/en/categories/internet/', 'https://f-droid.org/en/categories/internet/2/index.html', 'https://f-droid.org/en/categories/internet/3/index.html', 'https://f-droid.org/en/categories/internet/4/index.html', 'https://f-droid.org/en/categories/internet/5/index.html', 'https://f-droid.org/en/categories/money/', 'https://f-droid.org/en/categories/money/2/index.html', 'https://f-droid.org/en/categories/money/3/index.html', 
'https://f-droid.org/en/categories/money/4/index.html', 'https://f-droid.org/en/categories/money/5/index.html', 'https://f-droid.org/en/categories/multimedia/', 'https://f-droid.org/en/categories/multimedia/2/index.html', 'https://f-droid.org/en/categories/multimedia/3/index.html', 'https://f-droid.org/en/categories/multimedia/4/index.html', 'https://f-droid.org/en/categories/multimedia/5/index.html', 'https://f-droid.org/en/categories/navigation/', 'https://f-droid.org/en/categories/navigation/2/index.html', 'https://f-droid.org/en/categories/navigation/3/index.html', 'https://f-droid.org/en/categories/navigation/4/index.html', 'https://f-droid.org/en/categories/navigation/5/index.html', 'https://f-droid.org/en/categories/phone-sms/', 'https://f-droid.org/en/categories/phone-sms/2/index.html', 'https://f-droid.org/en/categories/phone-sms/3/index.html', 'https://f-droid.org/en/categories/phone-sms/4/index.html', 'https://f-droid.org/en/categories/phone-sms/5/index.html', 'https://f-droid.org/en/categories/reading/', 'https://f-droid.org/en/categories/reading/2/index.html', 'https://f-droid.org/en/categories/reading/3/index.html', 'https://f-droid.org/en/categories/reading/4/index.html', 'https://f-droid.org/en/categories/reading/5/index.html', 'https://f-droid.org/en/categories/reading/', 'https://f-droid.org/en/categories/reading/2/index.html', 'https://f-droid.org/en/categories/reading/3/index.html', 'https://f-droid.org/en/categories/reading/4/index.html', 'https://f-droid.org/en/categories/reading/5/index.html', 'https://f-droid.org/en/categories/security/', 'https://f-droid.org/en/categories/security/2/index.html', 'https://f-droid.org/en/categories/security/3/index.html', 'https://f-droid.org/en/categories/security/4/index.html', 'https://f-droid.org/en/categories/security/5/index.html', 'https://f-droid.org/en/categories/sports-health/', 'https://f-droid.org/en/categories/sports-health/2/index.html', 'https://f-droid.org/en/categories/sports-health/3/index.html', 'https://f-droid.org/en/categories/sports-health/4/index.html', 'https://f-droid.org/en/categories/sports-health/5/index.html', 'https://f-droid.org/en/categories/system/', 'https://f-droid.org/en/categories/system/2/index.html', 'https://f-droid.org/en/categories/system/3/index.html', 'https://f-droid.org/en/categories/system/4/index.html', 'https://f-droid.org/en/categories/system/5/index.html', 'https://f-droid.org/en/categories/theming/', 'https://f-droid.org/en/categories/theming/2/index.html', 'https://f-droid.org/en/categories/theming/3/index.html', 'https://f-droid.org/en/categories/theming/4/index.html', 'https://f-droid.org/en/categories/theming/5/index.html', 'https://f-droid.org/en/categories/time/', 'https://f-droid.org/en/categories/time/2/index.html', 'https://f-droid.org/en/categories/time/3/index.html', 'https://f-droid.org/en/categories/time/4/index.html', 'https://f-droid.org/en/categories/time/5/index.html', 'https://f-droid.org/en/categories/writing/', 'https://f-droid.org/en/categories/writing/2/index.html', 'https://f-droid.org/en/categories/writing/3/index.html', 'https://f-droid.org/en/categories/writing/4/index.html', 'https://f-droid.org/en/categories/writing/5/index.html']
    item_count = 0
    max_items = 2000
    csv_file = 'fdroid_data.csv'
    
    def __init__(self, *args, **kwargs):
        super(FdroidInfoSpider, self).__init__(*args, **kwargs)
        # Create CSV file and write header
        with open(self.csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['APP Name', 'F-Droid Link', 'Last Updated', 'APP Description', 'Github Repository', 'Category'])

    def parse(self, response):
        base_url = 'https://f-droid.org/en/packages'
        # Extract category information from URL
        category = response.url.split('/categories/')[1].split('/')[0]

        for href in response.css('a.package-header ::attr("href")').extract():
            yield Request(
                url=response.urljoin(href),
                callback=self.parse_app_info,
                meta={'category': category}  # Pass category information to the next callback function
            )

        # Get the next page's link
        next_page_relative_url = response.css('li.nav.next > a::attr(href)').get()

        # Use response.follow to build the full URL and make a new request
        if next_page_relative_url:
            # print('next page relative url:', next_page_relative_url)
            # input('stop')
            yield Request(
                url=response.urljoin(href),
                callback=self.parse_app_info,
                meta={'category': category}  # Pass category information to the next callback function
            )

        for href in response.css('a.post-link ::attr("href")').extract():
            # print('next page sub page:', next_page_relative_url)
            # input('stop here')
            yield Request(
                url=response.urljoin(href),
                callback=self.parse_app_info,
                meta={'category': category}  # Pass category information to the next callback function
            )

    def parse_app_info(self, response):
        if self.item_count >= self.max_items:
            raise CloseSpider('Reached 2000 data limit')

        app_name = response.css('h3.package-name::text').get().strip()
        fdroid_link = response.url
        last_updated_detailed = response.css('div.package-version-header::text').getall()
        if last_updated_detailed:
            # Iterate through the extracted text fragments to find the one containing "Added on"
            for text_part in last_updated_detailed:
                if "Added on" in text_part:
                    last_updated = text_part.replace("Added on ", "").split(" == $")[0].strip()
                    # print(f"Correct detailed update date: {last_updated}")
                    break
            else:
                print("Could not find detailed update date information containing 'Added on'")
        else:
            print("Could not find package-version-header element")
        github_link = response.css('li.package-link:contains("Source Code") a::attr(href)').get()
        description_elements = response.css('div.package-description::text').getall()
        description_text = ''.join(element.strip() for element in description_elements if element.strip())

        last_updated_str = last_updated

        try:
            # Parse the string in "Apr 25, 2025" format into a datetime object
            datetime_object = datetime.strptime(last_updated_str, '%b %d, %Y')
            # Format the datetime object into "yy-mm-dd" format
            last_updated_formatted = datetime_object.strftime('%y-%m-%d')
        except ValueError:
            # If the date format does not match, keep the original string or set to None, and print error message
            last_updated_formatted = last_updated_str
            print(f"Warning: Could not parse date string: {last_updated_str}")

        print('APP Name', app_name)
        print('fdroid link', fdroid_link)
        print('last updated', last_updated_formatted)
        print('github link', github_link)
        print('description', description_text)
        # input('stop here')

        item = {
            'APP Name': app_name,
            'F-Droid Link': fdroid_link,
            'Last Updated': last_updated_formatted,
            'APP Description': description_text,
            'Github Repository': github_link,
            'Category': response.meta['category']  # Add category information
        }

        # Write to CSV file in real-time
        with open(self.csv_file, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                item['APP Name'],
                item['F-Droid Link'],
                item['Last Updated'],
                item['APP Description'],
                item['Github Repository'],
                item['Category']
            ])

        self.item_count += 1
        self.logger.info(f'Collected {self.item_count} items')

        yield item