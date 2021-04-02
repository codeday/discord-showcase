from discord.ext import commands

from cogs.pods import Pods
from helpers.helper import Helper
from services.podgqlservice import PodGQLService
from utils.subscriptions import subscribe

"""
    The purpose of this class is to listen for any changes by "subscribing" to GQL events. When an event is triggered,
    the code in each function is also executed.
"""


class ListenCog(commands.Cog, name="Listen"):
    """Listen to showcase api for team updates"""

    def __init__(self, bot):
        self.bot = bot
        self.on_project_created.start(self)
        self.on_project_member_added.start(self)
        self.on_project_member_removed.start(self)
        self.on_project_edited.start(self)

    def cog_unload(self):
        self.on_project_created.stop()
        self.on_project_member_added.stop()
        self.on_project_member_removed.stop()
        self.on_project_edited.stop()

    @subscribe(PodGQLService.team_created_listener)
    async def on_project_created(self, project):
        await Helper.assign_pods_helper(self.bot)

    @subscribe(PodGQLService.member_added_listener)
    async def on_project_member_added(self, member_with_project):
        await Pods.add_or_remove_user_to_pod_tc(self.bot, member_with_project, False)

    @subscribe(PodGQLService.member_removed_listener)
    async def on_project_member_removed(self, member_with_project):
        await Pods.add_or_remove_user_to_pod_tc(self.bot, member_with_project, True)

    @subscribe(PodGQLService.team_edited_listener)
    async def on_project_edited(self, project):
        pass


def setup(bot):
    bot.add_cog(ListenCog(bot))
