import requests

fetch_url = "http://wyre.pythonanywhere.com/load_readings/"

try:
    response = requests.get(fetch_url)
    # print(response.json())

except:
    print("Error: Site might be down")