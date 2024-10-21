from src import scan_receipt
from datetime import datetime
import json
import psycopg2
from openai import OpenAI
from dateutil import parser
import os
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAPI_KEY")
client = OpenAI(api_key=openai_key)

dbname=os.getenv("DB_NAME")
dbuser=os.getenv("DB_USERNAME")
dbpass=os.getenv("DB_PASS")
dbhost=os.getenv("DB_HOST")
conn = psycopg2.connect(f"dbname={dbname} user={dbuser} password={dbpass} host={dbhost}")


def process_receipt_image(filepath):
    text, image_arr = scan_receipt.scan_image(filepath)
    return text, image_arr

def gpt_process_receipt(receipt_text):
    prompt = f"""Analyze the following receipt text and provide estimates for ingredient prices. After that, store the items in an array of JSON format below. Your output should only include the JSON:
    [
    	{{
    	"name":,
    	"price":,
    	"date":,
    	"store_name":
    	}},
    	{{
    	"name":,
    	"price":,
    	"date":,
    	"store_name":
    	}},

    ]

    \n\n{receipt_text}
    """
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',  # or the latest available model
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    result = response.choices[0].message.content
    print (result)
    # Assume the response contains a JSON-like structure
    return result

def save_to_database(json_data):
    items = json.loads(json_data)
    cur = conn.cursor()
    for item in items:
        print(item)
        date_obj = datetime.strptime(item['date'], "%d/%m/%y").date()
        # date_obj = convert_date_to_iso(item['date'])
        cur.execute("INSERT INTO items (name, price, date, store_name) VALUES (%s, %s, %s, %s)",
                    (item['name'], item['price'], date_obj, item['store_name']))
    conn.commit()
    cur.close()


def convert_date_to_iso(date_string):
    try:
        # Parse the date string into a datetime object
        parsed_date = parser.parse(date_string)

        # Format the date to YYYY-MM-DD
        formatted_date = parsed_date.strftime("%d/%m/%y")

        return formatted_date
    except ValueError:
        return "Invalid date format"