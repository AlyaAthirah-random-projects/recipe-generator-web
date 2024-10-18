from openai import OpenAI
import psycopg2
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



def gpt_process_receipt(receipt_text):
    prompt = f"""Analyze the following receipt text and provide estimates for ingredient prices. After that, store the items in an array of JSON format below. Convert the date into %d/%m/%y format and the price into double precision format. Your output should only include the JSON. Think step-by-step:
    [
    	{{
        "name": "HAEPYO HOT PEPPER",
        "price": 13.50,
        "date": "22/05/24",
        "store_name": "Star Grocer Sdn. Bhd."
    	}},
    	{{
        "name": "HAEPYO HOT PEPPER",
        "price": 13.50,
        "date": "22/05/24",
        "store_name": "Star Grocer Sdn. Bhd."
    	}},

    ]

    \n\n{receipt_text}
    """
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',  # or the latest available model
        # model='gpt-4o-mini',  # or the latest available model
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    result = response.choices[0].message.content
    print (result)
    # Assume the response contains a JSON-like structure
    return result


def gpt_generate_recipe(ingredients, prompt):
    prompt = f"""Using the ingredients: {ingredients}, {prompt}:

        Check also the latest price(in MYR) of ingredients to make educated decision.
        {get_grocery_list()}
        """

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',  # or the latest available model
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    result = response.choices[0].message.content
    result = result.replace("\n", "<br>")
    return result

def get_grocery_list():
    cur = conn.cursor()
    cur.execute("SELECT * FROM items")
    groceries = cur.fetchall()
    cur.close()
    print (groceries)
    return groceries