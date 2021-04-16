import discord
from discord.ext import commands

from cogs.checkin import CheckinCommands
from cogs.pods import Pods
from env import EnvironmentVariables
from finders.mentorfinder import MentorFinder
from services.poddbservice import PodDBService
from utils import checks
from utils.confirmation import confirm


class Test(commands.Cog, name="Test"):

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot: discord.ext.commands.Bot = bot

    @commands.command(name='test_all')
    @checks.requires_staff_role()
    async def test_all(self, ctx: commands.Context):
        await self.test_pods()
        await self.test_checkin()
        await self.test_reactions()
        await self.test_listeners()

    @commands.command(name='test_pods')
    @checks.requires_staff_role()
    async def test_pods(self, ctx: commands.Context):
        """Tests all pod commands, requires at least 5 mentors in the given ENV variable role"""
        guild: discord.Guild = ctx.guild
        role: discord.Role = guild.get_role(EnvironmentVariables.MENTOR_ROLE)
        current_channel: discord.TextChannel = ctx.channel
        test_member: discord.Member = guild.get_member(111572782336208896)  # test member is Jacob Cuomo

        if len(role.members) < 5:
            await current_channel.send(f"There are not enough mentors to test pod commands. There needs to be at "
                                       f"least 5. Add more and try again.")
            return

        if not await confirm(
                confirmation="You are about to test all pod commands, are you sure you want to do this? It executes "
                             "over 20 commands, including removing all pods and takes some time to complete."
,
                ctx=ctx,
                bot=self.bot,
                abort_msg="You have decided to stop the command.",
                success_msg="Running the test_pods command now...",
                delete_msgs=False
        ):
            return

        pod_instance = Pods

        await Pods.remove_all_pods(pod_instance, ctx)

        # Create two separate pods with the singular create_pod command
        await Pods.create_pod(pod_instance, ctx, "DEBUG", MentorFinder.find_a_suitable_mentor(role))
        await Pods.create_pod(pod_instance, ctx, "DEBUG-2", MentorFinder.find_a_suitable_mentor(role))

        # Create three separate pods with the plural create_pods command
        await Pods.create_pods(pod_instance, ctx, 3)

        # Assign all created pods up and to this point
        await Pods.assign_pods(pod_instance, ctx)

        # List teams in a given pod, this command can find teams from current channel, a name, or user
        await Pods.teams(pod_instance, ctx, "DEBUG")
        await Pods.teams(pod_instance, ctx, "DEBUG-2")
        await Pods.teams(pod_instance, ctx, test_member.mention)
        if "pod" in current_channel.name:
            await Pods.teams(pod_instance, ctx)

        # Lists all pods in current channel
        await Pods.pods(pod_instance, ctx)

        # Adds a mentor to a given pod name
        await Pods.add_mentor(pod_instance, ctx, test_member, "DEBUG")
        await Pods.add_mentor(pod_instance, ctx, test_member, "DEBUG-2")

        # Merges two pods together, including any teams within them
        await Pods.merge_pods(pod_instance, ctx, "DEBUG-2", "DEBUG")

        # Finds a pod and returns their alembic ID
        await Pods.test(pod_instance, ctx, "DEBUG")

        # Send a message to a pod or all pods
        await Pods.send_message(pod_instance, ctx, "DEBUG", "THIS IS JUST A DRILL, DO NOT PANIC!")
        await Pods.send_message_all(pod_instance, ctx, "THIS IS JUST A DRILL, DO NOT PANIC!")

        # Lists all teams ever created
        await Pods.get_all_teams(pod_instance, ctx)

        # Remove Pod and Remove All Pods
        await Pods.remove_pod(pod_instance, ctx, "DEBUG")
        await Pods.remove_all_pods(pod_instance, ctx)

    @commands.command(name='test_checkin')
    @checks.requires_staff_role()
    async def test_checkin(self, ctx: commands.Context):
        guild: discord.Guild = ctx.guild
        role: discord.Role = guild.get_role(EnvironmentVariables.MENTOR_ROLE)
        current_channel: discord.TextChannel = ctx.channel

        pod_instance = Pods

        await Pods.create_pod(pod_instance, ctx, "DEBUG", MentorFinder.find_a_suitable_mentor(role))
        await Pods.create_pod(pod_instance, ctx, "DEBUG-2", MentorFinder.find_a_suitable_mentor(role))

        check_in_instance = CheckinCommands

        await CheckinCommands.checkin(check_in_instance, ctx, "DEBUG")
        await CheckinCommands.checkin(check_in_instance, ctx, "DEBUG-2")

        await CheckinCommands.checkin_all(check_in_instance, ctx)

        await Pods.remove_pod(pod_instance, ctx, "DEBUG")
        await Pods.remove_pod(pod_instance, ctx, "DEBUG-2")

    @commands.command(name='test_reactions')
    @checks.requires_staff_role()
    async def test_reactions(self, ctx: commands.Context):
        pass

    @commands.command(name='test_listeners')
    @checks.requires_staff_role()
    async def test_listeners(self, ctx: commands.Context):
        pass


def setup(bot):
    bot.add_cog(Test(bot))
