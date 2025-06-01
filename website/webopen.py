import webbrowser
from databse import website

def openweb(webname):
    website_name = webname.lower().split()
    counts = {}

    for name in website_name:
        counts[name] = counts.get(name, 0) + 1

    urls_to_open = []

    for name, count in counts.items():
        if name in website:
            urls_to_open.extend([website[name]] * count)

    for url in urls_to_open:
        webbrowser.open(url)

    if urls_to_open:
        print("Opening...")
    else:
        print("No matching websites found.")

# Example usage
# openweb("instagram")
