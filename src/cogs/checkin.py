from random import choice

from discord.ext import commands
from utils import checks

def generate_message(team_name):
    title_options = [
        f"How's life {team_name}?",
        "Hello, living organism! How do you do this fine [weather:city] day?",
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