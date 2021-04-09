import discord
from discord.ext import commands

from cogs.pods import Pods
from env import EnvironmentVariables
from finders.mentorfinder import MentorFinder
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
    async def test_pods(self, ctx: commands.Context):
        """Tests all pod commands, requires at least 5 mentors in the given ENV variable role"""
        guild: discord.Guild = ctx.guild
        role: discord.Role = guild.get_role(EnvironmentVariables.MENTOR_ROLE)
        current_channel: discord.TextChannel = ctx.channel
        test_member: discord.Member = guild.get_member(111572782336208896)  # test member is Jacob Cuomo

        # Create two separate pods with the singular create_pod command
        await Pods.create_pod(ctx, "DEBUG", MentorFinder.find_a_suitable_mentor(role))
        await Pods.create_pod(ctx, "DEBUG-2", MentorFinder.find_a_suitable_mentor(role))

        # Create three separate pods with the plural create_pods command
        await Pods.create_pods(ctx, 3)

        # Assign all created pods up and to this point
        await Pods.assign_pods(ctx)

        # List teams in a given pod, this command can find teams from current channel, a name, or user
        await Pods.teams(ctx, "DEBUG")
        await Pods.teams(ctx, "DEBUG-2")
        await Pods.teams(ctx, test_member)
        if "pod" in current_channel.name:
            await Pods.teams(ctx)

        # Lists all pods in current channel
        await Pods.pods(ctx)

        # Adds a mentor to a given pod name
        await Pods.add_mentor(ctx, test_member, "DEBUG")
        await Pods.add_mentor(ctx, test_member, "DEBUG-2")

        # Merges two pods together, including any teams within them
        await Pods.merge_pods("DEBUG-2", "DEBUG")

        # Finds a pod and returns their alembic ID
        await Pods.test(ctx, "DEBUG")

        # Send a message to a pod or all pods
        await Pods.send_message("DEBUG", "THIS IS JUST A DRILL, DO NOT PANIC!")
        await Pods.send_message_all("THIS IS JUST A DRILL, DO NOT PANIC!")

        # Lists all teams ever created
        await Pods.get_all_teams

        # Remove Pod and Remove All Pods
        await Pods.remove_pod("DEBUG")
        await Pods.remove_all_pods(ctx)

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
