# review_analyzer.py
#
# This file provides functions to perform sentiment analysis and topic modeling on review texts.
#
# We use two different methods for sentiment analysis:
#   1. A basic method using TextBlob – which computes a simple polarity score.
#   2. An advanced method using a Hugging Face Transformers pipeline – which is more context-aware.
#
# In addition, we provide a function to perform topic modeling using Non-negative Matrix Factorization (NMF)
# on a collection of reviews. This can help extract common themes or topics from the text.
#
# Note: The advanced sentiment analysis pipeline may download model files the first time you run it.

from textblob import TextBlob
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF

# Load the advanced sentiment analysis pipeline from Hugging Face.
# This pipeline is pre-trained to classify text sentiment and returns a label (e.g., "POSITIVE")
# along with a confidence score.
advanced_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    """
    Perform basic sentiment analysis using TextBlob.
    
    This function takes a review text as input, computes its sentiment polarity (a number between -1 and 1),
    and assigns a label based on the polarity:
      - Polarity > 0.1  -> "Positive"
      - Polarity < -0.1 -> "Negative"
      - Otherwise      -> "Neutral"
    
    Parameters:
        text (str): The text of the review to analyze.
    
    Returns:
        tuple: A tuple containing the sentiment label and the polarity score.
    """
    # Create a TextBlob object from the text.
    blob = TextBlob(text)
    # Get the sentiment polarity (range: -1.0 to 1.0)
    polarity = blob.sentiment.polarity
    # Determine the sentiment label based on thresholds.
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
    return label, polarity

def analyze_sentiment_advanced(text):
    """
    Perform advanced sentiment analysis using Hugging Face Transformers.
    
    This function uses a pre-trained Transformer model to analyze the sentiment of the input text.
    The output is a label (e.g., "POSITIVE" or "NEGATIVE") and a confidence score indicating how sure
    the model is about its prediction.
    
    Parameters:
        text (str): The review text to analyze.
    
    Returns:
        tuple: A tuple containing the sentiment label and the confidence score.
    """
    # Run the text through the advanced pipeline.
    result = advanced_pipeline(text)
    # The result is a list of dictionaries; we take the first element.
    label = result[0]["label"]
    score = result[0]["score"]
    return label, score

def perform_topic_modeling(reviews, num_topics=3, num_words=5):
    """
    Perform topic modeling on a list of reviews using Non-negative Matrix Factorization (NMF).
    
    This function vectorizes the input reviews using a bag-of-words approach (ignoring common English stop words),
    applies NMF to extract the specified number of topics, and then returns a list of topics with their top words.
    
    Parameters:
        reviews (list): A list of review texts.
        num_topics (int): The number of topics to extract. Default is 3.
        num_words (int): The number of top words to display for each topic. Default is 5.
    
    Returns:
        list: A list of strings, each describing a topic with its most representative words.
    """
    # Convert the list of reviews into a bag-of-words representation,
    # ignoring common words that don't add much meaning.
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(reviews)
    
    # Apply NMF to the document-term matrix to extract topics.
    nmf = NMF(n_components=num_topics, random_state=42)
    nmf.fit(X)
    H = nmf.components_
    
    # Get the words corresponding to each feature.
    feature_names = vectorizer.get_feature_names_out()
    
    topics = []
    # Loop through each topic and identify the top words.
    for topic_idx, topic in enumerate(H):
        # Get indices of the top words for this topic.
        top_words = [feature_names[i] for i in topic.argsort()[:-num_words - 1:-1]]
        topics.append(f"Topic {topic_idx+1}: " + ", ".join(top_words))
    
    return topics