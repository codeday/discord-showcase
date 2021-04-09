import discord
from discord.ext import commands


class Test(commands.Cog, name="Pods"):

    def __init__(self, bot):
        self.bot: discord.ext.commands.Bot = bot


def setup(bot):
    bot.add_cog(Test(bot))
