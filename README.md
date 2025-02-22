# Analyzing 40 Years of Nick Cave’s Lyrics: A Sentiment Deep Dive  

Has the sentiment in Nick Cave's lyrics changed over time? That’s what I set out to explore by analyzing his lyrics from the past 40 years.  

## Step 1: Building the Database  

To begin, I needed a structured dataset of Cave’s lyrics. I created an [**SQL database**](create_database.py) to store each song’s title, album name, release year, and lyrics.  

At first, I attempted to scrape the lyrics directly from [azlyrics.com](https://www.azlyrics.com), but while testing the code, the site eventually blocked my requests due to suspicious behavior. As a workaround, I used a dataset of HTML files containing the lyrics.  

Using **BeautifulSoup**, I parsed the HTML files to extract:  
✅ **Lyrics** (cleaned and formatted)  
✅ **Song title** (from embedded JavaScript)  
✅ **Album name & release year** (from the page’s metadata)  

All extracted data was then inserted into my **SQLite database**.  

## Step 2: Sentiment Analysis  

With the lyrics stored, it was time to analyze their sentiment. I opted for a **lexicon-based approach** using a sentiment file (`subjclueslen1-HLTEMNLP05.tff`).  

Here’s how I calculated sentiment scores:  
🔹 **Parsing the sentiment file:** This lexicon contains words labeled as positive or negative, with strength indicators.  
🔹 **Scoring lyrics:** Each word in a song was matched against the lexicon. Positive words increased the score, and negative words decreased it. Stronger words had **double impact**.  
🔹 **Updating the database:** I added a `sentiment_score` column and stored each song’s calculated sentiment value.  

## Step 3: Visualizing the Insights  

Once the sentiment scores were ready, I exported the database into an **Excel file** for visualization in Tableau.  

Using **interactive filters and slicers**, the Tableau dashboard allows users to:  
📊 Explore sentiment trends over time  
📅 Filter by album or decade  
🎵 Compare the sentiment of different songs  

## The Takeaway  

This project uncovered fascinating insights into Nick Cave’s lyrical evolution. Some albums show a sharp shift in tone, while others maintain a consistent emotional depth. By mapping sentiment over time, we get a data-driven glimpse into how Cave’s songwriting has changed.  

For those interested, you can check out the **Tableau Public link**.  

