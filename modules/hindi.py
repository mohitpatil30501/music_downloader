import zipfile, os, requests

from bs4 import BeautifulSoup


class Hindi:
    def __init__(self):
        self.month = int(input("Enter Month: "))
        self.year = int(input("Enter Year: "))
        self.album_list = []
        self.path_to_zip = self.path_to_extract = None

    def fetch_album_list(self):
        try:
            request = requests.get("https://jatt.net")
            baseurl = request.url
        except:
            print("Error to Connect Site....Try again...!")
            exit(0)

        try:
            request_url = str(baseurl) + "/month.php?c=Hindi&m=" + str(self.month) + "&y=" + str(self.year)
            request = requests.get(request_url)
        except:
            print("Error to Get Data...Try again...!")
            exit(0)

        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        for single_element in soup.find_all("a", {"class": "touch"}):
            removes = single_element.find("font", {"color": "#339900"})
            self.album_list.append({
                "Name": (single_element.text.strip().replace("»", "").replace(removes.text.strip(), "")).strip(),
                "Link": baseurl+single_element["href"]
            })

    def download_zip(self):
        pass

    def unzip_zipfile(self):
        with zipfile.ZipFile(self.path_to_zip, 'r') as zip_element:
            zip_element.extractall(self.path_to_extract)
