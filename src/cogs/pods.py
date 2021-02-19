from idlelib.undo import CommandSequence

import discord
from discord.ext import commands
from os import getenv

from db.models import session_creator
from services.podservice import PodService
from text.podhelpchannel import PodHelpChannel
from text.podnames import PodNames
from services.gqlservice import GQLService
from utils import checks


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
            # Default User Access to a Pod
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

        PodService.create_pod(pod_name, tc.id, mentor.id)

        pass

    @commands.command(name='create_pods')
    @checks.requires_staff_role()
    async def create_pods(self, ctx: commands.Context, number_of_mentors):
        """Creates all PODS for all TEAMS"""
        # First, create a help channel with text from the podhelpchannel.py file
        guild: discord.Guild = ctx.guild
        overwrites = {
            # Default User Access to the help channel
            guild.default_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True),
            guild.get_role(self.staff_role): discord.PermissionOverwrite(**dict(discord.Permissions.text())),
            guild.me: discord.PermissionOverwrite(read_messages=True, read_message_history=True),
        }

        tc = await guild.create_text_channel("what-is-a-pod", overwrites=overwrites,
                                             category=guild.get_channel(self.category),
                                             reason=None)
        await tc.send(PodHelpChannel.initial_message)
        # END of help channel text channel creation

        # Then, create the actual pods by calling the singular create_pod function
        # We subtract one so that there is an extra mentor left, who is designated to the pod called overflow
        for x in range(0, int(number_of_mentors) - 1):
            await self.create_pod(ctx, self.find_a_suitable_pod_name(), self.find_a_suitable_mentor(ctx))
        await self.create_pod(ctx, "overflow", self.find_a_suitable_mentor(ctx))

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
    async def assign_pod_helper(bot: discord.ext.commands.Bot, team_id, pod_name, session):
        current_pod = PodService.get_pod_by_name(pod_name, session)
        showcase_team = await GQLService.get_showcase_team_by_id(team_id)
        print(showcase_team)
        if current_pod is not None and showcase_team is not None:
            PodService.add_team_to_pod(current_pod, team_id, session)
            await GQLService.record_pod_on_team_metadata(showcase_team["id"], str(current_pod.id))

            tc = await bot.fetch_channel(int(current_pod.tc_id))
            member_mentions = []
            for showcase_member in showcase_team["members"]:
                member_mentions.append(f"<@{str(showcase_member['account']['discordId'])}>")
            embed = discord.Embed(title=f"Project {showcase_team['name']} has joined the pod!",
                                  url=f"https://showcase.codeday.org/project/{team_id}", color=0xff6766)
            embed.add_field(name=f"Project member(s): ", value=f"{', '.join(member_mentions)}", inline=False)
            await tc.send(embed=embed)

            # store initial message in gql
            # Add all members to text channel
            print(showcase_team["members"])
            guild: discord.Guild = await bot.fetch_guild(689213562740277361)
            for showcase_member in showcase_team["members"]:
                discordID = showcase_member["account"]["discordId"]
                print(discordID)
                try:
                    member = await guild.fetch_member(discordID)
                    await tc.set_permissions(member, read_messages=True, read_message_history=True,
                                             send_messages=True, embed_links=True, attach_files=True,
                                             external_emojis=True, add_reactions=True)
                except discord.errors.NotFound:
                    print("A user was not found within the server")
                except:
                    print("Some other sort of error has occurred.")
        else:
            print("Did nto make it ")

    @staticmethod
    async def assign_pods_helper(bot: discord.ext.commands.Bot):
        session = session_creator()
        all_teams_without_pods = await GQLService.get_all_showcase_teams_without_pods()

        for team in all_teams_without_pods:
            if len(team["members"]) >= 1:
                print(team)
                smallest_pod = PodService.get_smallest_pod(session, Pods.teams_per_pod)
                print(smallest_pod)
                if smallest_pod:
                    await Pods.assign_pod_helper(bot, team["id"], smallest_pod.name, session)
                else:
                    await Pods.assign_pod_helper(bot, team["id"], "overflow", session)

        session.commit()
        session.close()

    @staticmethod
    async def add_or_remove_user_to_pod_tc(bot: discord.ext.commands.Bot, member_with_project, should_be_removed):
        # Get User Member Object AND Get text channel object
        session = session_creator()
        print(member_with_project)
        discord_id = member_with_project["account"]["discordId"]
        guild: discord.Guild = await bot.fetch_guild(689213562740277361)
        showcase_team = await GQLService.get_showcase_team_by_id(member_with_project["project"]["id"])

        pod = PodService.get_pod_by_id(showcase_team["pod"], session)
        try:
            member: discord.Member = await guild.fetch_member(discord_id)

            tc = await bot.fetch_channel(pod.tc_id)

            # User is being removed from the pod tc
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

            # User is being added to the pod tc
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
        except discord.errors.NotFound:
            print("A user was not found within the server")
        except:
            print("Some other sort of error has occurred.")
        session.commit()
        session.close()

    @commands.command(name='list_teams')
    @checks.requires_staff_role()
    async def list_teams(self, ctx: commands.Context, pod_name):
        """Displays TEAMS of a POD in CURRENT CHANNEL"""
        session = session_creator()
        pod = PodService.get_pod_by_name(pod_name, session)
        current_channel: discord.DMChannel = ctx.channel
        await current_channel.send("The current teams inside of Pod " + pod_name + " are:")
        for team in pod.teams:
            await current_channel.send("Team " + team.showcase_id)
        session.commit()
        session.close()

    @commands.command(name='list_pods')
    @checks.requires_staff_role()
    async def list_pods(self, ctx: commands.Context):
        """Displays ALL PODS in CURRENT CHANNEL"""
        session = session_creator()
        all_pods = PodService.get_all_pods(session)
        current_channel: discord.DMChannel = ctx.channel
        if len(all_pods) >= 1:
            await current_channel.send("The current created pods are:")
            for pod in all_pods:
                await current_channel.send("Pod " + pod.name)
        else:
            await current_channel.send("There are no pods.")
        session.commit()
        session.close()

    @commands.command(name="merge_pods")
    @checks.requires_staff_role()
    async def merge_pods(self, ctx: commands.Context, pod_from, pod_to):
        """Merges one PDO into another POD"""
        session = session_creator()
        pod_to_be_merged = PodService.get_pod_by_name(pod_from, session)
        pod_being_merged_into = PodService.get_pod_by_name(pod_to, session)
        print(pod_to_be_merged)
        print(pod_being_merged_into)
        current_channel: discord.DMChannel = ctx.channel
        if pod_being_merged_into is not None and pod_being_merged_into is not None:
            await current_channel.send("Pods are currently being merged... give me one second...")
            pod_being_merged_into_channel: discord.DMChannel = await self.bot.fetch_channel(pod_being_merged_into.tc_id)
            pod_to_be_merged_channel = await self.bot.fetch_channel(pod_to_be_merged.tc_id)
            await pod_being_merged_into_channel.send("A pod is being merged into this channel...")
            await pod_being_merged_into_channel.send("The projects joining this pod are: ")
            await pod_to_be_merged_channel.delete()
            while len(pod_to_be_merged.teams) > 0:
                team = pod_to_be_merged.teams[0]
                await self.assign_pod_helper(self.bot, team.showcase_id, pod_being_merged_into.name, session)
                # showcase_team = await GQLService.get_showcase_team_by_id(team.showcase_id)
                await GQLService.unset_team_metadata(team.showcase_id)
                await GQLService.record_pod_on_team_metadata(team.showcase_id, str(pod_being_merged_into.id))
            await current_channel.send("Done!")
        else:
            await current_channel.send("One of the pod names were not correct. Please specify only the name after pod-")
        session.commit()
        session.close()

        PodService.remove_pod(pod_from)

    @commands.command(name='remove_pod')
    @checks.requires_staff_role()
    async def remove_pod(self, ctx: commands.Context, name_of_pod):
        session = session_creator()
        pod_to_remove = PodService.get_pod_by_name(name_of_pod, session)
        await ctx.send("Deleting the " + pod_to_remove.name + " pod...")
        pod_to_remove_channel = await self.bot.fetch_channel(pod_to_remove.tc_id)
        await pod_to_remove_channel.delete()
        for team in pod_to_remove.teams:
            await GQLService.unset_team_metadata(team.showcase_id)
        PodService.remove_pod(name_of_pod)
        await ctx.send("Pod " + pod_to_remove.name + " has been removed.")
        session.commit()
        session.close()

    @commands.command(name='remove_all_pods')
    @checks.requires_staff_role()
    async def remove_all_pods(self, ctx: commands.Context):
        """Removes all Pods from Alembic and deletes all text channels from category"""
        session = session_creator()
        all_pods = PodService.get_all_pods(session)
        if len(all_pods) >= 1:
            await ctx.send("Removing all pods... give me one second...")
            category = discord.utils.get(ctx.guild.categories, id=self.category)
            for channel in category.channels:
                await channel.delete()
            PodService.remove_all_pods()
            allTeams = await GQLService.get_all_showcase_teams()
            for team in allTeams:
                await GQLService.unset_team_metadata(team["id"])
            await ctx.send("All Pods have been removed.")
        else:
            await ctx.send("There are no pods to remove.")
        session.commit()
        session.close()

    @commands.command(name='get_teams_from_gql')
    @checks.requires_staff_role()
    async def get_teams_from_gql(self, ctx: commands.Context):
        """Displays PODS in CHANNEL"""
        all_teams = await GQLService.get_all_showcase_teams()
        current_channel: discord.DMChannel = ctx.channel
        await current_channel.send("The current created teams in showcase are:")
        for team in all_teams:
            await current_channel.send("Team " + team['name'])

    @commands.command(name='get_teams_by_user')
    @checks.requires_staff_role()
    async def get_teams_by_user_gql(self, ctx: commands.Context, user: discord.User):
        """Displays PODS in CHANNEL"""
        usergql = str(await GQLService.get_showcase_username_from_discord_id(str(user.id)))
        team = await GQLService.get_showcase_team_by_showcase_user(usergql)
        print(team)
        current_channel: discord.DMChannel = ctx.channel
        await current_channel.send("The team that " + user + " is in is " + team)

    def find_a_suitable_pod_name(self):
        for pod_name in PodNames.available_names:
            if PodService.get_pod_by_name(pod_name) is None:
                # Pod Name is suitable, return that pod name
                return pod_name
        return None  # No Valid Name was available

    def find_a_suitable_mentor(self, ctx):
        # Get List of Mentors from Discord Role and see if they're already in the taken mentors list
        guild: discord.Guild = ctx.guild
        role: discord.Role = guild.get_role(self.mentor_role)
        print(role.members)
        for member in role.members:
            if PodService.get_pod_by_mentor_id(str(member.id)) is None:
                # Mentor is Suitable, return that mentor object
                return member
        return None  # No Mentor was available


def setup(bot):
    bot.add_cog(Pods(bot))
