def get_enhance_prompt(category: str) -> str:
    if category == "tops":
        return (
            "Extract the top clothing item from the image and convert it into a flat-lay catalog image. "
            "Maintain the garment’s exact shape, fabric texture, sleeve length, neckline design, and any printed patterns. "
            "Do not alter or enhance the clothing in any way. "
            "Remove the entire background and all parts of the human body, ensuring the top is centered and isolated on a plain white or transparent background."
        )

    elif category == "longtops":
        return (
            "Isolate the long top or dress from the image and generate a flat-lay catalog version. "
            "Keep every aspect of the item intact—preserve its silhouette, flow, decorative elements (such as buttons, lace, or patterns), and original colors. "
            "Do not apply style transfer or enhancements. "
            "Remove all background elements and human body parts while keeping the dress in the exact same layout and position."
        )

    elif category == "bottoms":
        return (
            "Extract the bottom clothing item (such as pants, skirts, or shorts) from the image and present it in a clean, catalog-style flat-lay format. "
            "Precisely preserve the garment’s length, fabric folds, stitching, pocket placement, and hemline. "
            "Remove the background and any visible body parts. "
            "Keep the original composition and position of the item unchanged."
        )

    elif category == "one-pieces":
        return (
            "Extract the one-piece outfit exactly as shown in the original image, and generate a clean flat-lay catalog version. "
            "Do not modify or reinterpret any part of the design—preserve the exact material, color palette, fit, and embellishments. "
            "Ensure all background elements and human body parts are completely removed, keeping only the isolated garment in the same position."
        )

    elif category == "shoes":
        return (
            "Isolate the pair of shoes from the image and display them in a flat-lay or side-view product format, as originally photographed. "
            "Keep all physical details such as shape, stitching, sole design, textures, logos, and colors exactly the same. "
            "Remove the entire background and all body parts (feet, legs, etc.), ensuring the shoes are centered and clearly visible without alteration."
        )

    elif category == "accessories":
        return (
            "Extract the accessory item from the image—this includes bags, belts, hats, scarves, glasses, or jewelry—and display it cleanly and clearly in a catalog-ready format. "
            "Do not alter its dimensions, texture, branding, or color. Maintain the original position and layout. "
            "Remove all background elements and human body parts, including hands or shoulders if present."
        )

    else:
        return (
            "Extract the fashion item from the image and convert it into a clean, catalog-style flat-lay. "
            "Preserve all original visual characteristics including size, color, texture, and design details. "
            "Do not apply style changes or transformations. "
            "Remove all human features and background content, keeping the item in the same position and orientation as in the source image."
        )
