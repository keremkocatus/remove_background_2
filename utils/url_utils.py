
def clean_url(response_url: str):
    if response_url[-1] == "?":
        return response_url[:-1]
    else:
        return response_url