from typing import Union

import discord

from converters.PodConverter import PodConverter
from discord.ext import commands
from os import getenv

from converters.TeamConverter import TeamConverter
from finders.mentorfinder import MentorFinder
from finders.podnamefinder import PodNameFinder
from services.PodDispatcher import PodDispatcher
from services.poddbservice import PodDBService
from services.podgqlservice import PodGQLService
from utils import checks
from utils.generateembed import GenerateEmbed
from utils.setpermissions import SetPermissions


class Pods(commands.Cog, name="Pods"):
    """Contains information pertaining to Pods"""

    # How many teams should be in a singular pod? Change that value here. Default is 5.
    teams_per_pod = int(getenv("TEAMS_PER_POD", 5))

    def __init__(self, bot):
        self.bot: discord.ext.commands.Bot = bot

        # The role in which the bot will give all permissions to the pod channels
        self.staff_role = int(getenv("ROLE_STAFF", 689960285926195220))

        # The role in which the bot will pick a mentor from for each text channel
        self.mentor_role = int(getenv("ROLE_MENTOR", 782363834836975646))

        # The category in which the pods will reside
        self.category = int(getenv("CATEGORY", 783229579732320257))

    # For permissions attributes and other information, use the following links:
    # https://discordpy.readthedocs.io/en/latest/api.html#discord.Permissions
    # https://discordpy.readthedocs.io/en/latest/api.html#discord.TextChannel.set_permissions

    @commands.command(name='create_pod')
    @checks.requires_staff_role()
    async def create_pod(self, ctx: commands.Context, pod_name, mentor: discord.Member):
        """Creates a POD for a team"""

        """Create a text channel"""
        guild: discord.Guild = ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.get_role(self.staff_role): discord.PermissionOverwrite(**dict(discord.Permissions.text())),
            guild.me: discord.PermissionOverwrite(read_messages=True, read_message_history=True),
        }

        tc = await guild.create_text_channel("pod " + pod_name, overwrites=overwrites,
                                             category=guild.get_channel(
                                                 self.category),
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
    async def create_pods(self, ctx: commands.Context, number_of_mentors):
        """Creates all PODS for all TEAMS"""
        # Then, create the actual pods by calling the singular create_pod function
        # We subtract one so that there is an extra mentor left, who is designated to the pod called overflow
        for x in range(0, int(number_of_mentors) - 1):
            await self.create_pod(ctx,
                                  PodNameFinder.find_a_suitable_pod_name(),
                                  MentorFinder.find_a_suitable_mentor(ctx))
        await self.create_pod(ctx,
                              "Overflow",
                              MentorFinder.find_a_suitable_mentor(ctx))

    @commands.command(name='assign_pod')
    @checks.requires_staff_role()
    async def assign_pod(self, ctx: commands.Context, team_id, pod_name):
        """Assigns a TEAM to a particular POD"""
        await self.assign_pod_helper(self.bot, team_id, pod_name)

    @commands.command(name='assign_pods')
    @checks.requires_staff_role()
    async def assign_pods(self, ctx: commands.Context):
        """Assigns remaining TEAMS to PODS"""
        await self.assign_pods_helper(self.bot)

    # Some notes about embedded messages:
    # - To display fields side-by-side, you need at least two consecutive fields set to inline
    # - The timestamp will automatically adjust the timezone depending on the user's device
    # - Mentions of any kind will only render correctly in field values and descriptions
    # - Mentions in embeds will not trigger a notification
    @staticmethod
    async def assign_pod_helper(bot: discord.ext.commands.Bot, team_id, pod_name):
        current_pod = PodConverter.get_pod_by_name(pod_name)
        showcase_team = await TeamConverter.get_showcase_team_by_id(team_id)
        print(showcase_team)

        await PodDispatcher.assign_pod(current_pod, showcase_team)

        tc = await bot.fetch_channel(int(current_pod.tc_id))

        await tc.send(embed=GenerateEmbed.generate_embed(showcase_team))
        await SetPermissions.for_channel_with_showcase_team(bot, tc, showcase_team)

    @staticmethod
    async def assign_pods_helper(bot: discord.ext.commands.Bot):
        all_teams_without_pods = await TeamConverter.get_all_showcase_teams_without_pods()

        for team in all_teams_without_pods:
            if len(team["members"]) >= 1:
                smallest_pod = PodDispatcher.get_smallest_pod()
                if len(smallest_pod.teams) < Pods.teams_per_pod:
                    await Pods.assign_pod_helper(bot, team["id"], smallest_pod.name)
                else:
                    await Pods.assign_pod_helper(bot, team["id"], "overflow")

    @staticmethod
    async def add_or_remove_user_to_pod_tc(bot: discord.ext.commands.Bot, member_with_project, should_be_removed):
        """Add/remove users to a pod text channel, occurs when someone joins or leaves a team in showcase"""
        print(member_with_project)
        discord_id = member_with_project["account"]["discordId"]
        guild: discord.Guild = await bot.fetch_guild(689213562740277361)
        showcase_team = await TeamConverter.get_showcase_team_by_id(member_with_project["project"]["id"])

        pod = PodConverter.get_pod_by_id(showcase_team["pod"])

        member: discord.Member = await guild.fetch_member(discord_id)
        tc = await bot.fetch_channel(pod.tc_id)

        # Occurs when a user left a showcase team and is now being removed from the pod text channel
        if should_be_removed:
            await tc.set_permissions(member, read_messages=False, read_message_history=False,
                                     send_messages=False, embed_links=False, attach_files=False,
                                     external_emojis=False, add_reactions=False)
            embed = discord.Embed(
                title=f"{member_with_project['username']} left project {showcase_team['name']}",
                url=f"https://showcase.codeday.org/project/{showcase_team['id']}",
                color=0xff6766)
            embed.add_field(name="Member: ", value=f"<@{member_with_project['account']['discordId']}>",
                            inline=False)
            await tc.send(embed=embed)
        # Occurs when a user joins a showcase team and is now being added to the pod text channel
        else:
            await tc.set_permissions(member, read_messages=True, read_message_history=True,
                                     send_messages=True, embed_links=True, attach_files=True,
                                     external_emojis=True, add_reactions=True)
            embed = discord.Embed(
                title=f"{member_with_project['username']} joined project {showcase_team['name']}",
                url=f"https://showcase.codeday.org/project/{showcase_team['id']}",
                color=0xff6766)
            embed.add_field(name="Member: ", value=f"<@{member_with_project['account']['discordId']}>",
                            inline=False)
            await tc.send(embed=embed)

    @commands.command(name='teams', aliases=['list-teams', 'list_teams', 'listteams'])
    @checks.requires_mentor_role()
    async def teams(self, ctx: commands.Context, pod_name_or_discord_user: Union[str, discord.Member] = None):
        """Displays TEAMS of a POD in CURRENT CHANNEL"""
        current_channel: discord.TextChannel = ctx.channel
        teams = await TeamConverter.get_teams(current_channel, pod_name_or_discord_user)

        if len(teams) == 0:
            await current_channel.send(
                "There are no projects in your pod yet. Project(s) are still being created by attendee's.")
            return

        await current_channel.send("I found a couple of project(s), here they are!")
        for team in teams:
            member_mentions = []
            for showcase_member in team["members"]:
                member_mentions.append(f"<@{str(showcase_member['account']['discordId'])}>")
            embed = discord.Embed(title=f"Project {team['name']}",
                                  url=f"https://showcase.codeday.org/project/{team.showcase_id}", color=0xff6766)
            embed.add_field(name=f"Project member(s): ", value=f"{', '.join(member_mentions)}", inline=False)
            await current_channel.send(embed=embed)

    @commands.command(name='list_pods')
    @checks.requires_staff_role()
    async def list_pods(self, ctx: commands.Context):
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
    async def add_mentor(self, ctx: commands.Context, mentor: discord.Member, pod_name=None):
        """Gives additional permissions to a particular discord member"""
        # If the pod name is not given, use the current channels name as the argument
        pod = await PodConverter.get_pod(ctx.channel, pod_name)
        await self.add_mentor_helper(ctx.bot, mentor, None, pod)

    @staticmethod
    async def add_mentor_helper(bot: discord.ext.commands.Bot, mentor: discord.Member, pod_name=None, pod=None):
        if pod is None:
            pod = PodConverter.get_pod_by_name(pod_name)

        pod_channel: discord.TextChannel = await bot.fetch_channel(pod.tc_id)
        await pod_channel.set_permissions(mentor,
                                          overwrite=discord.PermissionOverwrite(**dict(discord.Permissions.text())))
        await pod_channel.send(
            "Hello <@" +
            str(mentor.id) +
            "> you have been added as a mentor to this pod! To see a list of teams, type s~teams")

    @commands.command(name="merge_pods")
    @checks.requires_staff_role()
    async def merge_pods(self, ctx: commands.Context, pod_from, pod_to):
        """Merges one PDO into another POD"""
        pod_to_be_merged = PodConverter.get_pod_by_name(pod_from)
        pod_being_merged_into = PodConverter.get_pod_by_name(pod_to)
        pod_to_be_merged_channel = await self.bot.fetch_channel(pod_to_be_merged.tc_id)
        pod_being_merged_into_channel: discord.DMChannel = await self.bot.fetch_channel(pod_being_merged_into.tc_id)
        current_channel: discord.DMChannel = ctx.channel

        await current_channel.send("Pods are currently being merged... give me one second...")

        await PodDispatcher.merge_pods(self.bot, pod_to_be_merged, pod_being_merged_into,
                                       pod_to_be_merged_channel, pod_being_merged_into_channel)

        await current_channel.send(f"Done! Pod {pod_from} has been successfully merged into {pod_to}. \n"
                                   f"If there were any teams, they have been merged as well.")

    @commands.command(name="test")
    @checks.requires_staff_role()
    async def test(self, ctx: commands.Context, pod_name=None):
        current_channel: discord.TextChannel = ctx.channel
        pod = await PodConverter.get_pod(current_channel, pod_name)
        await ctx.send(f'Pod was found. ID is {pod.id}')

    @commands.command(name='remove_pod')
    @checks.requires_staff_role()
    async def remove_pod(self, ctx: commands.Context, pod_name=None):
        current_channel: discord.TextChannel = ctx.channel
        pod = await PodConverter.get_pod(current_channel, pod_name)
        channel_to_remove = await self.bot.fetch_channel(pod.tc_id)
        await PodDispatcher.remove_pod(pod, channel_to_remove)

    @commands.command(name='remove_all_pods')
    @checks.requires_staff_role()
    async def remove_all_pods(self, ctx: commands.Context):
        """Removes all Pods from Alembic and deletes all text channels from category"""
        all_pods = PodDBService.get_all_pods()
        category = discord.utils.get(ctx.guild.categories, id=self.category)
        if len(all_pods) == 0:
            await ctx.send("There are no pods to remove.")
            return

        await ctx.send("I am in the process of removing pods, give me a couple of seconds... \n"
                       "I will let you know when I am done.")

        await PodDispatcher.remove_all_pods(category)

        await ctx.send("All pods have been removed.")

    @commands.command(name='send_message')
    @checks.requires_staff_role()
    async def send_message(self, ctx: commands.Context, pod_name, *message):
        """Sends a message to a single pod using the bot account"""
        pod = PodConverter.get_pod_by_name(pod_name)
        pod_channel = await self.bot.fetch_channel(pod.tc_id)
        await pod_channel.send(" ".join(message[:]))

    @commands.command(name='send_message_all')
    @checks.requires_staff_role()
    async def send_message_all(self, ctx: commands.Context, *message):
        """Sends a message to every pod using the bot account"""
        all_pods = PodDBService.get_all_pods()
        for pod in all_pods:
            pod_channel = await self.bot.fetch_channel(pod.tc_id)
            await pod_channel.send(" ".join(message[:]))

    @commands.command(name='get_all_teams')
    @checks.requires_staff_role()
    async def get_all_teams(self, ctx: commands.Context):
        """Displays PODS in CHANNEL"""
        all_teams = await PodGQLService.get_all_showcase_teams()
        current_channel: discord.DMChannel = ctx.channel
        await current_channel.send("The current created team(s) in showcase are: ")
        teams_message = ""
        for team in all_teams:
            teams_message += team['name']
        await current_channel.send(teams_message)

    @commands.command(name='secret')
    @checks.requires_staff_role()
    async def secret(self, ctx: commands.Context):
        """Secret Command"""
        await ctx.send("Jacob Cuomo is my dad.")


def setup(bot):
    bot.add_cog(Pods(bot))
