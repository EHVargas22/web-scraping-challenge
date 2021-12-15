# imports 
from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# scrape all function
def scrape_all():
    
    # set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # return a json with all data that can be loaded into MongoDB

    # get info from news page
    news_title, news_paragraph = scrape_news(browser)

    # build a dictionary using information from scrapes
    mars_data = {
        "newsTitle": news_title,
        "newsParagraph": news_paragraph,
        "featuredImage": scrape_featured_img(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres": scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now()
    }

    # stop the webdriver
    browser.quit()

    # display output
    return mars_data

# scrape through mars news page
def scrape_news(browser):

    # go to the Mars NASA news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # delay for loading page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # convert browser html to soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    # grab title
    news_title = slide_elem.find('div', class_='content_title').get_text()

    # grab paragraph for the headline
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    # return the title and paragraph
    return news_title, news_p

# scrape through featured image page
def scrape_featured_img(browser):
    # visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # find and click full image button
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # find image URL
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    # return the image url
    return img_url

# scrape through facts page
def scrape_facts_page(browser):

    # visit URL
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    facts_soup = soup(html, 'html.parser')

    # find facts location
    facts_location = facts_soup.find('div', class_= "diagram mt-4")

    # grab html code for facts table
    facts_table = facts_location.find('table')

    # create empty string
    facts = ""

    # add text to the empty string and return
    facts += str(facts_table)

    return facts


# scrape throug hemispheres pages
def scrape_hemispheres(browser):

    # base url
    url = "https://marshemispheres.com/"
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # set up loop & loop through each of the four pages
    for i in range(4):

        # Make hemisphere infor dictionary
        hemisphere_info = {}
    
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
    
        # Next, we find the Sample image anchor tag and extract the href
        sample = browser.links.find_by_text('Sample').first
        hemisphere_info["img_url"] = sample['href']
    
        # Get Hemisphere title
        hemisphere_info['title'] = browser.find_by_css('h2.title').text
    
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere_info)
    
        # Finally, we navigate backwards
        browser.back()

    # return hemisphere urls with titles
    return hemisphere_image_urls

# set up as a flask app
if __name__ == "__main__":
    print(scrape_all())