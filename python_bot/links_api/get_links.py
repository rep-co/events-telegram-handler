
def get_links():
    links = []
    file = open("channels", "r")
    for line in file:
        links.append(line)
    return links
