from discord.ext import commands, tasks

from services.gqlservice import GQLService


class ListenCog(commands.Cog, name="Listen"):
    """Listen to showcase api for team updates"""

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=60.0)
    def on_team_created(self):
        """Checks if available pod, if so assigns pod, if not adds to overflow pod"""
        GQLService.team_created_listener()

    @tasks.loop(seconds=5.0)
    def on_team_join(self):
        """Adds a newly joined student to their teams pod"""
        GQLService.member_added_listener()

    @tasks.loop(seconds=5.0)
    def on_team_leave(self):
        """Removes a left student from their teams pod"""
        GQLService.member_removed_listener()

    @tasks.loop(seconds=60.0)
    def on_submit_project(self):
        """Congratulates and confirms the submission of a teams project"""
        GQLService.team_submitted_listener()


def setup(bot):
    bot.add_cog(ListenCog(bot))