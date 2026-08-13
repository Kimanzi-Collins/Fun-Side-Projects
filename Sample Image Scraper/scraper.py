import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Constants
API_URL = "https://ramco-group.com/wp-json/wp/v2/posts"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://ramco-group.com/',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
}

def download_image(url, filepath):
    if os.path.exists(filepath):
        print(f"  [Skipping] Already exists: {os.path.basename(filepath)}")
        return True
    
    try:
        response = requests.get(url, headers=HEADERS, stream=True, timeout=15)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"  [Downloaded] {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"  [Failed] Could not download {url}: {e}")
        return False

def scrape_articles(limit=None):
    page = 1
    articles_processed = 0
    total_downloaded = 0
    
    print("Starting scraping...")
    
    while True:
        print(f"\nFetching page {page} from API...")
        try:
            params = {
                '_embed': '1',
                'per_page': '100',
                'page': str(page)
            }
            response = requests.get(API_URL, params=params, headers=HEADERS, timeout=30)
            
            if response.status_code == 400:
                print("Reached the end of the pages.")
                break
                
            response.raise_for_status()
            posts = response.json()
            
            if not posts:
                print("No more posts found.")
                break
                
            for post in posts:
                if limit and articles_processed >= limit:
                    print(f"\nReached the limit of {limit} articles. Stopping.")
                    return
                
                # Gather image URLs
                image_urls = []
                
                # 1. Featured image
                embedded = post.get('_embedded', {})
                featured_media = embedded.get('wp:featuredmedia', [])
                if featured_media and isinstance(featured_media, list) and len(featured_media) > 0:
                    source_url = featured_media[0].get('source_url')
                    if source_url:
                        image_urls.append(source_url)
                
                # 2. Images in content
                content = post.get('content', {}).get('rendered', '')
                if content:
                    soup = BeautifulSoup(content, 'html.parser')
                    for img in soup.find_all('img'):
                        parent_a = img.find_parent('a')
                        src_to_use = None
                        
                        if parent_a and parent_a.get('href') and any(parent_a['href'].lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                            src_to_use = parent_a['href']
                        else:
                            src_to_use = img.get('src')
                            
                        if src_to_use and not src_to_use.startswith('data:'):
                            abs_url = urljoin("https://ramco-group.com", src_to_use)
                            if abs_url not in image_urls:
                                image_urls.append(abs_url)
                
                # Download images
                for url in image_urls:
                    parsed = urlparse(url)
                    path_parts = parsed.path.split('/')
                    
                    # Try to extract YYYY/MM from wp-content/uploads/YYYY/MM/...
                    year, month = None, None
                    filename = os.path.basename(parsed.path)
                    
                    if not filename or '.' not in filename:
                        # Skip if there's no valid filename with an extension
                        continue
                        
                    # find /uploads/YYYY/MM
                    for i in range(len(path_parts) - 2):
                        if path_parts[i] == 'uploads' and path_parts[i+1].isdigit() and len(path_parts[i+1]) == 4 and path_parts[i+2].isdigit():
                            year = path_parts[i+1]
                            month = path_parts[i+2]
                            break
                            
                    if not year or not month:
                        # Fallback to post date if URL doesn't have YYYY/MM
                        date_str = post.get('date', '')
                        if date_str and len(date_str) >= 7:
                            year, month = date_str[:4], date_str[5:7]
                        else:
                            year, month = "unknown_year", "00"
                            
                    img_dir = os.path.join(BASE_DIR, year, month)
                    os.makedirs(img_dir, exist_ok=True)
                    
                    filepath = os.path.join(img_dir, filename)
                    
                    success = download_image(url, filepath)
                    if success:
                        total_downloaded += 1
                
                articles_processed += 1
                
            page += 1
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    import sys
    limit = None
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        limit = 5
        print("Running in TEST mode (limit to 5 articles)")
        
    scrape_articles(limit=limit)
    print("\nScraping complete!")
