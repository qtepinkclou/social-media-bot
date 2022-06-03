import os
from .abc_media import ABCMediaHandler


tmp_media_path = 'Tmp/Media'


class SendMediaHandler(ABCMediaHandler):

    def __init__(self):
        super().__init__()
        self.tmp_media_folder = self.file_handler.dir_create(tmp_media_path)

    async def send_media(self, app_object, *url, **kwargs):
        save_path = self.file_handler.get_path(self.tmp_media_folder)
        self._process_media(
            save_path,
            *url
        )
        for media_name in os.listdir(self.tmp_media_folder):
            await app_object.send_to_user(
                content=self.tmp_media_folder + '/' + media_name,
                content_type='media',
                **kwargs
            )
        self.file_handler.delete_files_in_path(
            self.tmp_media_folder
        )
