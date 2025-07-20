
def get_enhance_prompt(category: str) -> str:
    if category == "tops":
        return (
            "Extract the top clothing item from the image and convert it into a flat-lay catalog image. "
            "Do not change or alter the garment in any way—preserve its exact shape, fabric texture, sleeve length, neckline, and print details. "
            "Remove the background and all parts of the human body, ensuring that only the clothing is shown cleanly and clearly."
        )

    elif category == "longtops":
        return (
            "Isolate the long top or dress from the original image and generate a clean flat-lay version suitable for catalogs. "
            "Keep the garment completely intact without modifying its flow, cut, or decorative elements like buttons or patterns. "
            "Ensure that the result contains no background or human body parts—only the dress clearly visible."
        )

    elif category == "bottoms":
        return (
            "Extract the bottom clothing item such as pants or skirts exactly as seen, and present it as a flat-lay image. "
            "Retain all details including stitching, fabric texture, pockets, and length without any modifications. "
            "Remove everything else from the image including background and human body—only the clothing should remain."
        )

    elif category == "one-pieces":
        return (
            "Extract the one-piece outfit exactly as it appears, showing the full item in a clean, catalog-style layout. "
            "Do not modify or redesign any part of the outfit—preserve its original material, color, cut, and small details. "
            "Ensure there are no people, limbs, or background elements in the final output—only the isolated clothing item."
        )

    elif category == "shoes":
        return (
            "Isolate the pair of shoes from the image and display them exactly as they are in a clean product photo format. "
            "Do not change the shoe structure, colors, materials, or design elements like soles, stitching, or logos. "
            "Make sure the background and all human body parts (feet, legs, etc.) are completely removed, showing only the shoes."
        )

    elif category == "accessories":
        return (
            "Extract the accessory item—this may include bags, belts, hats, scarves, glasses, or jewelry—and display it clearly and cleanly. "
            "Do not make any alterations to the item's size, shape, texture, material, or branding details. "
            "Remove all background elements and human body parts—only the accessory should remain, centered and isolated."
        )

    else:
        return (
            "Extract the fashion item from the image and show it exactly as it is, in a clean catalog-ready flat-lay format. "
            "Preserve all original visual features like shape, texture, material, and design without modification. "
            "Ensure the image contains no background or human body parts—only the clothing or item clearly presented."
        )


