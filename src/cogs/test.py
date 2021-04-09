import discord
from discord.ext import commands

from env import EnvironmentVariables
from utils import checks


class Test(commands.Cog, name="Pods"):

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot: discord.ext.commands.Bot = bot
        self.channel = bot.fetch_channel(EnvironmentVariables.DEBUG_CHANNEL)

    @commands.command(name='test_all')
    @checks.requires_staff_role()
    def test_all(self, ctx: commands.Context):
        self.test_pods()
        self.test_checkin()
        self.test_reactions()
        self.test_listeners()

    @commands.command(name='test_pods')
    @checks.requires_staff_role()
    def test_pods(self, ctx: commands.Context):


    @commands.command(name='test_checkin')
    @checks.requires_staff_role()
    def test_checkin(self, ctx: commands.Context):
        pass

    @commands.command(name='test_reactions')
    @checks.requires_staff_role()
    def test_reactions(self, ctx: commands.Context):
        pass

    @commands.command(name='test_listeners')
    @checks.requires_staff_role()
    def test_listeners(self, ctx: commands.Context):
        pass


def setup(bot):
    bot.add_cog(Test(bot))
