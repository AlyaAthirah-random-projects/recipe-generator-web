import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANYTHINGLLM_KEY")

url = 'http://localhost:3001/api/v1/workspace/grocery/thread/8a91e107-2781-4202-a81d-b0f65314eb14/chat'
headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

def get_recipe(dish):
    prompt = f"""
        Follow the steps:
        
        Give me the recipe for {dish} along with the ingredients and the instructions.
        After that, pick a product for each ingredients listed for its price.
        Lastly calculate the total cost.
        Take a breath and think about it slowly.
        
        Example: Basic Pancake Recipe
        
        Ingredients: All-purpose flour – 1 cup (125g) Granulated sugar – 2 tablespoons (25g) Baking powder – 2 teaspoons (10g) Salt – 1/2 teaspoon (2.5g) Milk – 1 cup (240ml) Large egg – 1 Melted butter – 2 tablespoons (30ml) Vanilla extract (optional) – 1 teaspoon (5ml)
        
        Instructions: In a mixing bowl, whisk together the flour, sugar, baking powder, and salt. In another bowl, mix the milk, egg, melted butter, and vanilla extract (if using). Pour the wet ingredients into the dry ingredients and stir until just combined. (It’s okay if there are a few lumps; do not overmix.) Preheat a non-stick skillet or griddle over medium heat. Lightly grease with oil or butter. Pour about 1/4 cup of batter for each pancake onto the skillet. Cook until bubbles form on the surface and the edges look set, about 2-3 minutes. Flip the pancakes and cook for an additional 1-2 minutes, or until golden brown. Serve warm with your favorite toppings (e.g., syrup, fresh fruit, whipped cream).
        
        Found products: All-purpose flour (125g) - Cap Ros Tepung Gandum (Wheat Flour) 850g - RM 2.70 Granulated sugar (25g) - Gula Prai Coarse Grain Sugar 1kg - RM 2.85 Baking powder (10g) - Meriah Double Action Baking Powder 100g - RM 2.70 Salt (2.5g) - Fine Salt 1kg - RM 1.20 Milk (240ml) - Farm Fresh Cows Milk 1L - RM 8.40 Large egg (1 unit) - QL Omega Eggs with Omega 3 and DHA (Large) 15pcs/pack - RM 12 Melted butter (30ml) - Westgold Salted Butter 250g - RM 13.99 Vanilla extract (5ml) - Star Brand Artificial Vanilla Flavour 25ml - RM 2.95
        
        Price: Cap Ros Tepung Gandum (Wheat Flour) RM 2.70 / 850g * 125g = RM 0.40 Gula Prai Coarse Grain Sugar RM 2.85 / 1000g * 25g = RM 0.07 Meriah Double Action Baking Powder RM 2.70 / 100g * 10g = RM 0.27 Fine Salt RM 1.20 / 1000g * 2.5 = RM 0 Farm Fresh Cows Milk RM 8.40 / 1000ml * 240ml = RM 2.02 QL Omega Eggs with Omega 3 and DHA (Large) RM 12 / 15 * 1 = RM 0.80 Westgold Salted Butter RM 13.99 / 250g * 30ml = RM 1.68 Star Brand Artificial Vanilla Flavour RM 2.95 / 25ml * 5ml = RM0.59
        
        Total cost = 0.40+0.07+0.27+0+2.02+0.80+1.68+0.59 = 5.83
        """

    data = {
      "message": f"{prompt}",
      "mode": "chat",
      "userId": 42
    }
    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    if response.status_code == 200:
        # beautified_json = json.dumps(response.json(), indent=4)
        print (response.json()["textResponse"])
        return response.json()["textResponse"]
    else:
        return f"Request failed with status code: {response.status_code}"




