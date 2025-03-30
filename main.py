"""
main.py
========
Author: Sachin Chhetri
Date: 3/30/2025
Description:
    This is the main file for the Local Business Sentiment Analyzer application.
    The application provides a graphical interface for loading, analyzing, filtering,
    and sorting review data. It uses both basic (TextBlob) and advanced (Hugging Face Transformers)
    sentiment analysis methods. Users can compare the outputs of both NLP methods and view topic
    extraction from reviews.
    
    The application workflow is:
        - Load reviews from a CSV file (using fetch_reviews from review_fetcher.py)
        - Analyze reviews using either a basic or advanced NLP method
        - Filter and sort the reviews based on date or sentiment
        - Compare the outputs of the two NLP methods side by side
        - Display sentiment distribution and extracted topics using plots and pop-up dialogs

Dependencies:
    - tkinter, ttk, messagebox for the GUI.
    - matplotlib for plotting.
    - pandas for data handling.
    - review_fetcher.py and review_analyzer.py for data loading and NLP tasks.
    
Usage:
    Run this file directly to launch the GUI application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import pandas as pd 
from review_fetcher import fetch_reviews
from review_analyzer import analyze_sentiment, analyze_sentiment_advanced, perform_topic_modeling

class SentimentAnalyzerApp:
    """
    Initialize the main application window.
    Sets up the window title, size, and initializes data containers.
    Then calls create_widgets() to build the UI.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Local Business Sentiment Analyzer")
        self.master.geometry("900x850")
        self.data = None          # Holds all loaded reviews
        self.current_data = None  # Holds currently displayed (filtered/sorted) reviews
        self.create_widgets()
        
    def create_widgets(self):
        """
        Build the user interface.
        Creates and organizes frames for buttons, filtering, sorting, and displays the review table.
        """
        # Top Buttons Frame
        buttons_frame = tk.Frame(self.master)
        buttons_frame.pack(pady=5)

        load_button = tk.Button(buttons_frame, text="Load Reviews", command=self.load_reviews)
        load_button.grid(row=0, column=0, padx=5)

        analyze_button = tk.Button(buttons_frame, text="Analyze Reviews", command=self.analyze_reviews)
        analyze_button.grid(row=0, column=1, padx=5)

        sentiment_button = tk.Button(buttons_frame, text="Show Sentiment Distribution", command=self.show_sentiment_distribution)
        sentiment_button.grid(row=0, column=2, padx=5)

        topics_button = tk.Button(buttons_frame, text="Show Topics", command=self.show_topics)
        topics_button.grid(row=0, column=3, padx=5)

        clear_button = tk.Button(buttons_frame, text="Clear Reviews", command=self.clear_reviews)
        clear_button.grid(row=0, column=4, padx=5)

        # Compare NLP Results button to compare basic and advanced sentiment analysis side by side.
        compare_btn = ttk.Button(buttons_frame, text="Compare NLP Results", command=self.compare_nlp_results)
        compare_btn.grid(row=0, column=5, padx=5)

        # Advanced NLP Toggle: Check this if you want to use the advanced (Transformers) method.
        self.use_advanced = tk.BooleanVar()
        advanced_check = tk.Checkbutton(buttons_frame, text="Use Advanced NLP", variable=self.use_advanced)
        advanced_check.grid(row=0, column=6, padx=5)
        
        # Filter Frame for Date Range - Allows users to filter reviews by start and end date.
        filter_frame = tk.Frame(self.master)
        filter_frame.pack(pady=5)
        
        tk.Label(filter_frame, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5)
        self.start_date_entry = tk.Entry(filter_frame, width=12)
        self.start_date_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(filter_frame, text="End Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5)
        self.end_date_entry = tk.Entry(filter_frame, width=12)
        self.end_date_entry.grid(row=0, column=3, padx=5)
        
        filter_button = tk.Button(filter_frame, text="Filter Reviews", command=self.filter_reviews)
        filter_button.grid(row=0, column=4, padx=5)
        
        # Sort Frame for Sorting Options - Enables sorting of reviews by date or sentiment.
        sort_frame = tk.Frame(self.master)
        sort_frame.pack(pady=5)
        
        tk.Label(sort_frame, text="Sort By:").grid(row=0, column=0, padx=5)
        self.sort_option = tk.StringVar(value="Date Ascending")
        sort_options = ["Date Ascending", "Date Descending", "Sentiment Ascending", "Sentiment Descending"]
        sort_menu = ttk.OptionMenu(sort_frame, self.sort_option, sort_options[0], *sort_options)
        sort_menu.grid(row=0, column=1, padx=5)
        
        sort_button = tk.Button(sort_frame, text="Sort Data", command=self.sort_data)
        sort_button.grid(row=0, column=2, padx=5)
        
        # Treeview for Displaying Reviews
        columns = ("Date", "Review", "Sentiment", "Polarity")
        self.tree = ttk.Treeview(self.master, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200 if col=="Review" else 120)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Label to Show Total Reviews Count
        self.total_label = tk.Label(self.master, text="Total Reviews: 0", font=("Helvetica", 12))
        self.total_label.pack(pady=5)

    def compare_nlp_results(self):
        """
        Compare the results of basic and advanced NLP methods for a selected review.
        The user must select a review from the table.
        The function then runs both NLP methods on that review and shows a pop-up
        with the results side by side for comparison.
        """
        # Get the currently selected review from the Treeview
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a review from the list to compare NLP results.")
            return
        # Assuming the second column is the review text
        review_text_value = self.tree.item(selected[0])["values"][1]
        
        # Run both NLP methods on the selected review
        basic_label, basic_polarity = analyze_sentiment(review_text_value)
        advanced_label, advanced_score = analyze_sentiment_advanced(review_text_value)
        
        # Format the results for display
        result_message = (
            f"Review:\n\"{review_text_value}\"\n\n"
            f"Basic NLP (TextBlob):\n"
            f"  Sentiment: {basic_label}\n"
            f"  Polarity: {basic_polarity:.2f}\n\n"
            f"Advanced NLP (Transformers):\n"
            f"  Sentiment: {advanced_label}\n"
            f"  Confidence Score: {advanced_score:.2f}\n\n"
            "Which result seems more accurate to you?"
        )
        messagebox.showinfo("NLP Comparison", result_message)

    
    def load_reviews(self):
        """
        Load review data from the CSV file using fetch_reviews().
        If data is successfully loaded, store it in self.data and self.current_data,
        then display the reviews in the table and update the total count.
        """
        df = fetch_reviews()
        if df is None or df.empty:
            messagebox.showerror("Error", "No reviews loaded!")
            return
        self.data = df
        self.current_data = df.copy()  # Initially, all data is shown.
        self.populate_tree(self.current_data)
        self.total_label.config(text=f"Total Reviews: {len(self.current_data)}")
    
    def populate_tree(self, df):
        """
        Populate the Treeview with review data.
        Clears any existing entries and inserts rows from the DataFrame.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert rows
        for idx, row in df.iterrows():
            date_str = row['date'].strftime("%Y-%m-%d") if isinstance(row['date'], pd.Timestamp) else row['date']
            sentiment = row.get('Sentiment', "")
            polarity = f"{row.get('Polarity', 0):.2f}" if 'Polarity' in row else ""
            self.tree.insert("", tk.END, values=(date_str, row['review'], sentiment, polarity))
    
    def analyze_reviews(self):
        """
        Analyze the sentiment of all reviews currently loaded (or filtered).
        Applies either the basic or advanced NLP method based on the toggle.
        Updates the DataFrame with sentiment labels and polarity/confidence scores,
        then refreshes the Treeview.
        """
        if self.current_data is None or self.current_data.empty:
            messagebox.showerror("Error", "Load reviews first!")
            return
        
        sentiments = []
        polarities = []
        # Use advanced NLP if toggle is checked
        for index, row in self.current_data.iterrows():
            if self.use_advanced.get():
                sentiment, polarity = analyze_sentiment_advanced(row['review'])
            else:
                sentiment, polarity = analyze_sentiment(row['review'])
            sentiments.append(sentiment)
            polarities.append(polarity)
        self.current_data['Sentiment'] = sentiments
        self.current_data['Polarity'] = polarities
        self.populate_tree(self.current_data)
        messagebox.showinfo("Analysis Complete", "Reviews have been analyzed.")
    
    def clear_reviews(self):
        """
        Clear all review data from the application.
        Resets the data containers and clears the Treeview.
        """
        self.data = None
        self.current_data = None
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.total_label.config(text="Total Reviews: 0")
    
    def filter_reviews(self):
        """
        Filter the loaded reviews based on a date range entered by the user.
        The start and end dates are read from the corresponding entry fields.
        Updates the current data and refreshes the Treeview with the filtered set.
        """
        if self.data is None or self.data.empty:
            messagebox.showerror("Error", "Load reviews first!")
            return
        start_date_str = self.start_date_entry.get().strip()
        end_date_str = self.end_date_entry.get().strip()
        try:
            if start_date_str:
                start_date = pd.to_datetime(start_date_str)
            else:
                start_date = self.data['date'].min()
            if end_date_str:
                end_date = pd.to_datetime(end_date_str)
            else:
                end_date = self.data['date'].max()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid date format: {e}")
            return
        
        # Filter the data based on the date range
        filtered_data = self.data[(self.data['date'] >= start_date) & (self.data['date'] <= end_date)]
        if filtered_data.empty:
            messagebox.showinfo("Info", "No reviews found in this date range.")
        else:
            self.current_data = filtered_data.copy()
            self.populate_tree(self.current_data)
            self.total_label.config(text=f"Total Reviews: {len(self.current_data)}")
    
    def sort_data(self):
        """
        Sort the reviews based on the selected option (date or sentiment).
        Options include ascending or descending order.
        Updates the current data and refreshes the Treeview.
        """
        if self.current_data is None or self.current_data.empty:
            messagebox.showerror("Error", "No data to sort!")
            return
        option = self.sort_option.get()
        # Sort based on the chosen option
        if option == "Date Ascending":
            sorted_data = self.current_data.sort_values(by='date', ascending=True)
        elif option == "Date Descending":
            sorted_data = self.current_data.sort_values(by='date', ascending=False)
        elif option == "Sentiment Ascending":
            sorted_data = self.current_data.sort_values(by='Sentiment', ascending=True)
        elif option == "Sentiment Descending":
            sorted_data = self.current_data.sort_values(by='Sentiment', ascending=False)
        else:
            sorted_data = self.current_data
        self.current_data = sorted_data.copy()
        self.populate_tree(self.current_data)
    
    def show_sentiment_distribution(self):
        """
        Display a bar chart showing the distribution of sentiment labels
        for the reviews currently displayed.
        """
        if self.current_data is None or 'Sentiment' not in self.current_data.columns:
            messagebox.showerror("Error", "Please analyze reviews first!")
            return
        counts = self.current_data['Sentiment'].value_counts()
        counts.plot(kind="bar", color="skyblue", title="Sentiment Distribution")
        plt.xlabel("Sentiment")
        plt.ylabel("Count")
        plt.show()
    
    def show_topics(self):
        """
        Extract topics from the currently displayed reviews using topic modeling.
        Displays the extracted topics in a message box.
        """
        if self.current_data is None or self.current_data.empty:
            messagebox.showerror("Error", "Load and analyze reviews first!")
            return
        reviews = self.current_data['review'].tolist()
        topics = perform_topic_modeling(reviews, num_topics=3)
        topics_str = "\n".join(topics)
        messagebox.showinfo("Extracted Topics", topics_str)
        
if __name__ == "__main__":
    # Create the main window and launch the Sentiment Analyzer application.
    root = tk.Tk()
    app = SentimentAnalyzerApp(root)
    root.mainloop()
