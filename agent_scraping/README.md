# Diverse E-commerce Scraper
# Overview
A Python script for scraping e-commerce websites across categories like books, electronics, clothing, and digital content. It extracts product details (title, price, availability, etc.) and saves them to a CSV file, with error handling, random delays, and statistics generation.
# Features

Extracts product data: title, price, availability, rating, description, vendor, category, link.
Supports multiple categories and websites.
Uses flexible CSS selectors for adaptability.
Logs errors and operations to diverse_scraping.log.
Saves data to products_diverse_final.csv.
Generates category and content type statistics.

# Prerequisites

Python 3.6+
Internet access

# Installation

Clone the repository:git clone https://github.com/your-username/diverse-ecommerce-scraper.git
cd diverse-ecommerce-scraper


Install dependencies:pip install -r requirements.txt





# Usage

Run the script:
python diverse_scraper.py


# Output:
Scrapes sites (Books to Scrape, WebScraper.io, JSONPlaceholder).
Targets 800 products (adjustable in main()).
Saves data to products_diverse_final.csv.
Logs to diverse_scraping.log.
Displays statistics.



# Files

diverse_scraper.py: Main scraping script.
requirements.txt: Python dependencies.
LICENSE
products_diverse_final.csv: Output data (generated).
diverse_scraping.log: Execution logs (generated).






# Push to GitHub

Initialize Git:git init


Add files:git add .


Commit:git commit -m "Initial commit"


Link to GitHub:git remote add origin https://github.com/your-username/diverse-ecommerce-scraper.git


Push:git push -u origin main



