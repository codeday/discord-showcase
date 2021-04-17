from typing import Union

import discord
from disputils import BotEmbedPaginator

from converters.PodConverter import PodConverter
from discord.ext import commands

from converters.TeamConverter import TeamConverter
from env import EnvironmentVariables
from finders.mentorfinder import MentorFinder
from finders.podnamefinder import PodNameFinder
from helpers.helper import Helper
from services.PodDispatcher import PodDispatcher
from services.poddbservice import PodDBService
from services.podgqlservice import PodGQLService
from utils import checks
from utils.generateembed import GenerateEmbed
from utils.setpermissions import SetPermissions

"""
    The purpose of this class is to execute commands and reach out to other classes for input sanitation and actions
"""


class Pods(commands.Cog, name="Pods"):

    def __init__(self, bot):
        self.bot: discord.ext.commands.Bot = bot

    @commands.command(name='create_pod')
    @checks.requires_staff_role()
    async def create_pod(self, ctx: commands.Context, pod_name: str, mentor: discord.Member):
        """Creates a POD for a team"""

        """Create a text channel"""
        guild: discord.Guild = ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.get_role(EnvironmentVariables.STAFF_ROLE): discord.PermissionOverwrite(
                **dict(discord.Permissions.text())),
            guild.me: discord.PermissionOverwrite(read_messages=True, read_message_history=True),
        }

        tc = await guild.create_text_channel("pod " + pod_name, overwrites=overwrites,
                                             category=guild.get_channel(
                                                 EnvironmentVariables.CATEGORY),
                                             reason=None)
        print(mentor)
        await tc.set_permissions(mentor, overwrite=discord.PermissionOverwrite(**dict(discord.Permissions.text())))

        await tc.send(
            "Hello <@" +
            str(mentor.id) +
            "> you have been selected to be the mentor for this pod! Teams will be "
            "added shortly.")

        PodDispatcher.create_pod(pod_name, tc.id, mentor.id)

    @commands.command(name='create_pods')
    @checks.requires_staff_role()
    async def create_pods(self, ctx: commands.Context, number_of_mentors: int):
        """Creates all PODS for all TEAMS"""
        # Then, create the actual pods by calling the singular create_pod function
        # We subtract one so that there is an extra mentor left, who is designated to the pod called overflow
        guild: discord.Guild = ctx.guild
        role: discord.Role = guild.get_role(EnvironmentVariables.MENTOR_ROLE)
        for x in range(0, number_of_mentors - 1):
            await self.create_pod(self, ctx,
                                  PodNameFinder.find_a_suitable_pod_name(),
                                  MentorFinder.find_a_suitable_mentor(role))
        await self.create_pod(self, ctx,
                              "Overflow",
                              MentorFinder.find_a_suitable_mentor(role))

    @commands.command(name='assign_pods')
    @checks.requires_staff_role()
    async def assign_pods(self, ctx: commands.Context):
        """Assigns remaining TEAMS to PODS"""
        await Helper.assign_pods_helper(ctx.bot)

    @commands.command(name='teams', aliases=['list-teams', 'list_teams', 'listteams'])
    @checks.requires_mentor_role()
    async def teams(self, ctx: commands.Context, pod_name_or_discord_user: Union[str, discord.Member] = None):
        """Displays TEAMS of a POD in CURRENT CHANNEL"""
        current_channel: discord.TextChannel = ctx.channel
        teams = await TeamConverter.get_teams(current_channel, pod_name_or_discord_user)
        is_pod = True if PodConverter.get_pod_by_name(pod_name_or_discord_user) is not None else False
        if is_pod:
            await current_channel.send(f"I found a couple of projects for Pod {pod_name_or_discord_user}")
        else:
            await current_channel.send(f"I found a couple of projects for {pod_name_or_discord_user}")

        for team in teams:
            await current_channel.send(embed=GenerateEmbed.for_single_showcase_team(team, False))

    @commands.command(name='pods', aliases=['list_pods', 'list-pods, list_all_pods', 'listpods'])
    @checks.requires_staff_role()
    async def pods(self, ctx: commands.Context):
        """Displays ALL PODS in CURRENT CHANNEL"""
        current_channel: discord.DMChannel = ctx.channel
        all_pods = PodDBService.get_all_pods()
        if len(all_pods) == 0:
            await current_channel.send("There are no pods.")
            return

        message = "The current created pods are: \n"
        for pod in all_pods:
            message += f"Pod {pod.name}\n"
        await current_channel.send(message)

    @commands.command("add_mentor")
    @checks.requires_staff_role()
    async def add_mentor(self, ctx: commands.Context, mentor: discord.Member, pod_name: str = None):
        """Gives additional permissions to a particular discord member"""
        # If the pod name is not given, use the current channels name as the argument
        pod = await PodConverter.get_pod(ctx.channel, pod_name)
        await Helper.add_mentor_helper(ctx.bot, mentor, None, pod)

    @commands.command(name="merge_pods")
    @checks.requires_staff_role()
    async def merge_pods(self, ctx: commands.Context, pod_from: str, pod_to: str):
        """Merges one PDO into another POD"""
        pod_to_be_merged = PodConverter.get_pod_by_name(pod_from)
        pod_being_merged_into = PodConverter.get_pod_by_name(pod_to)
        pod_to_be_merged_channel = await ctx.bot.fetch_channel(pod_to_be_merged.tc_id)
        pod_being_merged_into_channel: discord.DMChannel = await ctx.bot.fetch_channel(pod_being_merged_into.tc_id)
        current_channel: discord.DMChannel = ctx.channel

        await current_channel.send("Pods are currently being merged... give me one second...")

        await PodDispatcher.merge_pods(ctx.bot, pod_to_be_merged, pod_being_merged_into,
                                       pod_to_be_merged_channel, pod_being_merged_into_channel)

        await current_channel.send(f"Done! Pod {pod_from.capitalize()} has been successfully merged into Pod "
                                   f"{pod_to.capitalize()}. \n"
                                   f"If there were any teams, they have been merged as well.")

    @commands.command(name="test")
    @checks.requires_staff_role()
    async def test(self, ctx: commands.Context, pod_name: str = None):
        current_channel: discord.TextChannel = ctx.channel
        pod = await PodConverter.get_pod(current_channel, pod_name)
        await ctx.send(f'Pod was found. ID is {pod.id}')

    @commands.command(name='remove_pod')
    @checks.requires_staff_role()
    async def remove_pod(self, ctx: commands.Context, pod_name: str = None):
        current_channel: discord.TextChannel = ctx.channel
        pod = await PodConverter.get_pod(current_channel, pod_name)
        channel_to_remove = await ctx.bot.fetch_channel(pod.tc_id)
        await PodDispatcher.remove_pod(pod, channel_to_remove)

    @commands.command(name='remove_all_pods')
    @checks.requires_staff_role()
    async def remove_all_pods(self, ctx: commands.Context):
        """Removes all Pods from Alembic and deletes all text channels from category"""
        all_pods = PodDBService.get_all_pods()
        category = discord.utils.get(ctx.guild.categories, id=EnvironmentVariables.CATEGORY)
        if len(all_pods) == 0:
            await ctx.send("There are no pods to remove.")
            return

        await ctx.send("I am in the process of removing pods, give me a couple of seconds... \n"
                       "I will let you know when I am done.")

        await PodDispatcher.remove_all_pods(all_pods, category)

        await ctx.send("All pods have been removed.")

    @commands.command(name='send_message')
    @checks.requires_staff_role()
    async def send_message(self, ctx: commands.Context, pod_name: str, *message):
        """Sends a message to a single pod using the bot account"""
        pod = PodConverter.get_pod_by_name(pod_name)
        pod_channel = await ctx.bot.fetch_channel(pod.tc_id)
        await pod_channel.send(" ".join(message[:]))

    @commands.command(name='send_message_all')
    @checks.requires_staff_role()
    async def send_message_all(self, ctx: commands.Context, *message):
        """Sends a message to every pod using the bot account"""
        all_pods = PodDBService.get_all_pods()
        for pod in all_pods:
            pod_channel = await ctx.bot.fetch_channel(pod.tc_id)
            await pod_channel.send(" ".join(message[:]))

    @commands.command(name='get_all_teams')
    @checks.requires_staff_role()
    async def get_all_teams(self, ctx: commands.Context):
        """Displays PODS in CHANNEL"""
        all_teams = await PodGQLService.get_all_showcase_teams()
        current_channel: discord.DMChannel = ctx.channel
        await current_channel.send("The current created team(s) in showcase are: \n")
        for embed in GenerateEmbed.for_all_showcase_teams(all_teams):
            await current_channel.send(embed=embed)

    @commands.command(name='secret')
    @checks.requires_staff_role()
    async def secret(self, ctx: commands.Context):
        """Secret Command"""
        await ctx.send("Jacob Cuomo is my dad.")


def setup(bot):
    bot.add_cog(Pods(bot))