import os

from collections import defaultdict

from .abc_media import ABCMediaHandler


perm_media_path = 'Perm/Media'


def no_media_msg(cmd):
    return f'There is no media linked with the command [{cmd}]'


def save_media_msg(cmd):
    return f'Saved the following media and linked them with command [{cmd}]'


def deleted_media_msg(cmd):
    return f'Deleted aforementioned media linked with command [{cmd}]:'


def show_media_names_msg(cmd):
    return f'The command [{cmd}] has the following media linked with it:'


class SaveMediaHandler(ABCMediaHandler):

    def __init__(self):
        super().__init__()
        self.file_handler.remove_directory(perm_media_path)
        self.command_folders = defaultdict(str)

    async def save_media(self, cmd, app_object, *url, **kwargs):
        self.command_folders[cmd] = self.file_handler.dir_create(
            self.file_handler.get_path(
                perm_media_path,
                cmd
            )
        )
        self._process_media(
            self.command_folders[cmd],
            *url
        )
        await app_object.send_to_user(
            content=save_media_msg(cmd),
            content_type='text',
            **kwargs
        )
        await self.show_media_names(cmd, app_object, **kwargs)

    async def show_media_names(self, cmd, app_object, **kwargs):
        if os.path.isdir(self.command_folders[cmd]):
            await app_object.send_to_user(
                content=show_media_names_msg(cmd),
                content_type='text',
                **kwargs
            )
            for media_name in os.listdir(self.command_folders[cmd]):
                await app_object.send_to_user(
                    content=media_name,
                    content_type='text',
                    **kwargs
                )
        else:
            await app_object.send_to_user(
                content=no_media_msg(cmd),
                content_type='text',
                **kwargs
            )

    async def show_media(self, cmd, app_object, **kwargs):
        if os.path.isdir(self.command_folders[cmd]):
            for media_name in os.listdir(self.command_folders[cmd]):
                await app_object.send_to_user(
                    content= perm_media_path + '/' + cmd + '/' + media_name,
                    content_type='media',
                    **kwargs
                )
        else:
            await app_object.send_to_user(
                content=no_media_msg(cmd),
                content_type='text',
                **kwargs
            )

    async def delete_media(self, cmd, app_object, **kwargs):
        if os.path.isdir(self.command_folders[cmd]):
            await self.show_media_names(
                cmd,
                app_object,
                **kwargs
            )
            self.file_handler.remove_directory(
                self.command_folders[cmd]
            )
            await app_object.send_to_user(
                content=deleted_media_msg(cmd),
                content_type='text',
                **kwargs
            )
            del self.command_folder[cmd]
        else:
            await app_object.send_to_user(
                content=no_media_msg(cmd),
                content_type='text',
                **kwargs
            )
