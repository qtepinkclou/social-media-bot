from src.commons.config import Config

from src.app.discord_handler.client.banana_dread import BananaDread

from src.app.discord_handler.client_features.comms_handler import CommsHandler
from src.app.discord_handler.client_features.cmd_err_handler import CmdErrHandler
from src.app.discord_handler.client_features.landmark_feature_handler import LandmarkFeatureHandler
from src.app.discord_handler.client_features.media_feature_handler import MediaFeatureHandler


cfg = Config()

TOKEN = cfg.get_param('DISCORD_TOKEN')


def go_bananas():
    bot = BananaDread(
        command_prefix='!',
    )

    bot.add_cog(CommsHandler(bot))
    bot.add_cog(CmdErrHandler(bot))
    bot.add_cog(LandmarkFeatureHandler(bot))
    bot.add_cog(MediaFeatureHandler(bot))

    bot.run(TOKEN)


go_bananas()
