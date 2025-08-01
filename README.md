# Amazon Fashion Lookalikes Finder

**An AI-driven pipeline that scrapes Amazon fashion data (products/images), extracts visual embeddings with OpenAI’s CLIP model, and powers fast vector similarity search with Qdrant.**

---

## 🧰 Tech Stack

- **Scraping**: Selenium (Python) for automated Amazon data + image extraction.
- **Embeddings**: OpenAI CLIP for encoding product images.
- **Vector Database**: Qdrant (stores and searches CLIP embeddings & metadata).
- **Data Handling**: Pandas for cleaning; JSON/CSV for dataset export.

---

## 📦 Project Overview

This project aims to generate lookalike fashion product pairs ("Which one looks more expensive?") for the LIT Game using only **Amazon** data. It matches visually similar items across "expensive" and "affordable" price tiers, grouping them by category (shoes, bags, clothing, accessories) and gender.

---

## ⚙️ Pipeline Outline

1. **Amazon Data Crawling**
    - Scrapes product name, brand, price, category, gender, main image, and affiliate/product links from Amazon using Selenium.
    - Stores raw and cleaned product metadata and images locally.

2. **Price Tiering**
    - Classifies products as "expensive" (≥ ₹10,000) or "affordable" (≤ ₹4,000).
    - Optionally, allows manual brand lists for extra luxury/affordable splits.

3. **Image Embedding (OpenAI CLIP)**
    - Loads each product image and computes its CLIP vector embedding.
    - Stores image and embedding vectors, keeping category/gender tags for groupwise matching.

4. **Qdrant Vector Store**
    - Creates a collection in Qdrant to store embedding vectors + full product metadata.
    - Enables sub-second similarity (nearest neighbor) search over all embeddings.
    - Matches each "expensive" item to its most visually similar "affordable" pair.

5. **Output Matched Pairs**
    - Exports final pairs with all product details, letting users easily build a game/app UI based on this data.
