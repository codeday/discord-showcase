from random import choice

import discord
from discord.ext import commands

from converters.PodConverter import PodConverter
from services.poddbservice import PodDBService
from utils import checks

"""
    The purpose of this class is to allow administrators the ability to run commands to checkin to all or specific pods.
"""


def generate_message(team_name):
    title_options = [
        f"How's life {team_name}?",
        "Hello, living organism! How do you do this fine day?",
        "Howdy do!?!",
    ]
    message_options = [
        f"Good? I hope so! Please, go to the link down there and tell me so we can keep tabs on how you're doing. Thanks!",
        f"Hope you're programming is going swell! I have orders to have you fill out the form down there so my fellow staff can keep up to date. Thanks!",
        f"I'm feeling pretty [john:emotion]! Please, tell me how you are feeling about your project down there. Bye for now!",
    ]
    return choice(title_options) + " " + choice(message_options)


class CheckinCommands(commands.Cog, name="Checkin"):
    """Contains pod checkin commands"""

    def __init__(self, bot):
        self.bot: discord.ext.commands.Bot = bot

    @commands.command(name='checkin')
    @checks.requires_staff_role()
    async def checkin(self, ctx: commands.Context, pod_name):
        """Checks in on a specific pod"""
        guild: discord.Guild = ctx.guild
        pod = await PodConverter.get_pod_by_name(pod_name=pod_name, current_channel=ctx.channel)
        if pod is None:
            return

        channel: discord.TextChannel = guild.get_channel(int(pod.tc_id))
        message = await channel.send("Hello @everyone, can you quickly react to this message to let us know how "
                                     "you're feeling about your project right now:")
        await message.add_reaction("😀")
        await message.add_reaction("😐")
        await message.add_reaction("☹")

    @commands.command(name='checkin_all')
    @checks.requires_staff_role()
    async def checkin_all(self, ctx: commands.Context):
        """checks in on all teams"""
        guild: discord.Guild = ctx.guild
        pods = await PodConverter.get_all_pods(current_channel=ctx.channel,
                                               output_msg="There are no pods to check into with.")
        if pods is None or len(pods) == 0:
            return
        for pod in pods:
            channel: discord.DMChannel = guild.get_channel(int(pod.tc_id))
            message = await channel.send("Hello @everyone, can you quickly react to this message to let us know how "
                                         "you're feeling about your project right now:")
            await message.add_reaction("😀")
            await message.add_reaction("😐")
            await message.add_reaction("☹")


def setup(bot):
    bot.add_cog(CheckinCommands(bot))
