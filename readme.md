# 🧠 ChaiDocs AI Assistant

An intelligent assistant that scrapes [ChaiDocs](https://chaidocs.vercel.app/youtube/getting-started/) and its linked documentation pages, performs vector embeddings, stores them in a Qdrant vector database, and uses OpenAI to generate context-aware answers to user questions.

---

## ✨ Features

- 🔍 **Web Scraping**  
  Scrapes the ChaiDocs homepage and all internally linked documentation pages.

- 🧠 **Vector Embeddings**  
  Embeds scraped content using OpenAI's embedding API and stores vectors in Qdrant.

- 🔎 **Semantic Search**  
  Performs similarity search on Qdrant vectors to find relevant chunks for a given query.

- 🤖 **AI-Powered Response**  
  Sends retrieved context to OpenAI's GPT model to generate accurate, context-rich answers.

- 🐳 **Dockerized Setup**  
  Fully containerized — just clone the repo, add your `.env`, and you're ready to go!

---

## 🧰 Tech Stack

- **Python 3.10+**
- **BeautifulSoup / Requests** – For scraping
- **Qdrant** – Vector database
- **OpenAI API** – For embeddings + GPT-based responses
- **FastAPI / Flask** – (Depending on your implementation) for serving the app
- **Docker** – For containerized deployment

---