from discord.ext import commands
from utils import checks


class CheckinCommands(commands.Cog, name="Checkin"):
    """Contains pod checkin commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='checkin')
    @checks.requires_staff_role()
    async def checkin(self, ctx, pod_name):
        """Checks in on a specific pod"""
        pass

    @commands.command(name='checkin_all')
    @checks.requires_staff_role()
    def checkin_all(self, ctx):
        """checks in on all teams"""
        pass


def setup(bot):
    bot.add_cog(CheckinCommands(bot))