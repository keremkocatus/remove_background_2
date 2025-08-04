def get_outfit_review_prompt(image_url: str, roast_level: int) -> list:
    """
    Returns OpenAI chat messages for outfit review, customized by roast_level (1 to 5).
    """
    if roast_level == 1:
        tone_instruction = (
            "You're a friendly fashion coach. Be extremely gentle and encouraging. "
            "Avoid criticism. Focus on what's working and give only the softest suggestions."
        )
    elif roast_level == 2:
        tone_instruction = (
            "You're a kind fashion stylist. Be mostly positive, mention a few areas to improve, "
            "but keep the tone supportive and polite."
        )
    elif roast_level == 3:
        tone_instruction = (
            "You're a balanced fashion expert. Give fair, objective feedback. "
            "Mention strengths and weaknesses equally. Be honest but respectful."
        )
    elif roast_level == 4:
        tone_instruction = (
            "You're a bold fashion critic. Lean into sharp feedback and don't sugarcoat. "
            "Still be fair and don't roast too hard — just keep it real."
        )
    elif roast_level == 5:
        tone_instruction = (
            "You're a savage fashion roaster. Be brutally honest, sarcastic, and funny. "
            "Point out flaws dramatically. Your job is to roast this outfit mercilessly — but still include structured ratings."
        )
    else:
        tone_instruction = (
            "You're a balanced fashion expert. Use a professional tone and return a structured review."
        )

    return [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        f"{tone_instruction}\n\n"
                        "Look at the outfit in the image and return a JSON object containing:\n"
                        "- 'review': a short paragraph giving overall impression of the outfit\n"
                        "- 'style_rating': score out of 5\n"
                        "- 'color_match_rating': score out of 5\n"
                        "- 'piece_match_rating': score out of 5\n"
                        "- 'overall_rating': score out of 5 (not average — your own holistic judgment)\n\n"
                        "Output ONLY via tool call with the exact structure."
                    )
                },
                {
                    "type": "image_url",
                    "image_url": {"url": image_url, "detail": "high"}
                }
            ]
        }
    ]

def get_outfit_review_tool_schema() -> list:
    """
    Returns the OpenAI tool schema for outfit review response structure.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "return_outfit_review",
                "description": "Returns structured review and scores for an outfit",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "review": {"type": "string"},
                        "style_rating": {"type": "number"},
                        "color_match_rating": {"type": "number"},
                        "piece_match_rating": {"type": "number"},
                        "overall_rating": {"type": "number"}
                    },
                    "required": [
                        "review",
                        "style_rating",
                        "color_match_rating",
                        "piece_match_rating",
                        "overall_rating"
                    ]
                }
            }
        }
    ]
