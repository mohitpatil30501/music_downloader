import zipfile, os, requests

from bs4 import BeautifulSoup


class Hindi:
    def __init__(self):
        self.month = int(input("Enter Month: "))
        self.year = int(input("Enter Year: "))
        self.album_list = []

    def fetch_album_list(self):
        try:
            request = requests.get("https://jatt.net")
            baseurl = request.url
            if request is None:
                print("No Data found....Try again...!")
                exit(0)
        except:
            print("Error to Connect Site....Try again...!")
            exit(0)

        try:
            request_url = str(baseurl) + "/month.php?c=Hindi&m=" + str(self.month) + "&y=" + str(self.year)
            request = requests.get(request_url)
            if request is None:
                print("No Data found....Try again...!")
                exit(0)
        except:
            print("Error to Extract Data...Try again...!")
            exit(0)

        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        for single_element in soup.find_all("a", {"class": "touch"}):
            removes = single_element.find("font", {"color": "#339900"})

            list_song = Hindi.find_song(baseurl + single_element["href"])
            if list_song is None:
                print("Not Downloadable file Founded...!")
                continue

            self.album_list.append({
                "Album_name": (single_element.text.strip().replace("»", "").replace(removes.text.strip(), "")).strip(),
                "Link": baseurl + single_element["href"],
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
        for song in soup.find_all("a", {"class": "touch"}):
            if song.text.strip() != "Play All":
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
        song_link = None
        for song in soup.find_all("a", {"class": "touch"}):
            removes = song.find("font", {"color": "#339900;"})

            if removes is not None:
                data = song.text.strip().replace(removes.text.strip(), "").strip()

                if data == "Download in 320 kbps":
                    song_link = song["href"]
                elif data == "Download in 128 kbps":
                    song_link = song["href"]
                elif data == "Download in 48 kbps":
                    song_link = song["href"]
        return song_link

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
