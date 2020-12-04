from discord.ext import commands, tasks

from services.gqlservice import GQLService
from utils.subscriptions import subscribe


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

    @subscribe(GQLService.team_created_listener)
    async def on_project_created(self, project):
        pass

    @subscribe(GQLService.member_added_listener)
    async def on_project_member_added(self, member_with_project):
        pass

    @subscribe(GQLService.member_removed_listener)
    async def on_project_member_removed(self, member_with_project):
        pass

    @subscribe(GQLService.team_edited_listener)
    async def on_project_edited(self, project):
        pass


def setup(bot):
    bot.add_cog(ListenCog(bot))
