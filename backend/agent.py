import praw
import openai
import schedule
import time
import os
import tiktoken
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),   
    user_agent=os.getenv('REDDIT_USER_AGENT')      
)

openai.base_url = os.getenv('OPENAI_BASE_URL')
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_type = os.getenv('OPENAI_API_TYPE')
model = os.getenv('OPENAI_MODEL')

def search_posts(subreddit_name, query, prompt):
    subreddit = reddit.subreddit(subreddit_name)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    posts = []
    for submission in subreddit.search(query, limit=200):
        if datetime.utcfromtimestamp(submission.created_utc) >= thirty_days_ago:
            posts.append(f"Title: {submission.title}\n\n{submission.selftext}")

    comments = []
    for comment in subreddit.comments(limit=1000):
        if query in comment.body.lower() and datetime.utcfromtimestamp(comment.created_utc) >= thirty_days_ago:
            comments.append(comment.body)

    content = f"The following are Reddit posts and comments related to '{query}' in r/{subreddit_name} from the last 30 days:\n\n. Please give in plain text no markdown or bold things"
    content += "\n\n".join(posts + comments)

    full_prompt = f"{content}\n\n{prompt}"

    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": full_prompt},
        ],
    )

    encoding = tiktoken.encoding_for_model(model)
    input_tokens = encoding.encode(full_prompt)
    output_tokens = encoding.encode(response.__str__())

    response_text = response.choices[0].message.content

    return {
        "response_text": response_text,
        "token_usage": {
            "completion_tokens": len(output_tokens),
            "prompt_tokens": len(input_tokens),
            "total_tokens": len(input_tokens) + len(output_tokens)
        }
    }

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    subreddit_name = data.get('subreddit')
    query = data.get('query')
    prompt = data.get('prompt')

    if not subreddit_name or not query or not prompt:
        return jsonify({"error": "subreddit, query, and prompt are required"}), 400

    result = search_posts(subreddit_name, query, prompt)
    return jsonify(result)

def schedule_search(subreddit_name, query, prompt, day, time):
    def job():
        result = search_posts(subreddit_name, query, prompt)
        print(f"Scheduled Search Result: {result['response_text']}")
        print(f"Token Usage: {result['token_usage']}")

    schedule.every().day.at(time).do(job)

    if __name__ == "__main__":
        print(f"Agent started. Running the search every {day} at {time}.")
        job()
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)