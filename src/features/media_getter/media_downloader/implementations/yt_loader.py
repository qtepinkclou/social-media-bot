from youtube_dl import YoutubeDL


yt_configuration = {
    'format': 'best',
    'noplaylist': True,
    'extract-audio': True,
    'quiet': True
}


class YTLoader:

    def __init__(self):
        self.yt_loader = YoutubeDL(yt_configuration)

    def download_media(self, save_path, url):
        self.yt_loader.params['outtmpl'] = save_path + '/' + '%(title)s.mp4'

        with self.yt_loader as ydl:
            ydl.download([url])
