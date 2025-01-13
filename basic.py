from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# Real Bangla news dataset
news = {
    1: {
        "id": 1,
        "title": "বাংলাদেশের নির্বাচনের তারিখ ঘোষণা",
        "content": "বাংলাদেশের জাতীয় নির্বাচনের তারিখ ঘোষণা করেছে নির্বাচন কমিশন। আগামী ১০ জানুয়ারি ভোটগ্রহণ অনুষ্ঠিত হবে।",
        "author": "প্রথম আলো"
    },
    2: {
        "id": 2,
        "title": "পদ্মা সেতুর টোল কমানোর দাবি",
        "content": "পদ্মা সেতুর টোল কমানোর দাবিতে বিক্ষোভ হয়েছে মুন্সীগঞ্জে। স্থানীয় বাসিন্দারা দাবি করেছেন, টোল কমালে অর্থনীতি চাঙ্গা হবে।",
        "author": "বাংলা ট্রিবিউন"
    },
    3: {
        "id": 3,
        "title": "বাংলাদেশের ক্রিকেট দলের নতুন কোচ",
        "content": "বাংলাদেশ ক্রিকেট বোর্ড (বিসিবি) ঘোষণা করেছে যে নতুন কোচ হিসেবে স্টিভ রোডসকে নিযুক্ত করা হয়েছে।",
        "author": "বিডি নিউজ ২৪"
    },
    4: {
        "id": 4,
        "title": "বন্যার পানিতে ফসলের ক্ষতি",
        "content": "সিলেট অঞ্চলে বন্যার পানিতে কয়েকশো হেক্টর জমির ধান নষ্ট হয়েছে। কৃষকদের জন্য সরকারি সাহায্যের আহ্বান।",
        "author": "কালের কণ্ঠ"
    },
}

class News(BaseModel):
    title: str
    content: str | None = None
    author: str


@app.get("/news")
def all_news():
    return news


@app.get("/news")
def news_by_title(title_contains: str):
    for single_news in news.values():
        if title_contains.lower() in single_news["title"].lower():
            return single_news
    return {"data": "এই শিরোনামের কোনো খবর পাওয়া যায়নি: " + title_contains}


@app.get("/news/{author}")
def news_filter_by_author_title(author: str, title_contains: str = None):
    filtered_news = [single_news for single_news in news.values() if single_news["author"].lower() == author.lower()]
    if title_contains:
        filtered_news = [single_news for single_news in filtered_news if title_contains.lower() in single_news["title"].lower()]
        if not filtered_news:
            return {"data": f"লেখক {author} এর কোনো খবর পাওয়া যায়নি যার শিরোনামে {title_contains} রয়েছে।"}
    return filtered_news


@app.post("/create-news")
def create_news(response_news: News):
    id = max(news.keys()) + 1
    news[id] = {
        "id": id,
        "title": response_news.title,
        "content": response_news.content,
        "author": response_news.author
    }
    return news[id]


@app.get("/")
def root():
    return {"message": "সার্ভার চলছে এবং প্রস্তুত!"}


if __name__ == '__main__':
    uvicorn.run("basic:app", host='localhost', port=8000, reload=True)
