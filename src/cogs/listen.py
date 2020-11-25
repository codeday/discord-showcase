from discord.ext import commands



class ListenCog(commands.Cog, name="Listen"):
    """Listen to showcase api for team updates"""

    def __init__(self, bot):
        self.bot = bot

    def on_team_created(self):
        """Checks if available pod, if so assigns pod, if not adds to overflow pod"""
        pass

    def on_team_join(self):
        """Adds a newly joined student to their teams pod"""
        pass

    def on_team_leave(self):
        """Removes a left student from their teams pod"""
        pass

    def on_submit_project(self):
        """Congratulates and confirms the submission of a teams project"""
        pass


def setup(bot):
    bot.add_cog(ListenCog(bot))