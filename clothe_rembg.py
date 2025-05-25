import replicate

client = replicate.Client()

with open("./images/müc_istek.jpg", "rb") as img_file:
    output = replicate.run(
        "schananas/grounded_sam:ee871c19efb1941f55f66a3d7d960428c8a5afcb77449547fe8e5a3ab9ebc21c",
        input={
            "image": img_file,
            "mask_prompt": "clothes",
            "adjustment_factor": -15,
            "negative_mask_prompt": "shoes"
        }
    )

# The schananas/grounded_sam model can stream output as it's running.
# The predict method returns an iterator, and you can iterate over that output.
for item in output:
    # https://replicate.com/schananas/grounded_sam/api#output-schema
    print(item)