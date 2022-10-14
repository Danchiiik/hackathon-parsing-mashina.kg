import requests
from bs4 import BeautifulSoup as BS
import csv

def get_html(url):
    response = requests.get(url)
    return response.text
    
def get_soup(html):
    soup = BS(html, 'lxml')
    return soup

def get_data(soup):
    catalog = soup.find('div', class_= 'table-view-list')
    cars = catalog.find_all('div', class_ = 'list-item list-label')    
    if cars:
        for car in cars:
            try:
                title = car.find('h2', class_= 'name').text.strip()
            except AttributeError:
                title = ''
            try:
                price = car.find('strong').text
            except AttributeError:
                price = ''
            try:
                img = car.find('img', class_= 'lazy-image' ).get('data-src')
            except AttributeError:
                img = ''
            try:
                desc = car.find('p', class_='year-miles').text.strip() + ', ' + car.find('p', class_='body-type').text.strip() + ', ' + car.find('p', class_ = 'volume').text.strip()
            except AttributeError:
                desc = ''
            
            write_csv({
            'title': title,
            'image': img,
            'price': price,
            'description': desc

            })
    else:
        raise AttributeError('No more product')
            
        
        

def write_csv(data):
    with open('cars.csv', 'a')as file:
        names = ['title', 'price', 'image', 'description']
        write = csv.DictWriter(file, delimiter=',', fieldnames=names)
        write.writerow(data)      
    




def main():
    try:
        for i in range(1, 10):
            URL = f'https://www.mashina.kg/kg/specsearch/all/?type=8&page={i}'
            html = get_html(URL)
            soup = get_soup(html)
            get_data(soup)
            print(f'page {i}')
    except AttributeError:
        print('No more page')        
            

if __name__ == '__main__':
    main()