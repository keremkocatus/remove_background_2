mask_prompt = {
    "top": "clothes",
    "longtop": "dress",
    "bottom": "pants",
    "one-piece": "clothes",
    "shoes": "shoes",
    "accessories": "accessories"
}

def get_mask_prompts(category: str, is_long_top: bool):
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