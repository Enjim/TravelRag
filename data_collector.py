import wikipediaapi
import requests
import os
import time

def download_wikivoyage_article(title, output_dir="travel_data"):
    """Download Wikivoyage article using direct API."""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        # Wikivoyage API call
        url = f"https://en.wikivoyage.org/w/api.php?action=query&prop=extracts&titles={title}&format=json&explaintext=1"
        
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        pages = data['query']['pages']
        page_id = list(pages.keys())[0]
        
        if page_id != '-1':  # Article exists
            content = pages[page_id]['extract']
            
            # Save to file
            filename = f"{output_dir}/Wikivoyage_{title.replace(' ', '_')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Source: Wikivoyage\n")
                f.write(f"Title: {title}\n")
                f.write(f"Content:\n{content}")
            
            print(f"SUCCESS: Downloaded Wikivoyage: {title}")
            return filename
        else:
            print(f"ERROR: Wikivoyage article not found: {title}")
            return None
            
    except Exception as e:
        print(f"ERROR: Error downloading Wikivoyage {title}: {str(e)}")
        return None

def download_travel_articles():
    """Download travel articles from both sources."""
    
    # Wikipedia articles (using wikipediaapi)
    wikipedia_articles = ["Travel", "Tourism"]
    
    # Wikivoyage articles (using direct API)
    wikivoyage_articles = [
    # Peru
    "Peru",
    "Lima",
    "Cusco",
    "Arequipa",
    "Machu_Picchu",
    "Sacred_Valley",
    "Puno",
    "Lake_Titicaca",
    "Nazca",
    "Peruvian_Amazon",

    # Brazil
    "Brazil",
    "Rio_de_Janeiro",
    "São_Paulo",
    "Salvador",
    "Brasília",
    "Florianópolis",
    "Iguaçu_Falls",
    "Pantanal",
    "Amazon_Rainforest",

    # Regional / continental
    "South_America",

    # Travel topics
    "Backpacking",
    "Budget_travel"]

    
    print("🚀 Downloading travel articles...")

    # Download Wikivoyage articles
    for article in wikivoyage_articles:
        download_wikivoyage_article(article)
        time.sleep(1)
    
    print("SUCCESS: Done! Check the 'travel_data' folder.")

if __name__ == "__main__":
    download_travel_articles()
