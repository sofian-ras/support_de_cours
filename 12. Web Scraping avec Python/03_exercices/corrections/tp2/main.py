import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from urllib.parse import urljoin

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = 'http://quotes.toscrape.com'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
MAX_PAGES = 10
DELAY = 1

def fetch_page(url):
    """Récupère une page"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'lxml')
    except Exception as e:
        logger.error(f"Erreur pour {url}: {e}")
        return None
    
def extract_quotes_from_page(soup, page_url):
    """Extrait les citations d'une page"""
    quotes_data = []
    quotes = soup.find_all('div', class_='quote')
    
    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        
        # URL de l'auteur
        author_link = quote.find('a', href=True)
        author_url = urljoin(BASE_URL, author_link['href']) if author_link else None
        
        quotes_data.append({
            'text': text,
            'author': author,
            'tags': ', '.join(tags),
            'author_url': author_url,
            'page_url': page_url
        })
    
    return quotes_data


def get_next_page_url(soup, current_url):
    """Trouve l'URL de la page suivante"""
    next_button = soup.find('li', class_='next')
    if next_button:
        next_link = next_button.find('a')['href']
        return urljoin(current_url, next_link)
    return None

def scrape_all_pages():
    """Scrape toutes les pages"""
    all_quotes = []
    current_url = BASE_URL
    page_num = 1
    
    while current_url and page_num <= MAX_PAGES:
        logger.info(f"Scraping page {page_num}: {current_url}")
        
        soup = fetch_page(current_url)
        if not soup:
            break
        
        # Extraire citations
        quotes = extract_quotes_from_page(soup, current_url)
        all_quotes.extend(quotes)
        logger.info(f"{len(quotes)} citations extraites")
        
        # Page suivante
        current_url = get_next_page_url(soup, current_url)
        page_num += 1
        
        # Délai
        if current_url:
            time.sleep(DELAY)
    
    return all_quotes

def create_statistics(df):
    """Crée les feuilles d'analyse"""
    # Auteurs
    authors_df = df.groupby('author').agg({
        'text': 'count'
    }).reset_index()
    authors_df.columns = ['author', 'nb_citations']
    authors_df = authors_df.sort_values('nb_citations', ascending=False)
    
    # Tags (exploser les tags séparés par virgule)
    all_tags = []
    for tags_str in df['tags']:
        all_tags.extend([tag.strip() for tag in tags_str.split(',')])
    
    tags_df = pd.DataFrame({'tag': all_tags})
    tags_df = tags_df.groupby('tag').size().reset_index(name='frequency')
    tags_df = tags_df.sort_values('frequency', ascending=False)
    
    return authors_df, tags_df

def main():
    logger.info("="*60)
    logger.info("DÉMARRAGE DU SCRAPER")
    logger.info("="*60)
    
    # Scraper
    quotes = scrape_all_pages()
    logger.info(f"\n Total : {len(quotes)} citations scrapées")
    
    # DataFrame
    df = pd.DataFrame(quotes)
    df['text_length'] = df['text'].str.len()
    
    # Statistiques
    authors_df, tags_df = create_statistics(df)
    
    # Afficher stats
    print(f"\n STATISTIQUES")
    print(f"  - Total citations : {len(df)}")
    print(f"  - Auteurs uniques : {df['author'].nunique()}")
    print(f"  - Longueur moyenne : {df['text_length'].mean():.0f} caractères")
    
    print(f"\n Top 5 auteurs :")
    print(authors_df.head(5).to_string(index=False))
    
    print(f"\n Top 10 tags :")
    print(tags_df.head(10).to_string(index=False))
    
    # Sauvegarder Excel
    with pd.ExcelWriter('quotes_complet.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Citations', index=False)
        authors_df.to_excel(writer, sheet_name='Auteurs', index=False)
        tags_df.to_excel(writer, sheet_name='Tags', index=False)
    
    logger.info(f"\n Fichier créé : quotes_complet.xlsx")

if __name__ == '__main__':
    main()