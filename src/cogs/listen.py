from discord.ext import commands, tasks

from services.gqlservice import GQLService
from utils.subscriptions import subscribe


class ListenCog(commands.Cog, name="Listen"):
    """Listen to showcase api for team updates"""

    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.on_team_created.stop()
        self.on_team_join.stop()
        self.on_team_leave.stop()
        self.on_team_edited.stop()

    @subscribe(GQLService.team_created_listener)
    async def on_team_created(self, project):
        print("Project created", project)

    @subscribe(GQLService.member_added_listener)
    async def on_team_join(self, member):
        print("Team member added", )

    @subscribe(GQLService.member_removed_listener)
    async def on_team_leave(self, member):
        print("Team member removed", member)

    @subscribe(GQLService.team_edited_listener)
    async def on_submit_project(self, project):
        print("Team edited", project)


def setup(bot):
    bot.add_cog(ListenCog(bot))
