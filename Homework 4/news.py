import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

def fetch_news():
    url = "https://www.mse.mk/en/news/latest"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Successfully retrieved the webpage.")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the correct section that holds the news items
        news_items = soup.find_all('div', class_='col-md-11')  # Searching for news items
        
        print(f"Found {len(news_items)} news items.")  # Let us know how many items were found
        
        news_data = []
        for item in news_items:
            # Extract the date
            date_tag = item.find_previous('div', class_='col-md-1')
            date = date_tag.get_text(strip=True) if date_tag else 'Date not found'
            
            # Extract the title (directly from <a> tag within <div>)
            title_tag = item.find('a')
            title = title_tag.get_text(strip=True) if title_tag else 'Title not found'
            
            # Extract the summary from <p class="news-headline">
            summary_tag = item.find('p', class_='news-headline')
            summary = summary_tag.get_text(strip=True) if summary_tag else 'Summary not found'
            
            # Debugging output for missing elements
            if title == 'Title not found' or summary == 'Summary not found':
                print("Debugging missing data:")
                print(item.prettify())  # Print the raw HTML for inspection
            
            # Perform sentiment analysis using TextBlob
            blob = TextBlob(summary)
            sentiment = 'Positive' if blob.sentiment.polarity > 0 else 'Negative' if blob.sentiment.polarity < 0 else 'Neutral'
            
            # Collect the data
            news_data.append({
                'date': date,
                'title': title,
                'summary': summary,
                'sentiment': sentiment
            })
        
        return news_data
    else:
        print("Error fetching news.")
        return []

# Fetch the news data
news_data = fetch_news()

# Print the news data with sentiment
for article in news_data:
    print(f"Date: {article['date']}")
    print(f"Title: {article['title']}")
    print(f"Summary: {article['summary']}")
    print(f"Sentiment: {article['sentiment']}")
    print('-' * 50)
