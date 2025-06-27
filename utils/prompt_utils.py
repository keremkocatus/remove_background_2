mask_prompt = {
    "tops": "clothes",
    "longtops": "dress",
    "bottoms": "pants",
    "one-pieces": "clothes",
    "shoes": "shoes",
    "accessories": "accessories"
}

def get_mask_prompts(category: str, is_long_top: bool = False):
    try:
        negative_mask_prompt = ""
        
        if category == "top" and is_long_top:
            positive_mask_prompt = mask_prompt["longtop"]
        else:
            positive_mask_prompt = mask_prompt[category]
            
        return positive_mask_prompt, negative_mask_prompt
    except Exception as e:
        print(f"Error in get_mask_prompts: {e}")
        return None, None