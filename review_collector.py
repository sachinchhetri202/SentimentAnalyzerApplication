import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

CSV_FILE = "Reviews.csv"

def ensure_csv_exists():
    """
    Creates the CSV file with headers if it doesn't exist.
    We'll store: date, rating (1–5), and review text.
    """
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "rating", "review"])

def submit_review():
    """
    Saves the current date, rating, and review to the CSV.
    """
    rating_value = rating_scale.get()
    review_text_value = review_text.get("1.0", tk.END).strip()
    
    if not review_text_value:
        messagebox.showwarning("Input Error", "Please enter your review.")
        return
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([current_date, rating_value, review_text_value])
    
    # Optional: Show how many total reviews are in CSV
    total_reviews = get_total_reviews()
    
    messagebox.showinfo(
        "Thank You!",
        f"Your review has been submitted.\n"
        f"Current rating: {rating_value} star(s).\n"
        f"Total reviews so far: {total_reviews}"
    )
    
    # Reset fields
    rating_scale.set(3)  # default back to middle rating
    review_text.delete("1.0", tk.END)
    rating_label_var.set(f"{rating_scale.get()}")

def get_total_reviews():
    """
    Returns the total number of reviews in the CSV (excluding the header).
    """
    with open(CSV_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
        # Subtract 1 for the header row
        return len(rows) - 1

def on_rating_change(event):
    """
    Updates the label showing the current rating scale value in real time.
    """
    current_rating = rating_scale.get()
    rating_label_var.set(f"{current_rating}")

# ---------------------- MAIN UI SETUP ----------------------
root = tk.Tk()
root.title("Feedback Form - We Value Your Opinion!")
root.geometry("450x350")

# Ensure CSV file is ready
ensure_csv_exists()

# Title
title_label = ttk.Label(root, text="We'd love your feedback!", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Frame for rating
rating_frame = ttk.Frame(root)
rating_frame.pack(pady=5, fill="x")

ttk.Label(rating_frame, text="Rate your experience (1–5):", font=("Helvetica", 12)).pack(anchor="w")

# Scale for rating
rating_scale = tk.Scale(rating_frame, from_=1, to=5, orient=tk.HORIZONTAL, length=200, command=on_rating_change)
rating_scale.set(3)  # Default to middle rating
rating_scale.pack(side="left", padx=5)

# Label that shows the numeric value of the scale
rating_label_var = tk.StringVar(value="3")
rating_value_label = ttk.Label(rating_frame, textvariable=rating_label_var, font=("Helvetica", 12, "bold"))
rating_value_label.pack(side="left", padx=10)

# Frame for review text
review_frame = ttk.Frame(root)
review_frame.pack(pady=10, fill="both", expand=True)

ttk.Label(review_frame, text="Your Review:", font=("Helvetica", 12)).pack(anchor="w")

review_text = tk.Text(review_frame, height=6, width=40, wrap="word")
review_text.pack(pady=5, fill="both", expand=True)

# Submit button
submit_button = ttk.Button(root, text="Submit Review", command=submit_review)
submit_button.pack(pady=10)

root.mainloop()
