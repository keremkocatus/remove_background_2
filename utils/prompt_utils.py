def get_enhance_prompt(category: str) -> str:
    if category == "tops":
        return (
            "Extract only the **upper-body garment** (e.g., t-shirt, shirt, blouse) exactly as it appears in the original image. "
            "Preserve its **actual length** without extending it into a dress or shortening it. "
            "Keep all garment features such as **sleeve length, neckline, fabric texture, and patterns** unchanged. "
            "Do not stylize or enhance the item. Remove all background elements and human body parts, and isolate the top on a plain white or transparent background. "
            "Ensure the garment remains centered and in its original pose and scale."
        )

    elif category == "longtops":
        return (
            "Isolate the **long upper garment or dress** while maintaining its **full original length and silhouette**—do not crop, fold, or resize it. "
            "Preserve flow, decorative elements (like buttons, lace, patterns), and fabric structure exactly as in the input. "
            "Do not convert into a short top or modify its proportions. Remove the background and all body parts, centering the garment on a clean background. "
            "Keep the item in the same perspective and natural layout as shown."
        )

    elif category == "bottoms":
        return (
            "Extract only the **bottom clothing piece**—such as pants, shorts, or skirts—**exactly as it appears in the image**. "
            "Preserve the **original length** of the item: **do not mistakenly elongate shorts into pants or crop long pants into shorts**. "
            "Maintain details like folds, pockets, waistline, and texture. "
            "Remove all human body parts and background, presenting the item in a clean flat-lay view while keeping its exact proportions and pose."
        )

    elif category == "one-pieces":
        return (
            "Extract the one-piece outfit—such as a romper or jumpsuit—**without changing its type or structure**. "
            "Preserve the full length as visible in the original image (short if short, long if long), and keep all embellishments, colors, and textures intact. "
            "Avoid transforming it into separate top/bottom pieces. "
            "Remove all human features and background, ensuring the item remains in the original pose and layout."
        )

    elif category == "shoes":
        return (
            "Isolate the **pair of shoes** in their **original pose and view**—either flat-lay or side view—without altering the shape or exaggerating the size. "
            "Keep all visual details like **sole, texture, stitching, logos**, and material exactly as-is. "
            "Do not apply enhancements or style changes. Remove all background and body parts (legs, feet, etc.), and center the shoes clearly against a white or transparent background."
        )

    elif category == "accessories":
        return (
            "Extract the **accessory item**—such as bags, belts, hats, glasses, scarves, or jewelry—**exactly as it appears in the image**. "
            "Do not resize or distort its shape. Retain all original materials, logos, and textures. "
            "Make sure not to misinterpret small accessories like belts or earrings as larger items. "
            "Remove all body parts (e.g., hands, shoulders) and the background, and center the accessory on a clean flat surface."
        )

    else:
        return (
            "Extract the fashion item from the image **without making any assumptions about its type or altering its proportions**. "
            "Keep all features like size, length, material, and decorative elements identical to the original. "
            "Do not apply any transformation, style change, or enhancement. "
            "Remove all human body parts and the background, and keep the item centered in the same orientation and dimensions."
        )
