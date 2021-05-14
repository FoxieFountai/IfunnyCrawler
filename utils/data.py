import requests

def RetrieveHtml(url = None):
    if url == None:
        return

    try:
        page = requests.get(url)
        return page.text
    except:
        return

if __name__ == "__main__":
    print(RetrieveHtml('https://www.google.com'))