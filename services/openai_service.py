import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Category-specific prompts for better captions
CATEGORY_PROMPTS = {
    "tops": "Analyze this clothing item and provide a detailed description focusing on the top/shirt. Describe the style, color, fabric texture, neckline, sleeves, and any unique features or patterns. Be specific about the garment type (e.g., blouse, t-shirt, sweater, tank top).",
    "longtops": "Analyze this clothing item and provide a detailed description focusing on the long top/dress. Describe the style, color, fabric texture, length, sleeves, neckline, and any unique features or patterns. Be specific about the garment type (e.g., maxi dress, tunic, long cardigan).",
    "bottoms": "Analyze this clothing item and provide a detailed description focusing on the bottom/pants. Describe the style, color, fabric texture, fit, length, and any unique features or patterns. Be specific about the garment type (e.g., jeans, skirt, shorts, trousers).",
    "one-pieces": "Analyze this clothing item and provide a detailed description focusing on the one-piece garment. Describe the style, color, fabric texture, fit, and any unique features or patterns. Be specific about the garment type (e.g., jumpsuit, romper, overall dress).",
    "shoes": "Analyze this footwear and provide a detailed description. Describe the style, color, material, heel height (if applicable), and any unique features or patterns. Be specific about the shoe type (e.g., sneakers, boots, sandals, heels).",
    "accessories": "Analyze this accessory and provide a detailed description. Describe the style, color, material, and any unique features or patterns. Be specific about the accessory type (e.g., bag, hat, jewelry, belt, scarf)."
}

async def generate_image_caption(image_url: str, category: str) -> str:
    """
    Generate a caption for an image using OpenAI's GPT-4 Vision API
    
    Args:
        image_url: The URL of the image to analyze
        category: The category of the item (tops, bottoms, shoes, etc.)
    
    Returns:
        Generated caption as a string
    """
    try:
        # Get category-specific prompt
        prompt = CATEGORY_PROMPTS.get(category, CATEGORY_PROMPTS["tops"])
        
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates captions for clothing items."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300,
            temperature=0.7
        )
        print(response)
        caption = response.choices[0].message.content
        return caption.strip()
        
    except Exception as error:
        print(f"Error in generate_image_caption: {error}")
        return f"Error generating caption for {category} item"

async def generate_simple_caption(image_url: str) -> str:
    """
    Generate a simple caption for an image without category context
    
    Args:
        image_url: The URL of the image to analyze
    
    Returns:
        Generated caption as a string
    """
    try:
        response = await client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this clothing item and provide a brief, descriptive caption focusing on the style, color, and type of garment."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        caption = response.choices[0].message.content
        return caption.strip()
        
    except Exception as error:
        print(f"Error in generate_simple_caption: {error}")
        return "Error generating caption for clothing item" 