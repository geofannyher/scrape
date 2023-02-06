# Import required modules


import pandas as pd #For data manipulation and analysis
import pymongo  #To interact with a MongoDB database
import streamlit as st #Used to create the GUI
import snscrape.modules.twitter as sntwitter #Library used to scrape data from social media websites, including Twitter
from PIL import Image #Imports the Image module from the Python Imaging Library (PIL) package


# Load image
image = (r"https://www.bestproxyreviews.com/wp-content/uploads/2020/05/Twitter-scraping.jpg")


# Create a GUI using streamlit
st.title("Twitter Scraping")
st.image(image, use_column_width=True)

# Create text input for the hashtag
hashtag = st.text_input("Enter the Username or Hashtag (e.g. #example)>>>")


# Connect to the database
client = pymongo.MongoClient('mongodb+srv://xotiss:<password>@cluster0.xnshvmk.mongodb.net/test')

# Mention the required database
database = "Twitter"


# Create date range input
start_date = st.date_input("Enter start date>>>")
end_date = st.date_input("Enter end date>>>")

# Also time_interval
Search = hashtag + f" since:{start_date}"+f" until:{end_date}"


# Create text input for the limit of tweets to be scraped
limit = st.number_input("Enter the limit of tweets to be scraped>>>", min_value=1, max_value=1000, value=100)


# Scrape tweets containing the hashtag
tweets = []
if hashtag:
    for tweet in sntwitter.TwitterSearchScraper(Search).get_items():
        if len(tweets)== limit:
            break
        else:
             tweets.append({'date': tweet.date, 'id': tweet.id, 'url': tweet.url,'tweet_content': tweet.content,'user': tweet.user.username, 'replyCount': tweet.replyCount, 'retweet_count': tweet.retweetCount,'language': tweet.lang, 'source': tweet.source, 'like_count': tweet.likeCount})
else:
    st.warning("Please enter a valid hashtag or username")

# Convert data to a dataframe
data = pd.DataFrame(tweets)

# Add a button to control the display of the dataframe
show_dataframe = st.button("Show Dataframe")

# Display the dataframe only when the button is pressed
if show_dataframe:
    st.dataframe(data)


# Add a button to upload the data to the database
if st.button('Upload to database'):

      #Required_Database
      db = client[database]

      # Creates a new collection name in database.
      collection = db[str(limit)+'_'+hashtag+"_"+str(start_date)+"_"+str(end_date)]

      # Converts the pandas dataframe data into a dictionary format,where each row of the dataframe is converted into dictionary
      # Keys as the column names and the values as the corresponding cell values
      data_dict = data.to_dict("records")

      # Inserts the dataframe in selected collection.
      collection.insert_many(data_dict)

      #Finally
      st.success('Data uploaded to the database')


# Add a button to download the data in CSV format
if st.button('Download as CSV'):
    data.to_csv(f"{str(limit)+'_'+hashtag+'_'+str(start_date)+'_'+str(end_date)}_tweets.csv", index=False)
    st.success('Data downloaded as CSV')

# Add a button to download the data in JSON format
if st.button('Download as JSON'):
    data.to_json(f"{str(limit)+'_'+hashtag+'_'+str(start_date)+'_'+str(end_date)}_tweets.json",orient='records', force_ascii=False, indent=4, default_handler=str)
    st.success('Data downloaded as JSON')

