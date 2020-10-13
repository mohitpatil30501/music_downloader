import zipfile, os, requests

from bs4 import BeautifulSoup


class Hindi:
    def __init__(self):
        self.year = int(input("Enter Year: "))
        self.album_list = []

    def fetch_album_list(self):
        try:
            request = requests.get("https://pagalsong.in")
            baseurl = request.url
            if request is None:
                print("No Data found....Try again...!")
                exit(0)
        except:
            print("Error to Connect Site....Try again...!")
            exit(0)

        try:
            request_url = str(baseurl) + "/bollywood-mp3-songs-" + str(self.year) + "-subcategory.html"
            request = requests.get(request_url)
            if request is None:
                print("No Data found....Try again...!")
                exit(0)
        except:
            print("Error to Extract Data...Try again...!")
            exit(0)

        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        for element in soup.find_all("div", {"class": "tnned alt-bg-gray"}):
            headling_tag = element.find("h3")
            album = headling_tag.find("a")
            list_song = Hindi.find_song(album["href"])
            if list_song is None:
                print("Not Downloadable file Founded...!")
                continue

            self.album_list.append({
                "Album_name": album.text.strip(),
                "Link": album["href"],
                "Songs": list_song
            })
        self.download()

    @staticmethod
    def find_song(link):
        try:
            request = requests.get(link)
            if request is None:
                print("No Data found....Try again...!")
                exit(0)
        except:
            print("Error to Connect Site....Try again...!")
            exit(0)

        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        list_song = []
        for song in soup.find_all("div", {"class": "cat-list"}):
            song = song.find("a")
            data = {
                "Song_name": song.text.strip(),
                "Link": Hindi.find_song_link(song["href"])
            }
            list_song.append(data)
        return list_song

    @staticmethod
    def find_song_link(link):
        try:
            request = requests.get(link)
            if request is None:
                print("No Data found....Try again...!")
                exit(0)
        except:
            print("Error to Connect Site....Try again...!")
            exit(0)

        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        song_link = []
        for song in soup.find_all("div", {"class": "downloaddiv"}):
            song = song.find("a", {"class": "dbutton"})

            if song is not None:
                span_no = 0
                for data in song.find_all("span"):
                    span_no += 1
                    if span_no == 2:
                        song_link.append({
                            "name": data.text.strip(),
                            "value": int(data.text.strip().replace("Download", "").replace("KBPS mp3", "").strip()),
                            "link": song["href"]
                        })
        value = 0
        for single in song_link:
            if value < single["value"]:
                value = single["value"]
        for single in song_link:
            if value == single["value"]:
                return single["link"]

    def download(self):
        print("Downloading...")
        if not os.path.isdir('Songs'):
            os.mkdir('Songs')
        os.chdir('Songs')

        for album in self.album_list:
            os.mkdir(album["Album_name"])
            print(album["Album_name"], " Album stared downloading...")
            song_list = album['Songs']
            for song in song_list:
                status = True
                print(song["Song_name"], "stared downloading...")
                n = 0
                while status and n <= 3:
                    try:
                        song_link = song['Link']
                        request = requests.get(song_link)
                        break
                    except:
                        if n < 3:
                            n += 1
                            print("Trying Again...(", n, ")")
                        else:
                            print('Error to download File of "', album['Album_name'], '"\nTry Again..!')
                            status = False
                if status:
                    filename = os.path.join(os.getcwd(), album["Album_name"], song["Song_name"])
                    with open(filename + ".mp3", "wb") as file:
                        file.write(request.content)
                    print("Download completed...")
