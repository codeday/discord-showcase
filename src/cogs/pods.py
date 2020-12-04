from idlelib.undo import CommandSequence

import discord
from discord.ext import commands
from os import getenv

from db.models import session_creator
from services.podservice import PodService
from utils.person import id_from_mention
from services.gqlservice import GQLService
from utils import checks

# The list below shows all possible names that a pod can have. There are currently 118 different names.
available_names = ["Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon", "Nitrogen",
                   "Oxygen", "Fluorine", "Neon", "Sodium", "Magnesium", "Aluminum", "Silicon",
                   "Phosphorus", "Sulfur", "Chlorine", "Argon", "Potassium", "Calcium", "Scandium",
                   "Titanium", "Vanadium", "Chromium", "Manganese", "Iron", "Cobalt", "Nickel",
                   "Copper", "Zinc", "Gallium", "Germanium", "Arsenic", "Selenium", "Bromine",
                   "Krypton", "Rubidium", "Strontium", "Yttrium", "Zirconium", "Niobium",
                   "Molybdenum", "Technetium", "Ruthenium", "Rhodium", "Palladium", "Silver",
                   "Cadmium", "Indium", "Tin", "Antimony", "Tellurium", "Iodine", "Xenon",
                   "Caesium", "Barium", "Lanthanum", "Cerium", "Praseodymium", "Neodymium",
                   "Promethium", "Samarium", "Europium", "Gadolinium", "Terbium", "Dysprosium",
                   "Holmium", "Erbium", "Thulium", "Ytterbium", "Lutetium", "Hafnium", "Tantalum",
                   "Tungsten", "Rhenium", "Osmium", "Iridium", "Platinum", "Gold", "Mercury", "Thallium",
                   "Lead", "Bismuth", "Polonium", "Astatine", "Radon", "Francium", "Radium", "Actinium",
                   "Thorium", "Protactinium", "Uranium", "Neptunium", "Plutonium", "Americium", "Curium",
                   "Berkelium", "Californium", "Einsteinium", "Fermium", "Mendelevium", "Nobelium", "Lawrencium",
                   "Rutherfordium", "Dubnium", "Seaborgium", "Bohrium", "Hassium", "Meitnerium", "Darmstadtium",
                   "Roentgenium", "Copernicium", "Nihonium", "Flerovium", "Moscovium", "Livermorium", "Tennessine",
                   "Oganesson"]


class Pods(commands.Cog, name="Pods"):
    """Contains information pertaining to Pods"""

    def __init__(self, bot):
        self.bot: discord.ext.commands.Bot = bot
        self.staff_role = int(getenv("ROLE_STAFF", 689960285926195220))
        self.mentor_role = int(getenv("ROLE_MENTOR", 782363834836975646))
        self.category = int(getenv("CATEGORY", 783229579732320257))
        self.numOfMentors = 3
        self.teams_per_pod = 3
        self.check_in_messages = {}

    @commands.command(name='create_pod')
    # @checks.requires_staff_role()
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
            "Hello <@" + str(mentor.id) + "> you have been selected to be the mentor for this pod! Teams will be "
                                          "added shortly.")

        PodService.create_pod(pod_name, tc.id, mentor.id)

        pass

    @commands.command(name='create_pods')
    # @checks.requires_staff_role()
    async def create_pods(self, ctx: commands.Context, number_of_mentors):
        """Creates all PODS for all TEAMS"""
        self.numOfMentors = number_of_mentors
        for x in range(0, int(self.numOfMentors)):
            await self.create_pod(ctx, self.find_a_suitable_pod_name(), self.find_a_suitable_mentor(ctx))
        await self.create_pod(ctx, "overflow", self.find_a_suitable_mentor(ctx))

    @commands.command(name='assign_pod')
    # @checks.requires_staff_role()
    async def assign_pod(self, ctx: commands.Context, team_id, pod_name):
        """Assigns a TEAM to a particular POD"""
        await self.assign_pod_helper(self.bot, team_id, pod_name)

    @commands.command(name='assign_pods')
    # @checks.requires_staff_role()
    async def assign_pods(self, ctx: commands.Context):
        """Assigns remaining TEAMS to PODS"""
        await self.assign_pods_helper(self.bot)

    @staticmethod
    async def assign_pod_helper(bot: discord.ext.commands.Bot, team_id, pod_name, session):
        current_pod = PodService.get_pod_by_name(pod_name, session)
        showcase_team = await GQLService.get_showcase_team_by_id(team_id)

        if current_pod is not None:
            PodService.add_team_to_pod(current_pod, team_id, session)
            await GQLService.record_pod_on_team_metadata(showcase_team["id"], str(current_pod.id))

            tc = await bot.fetch_channel(int(current_pod.tc_id))
            await tc.send("Team " + showcase_team["name"] + " has joined the pod!")
            # Add all members to text channel
            print(showcase_team["members"])
            guild: discord.Guild = await bot.fetch_guild(689213562740277361)
            for showcase_member in showcase_team["members"]:
                discordID = showcase_member["account"]["discordId"]
                print(discordID)
                try:
                    member = await guild.fetch_member(discordID)
                    await tc.set_permissions(member, overwrite=discord.PermissionOverwrite(**dict(discord.Permissions.text())))
                except discord.errors.NotFound:
                    print("A user was not found within the server")
                except:
                    print("Some other sort of error has occurred.")

    @staticmethod
    async def add_user_to_pod_tc(bot: discord.ext.commands.Bot, member_with_project):
        # Get User Member Object AND Get text channel object
        session = session_creator()
        print(member_with_project)
        discord_id = member_with_project["account"]["discordId"]
        guild: discord.Guild = await bot.fetch_guild(689213562740277361)
        showcase_team = await GQLService.get_showcase_team_by_showcase_user(member_with_project["username"])

        for team in showcase_team:
            pod = PodService.get_pod_by_id(team["pod"], session)
            try:
                member: discord.Member = await guild.fetch_member(discord_id)

                tc = await bot.fetch_channel(pod.tc_id)

                await tc.set_permissions(member, read_messages=True, read_message_history=True,
                                         send_messages=True, embed_links=True, attach_files=True,
                                         external_emojis=True, add_reactions=True)
            except discord.errors.NotFound:
                print("A user was not found within the server")
            except:
                print("Some other sort of error has occurred.")
        session.commit()
        session.close()


    @staticmethod
    async def remove_user_from_pod_tc(bot: discord.ext.commands.Bot, member_with_project):
        print(member_with_project)


    @staticmethod
    async def assign_pods_helper(bot: discord.ext.commands.Bot):
        session = session_creator()
        all_teams_without_pods = await GQLService.get_all_showcase_teams_without_pods()

        for team in all_teams_without_pods:
            smallest_pod = PodService.get_smallest_pod(session)
            print(smallest_pod)
            if smallest_pod:
                await Pods.assign_pod_helper(bot, team["id"], smallest_pod.name, session)
            else:
                await Pods.assign_pod_helper(bot, team["id"], "overflow", session)

        session.commit()
        session.close()

    @commands.command(name='list_teams')
    # @checks.requires_staff_role()
    async def list_teams(self, ctx: commands.Context, pod_name):
        """Displays TEAMS of a POD in CHANNEL"""
        session = session_creator()
        pod = PodService.get_pod_by_name(pod_name, session)
        current_channel: discord.DMChannel = ctx.channel
        await current_channel.send("The current teams inside of Pod " + pod_name + " are:")
        for team in pod.teams:
            await current_channel.send("Team " + team.showcase_id)
        session.commit()
        session.close()

    @commands.command(name='list_pods')
    # @checks.requires_staff_role()
    async def list_pods(self, ctx: commands.Context):
        """Displays PODS in CHANNEL"""
        session = session_creator()
        all_pods = PodService.get_all_pods(session)
        current_channel: discord.DMChannel = ctx.channel
        await current_channel.send("The current created pods are:")
        for pod in all_pods:
            await current_channel.send("Pod " + pod.name)
        session.commit()
        session.close()

    @commands.command(name='remove_all_pods')
    # @checks.requires_staff_role()
    async def remove_all_pods(self, ctx: commands.Context):
        """Removes all Pods from Alembic"""
        session = session_creator()
        PodService.remove_all_pods()
        allTeams = await GQLService.get_all_showcase_teams()
        for team in allTeams:
            await GQLService.unset_team_metadata(team["id"])
        await ctx.send("All Pods have been removed.")
        session.commit()
        session.close()

    @commands.command(name='get_teams_from_gql')
    # @checks.requires_staff_role()
    async def get_teams_from_gql(self, ctx: commands.Context):
        """Displays PODS in CHANNEL"""
        all_teams = await GQLService.get_all_showcase_teams()
        current_channel: discord.DMChannel = ctx.channel
        await current_channel.send("The current created teams in showcase are:")
        for team in all_teams:
            await current_channel.send("Team " + team['name'])

    @commands.command(name='get_teams_by_user')
    # @checks.requires_staff_role()
    async def get_teams_by_user_gql(self, ctx: commands.Context, user: discord.User):
        """Displays PODS in CHANNEL"""
        usergql = str(await GQLService.get_showcase_username_from_discord_id(str(user.id)))
        team = await GQLService.get_showcase_team_by_showcase_user(usergql)
        print(team)
        current_channel: discord.DMChannel = ctx.channel
        await current_channel.send("The team that " + user + " is in is " + team)

    def find_a_suitable_pod_name(self):
        for pod_name in available_names:
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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if self.emoji_is_valid(payload.emoji):
            guild: discord.Guild = payload.member.guild
            session = session_creator()

            pod = PodService.get_pod_by_channel_id(
                str(payload.channel_id), session)
            if pod is not None:
                showcase_user = str(await GQLService.get_showcase_user_from_discord_id(str(payload.member.id)))
                team_that_reacted = await GQLService.get_showcase_team_by_showcase_user(showcase_user)
                channel: discord.DMChannel = guild.get_channel(
                    int(payload.channel_id))
                message = await channel.fetch_message(payload.message_id)
                user_who_posted_message = message.author
                if user_who_posted_message == self.bot.user.id:
                    await GQLService.send_team_reacted(str(team_that_reacted.id), str(showcase_user.username), int(self.emoji_to_value(payload.emoji)))
            session.commit()
            session.close()

    @staticmethod
    def emoji_is_valid(emoji):
        if emoji == "😀" or emoji == "😐" or emoji == "☹":
            return True
        return False

    @staticmethod
    def emoji_to_value(emoji):
        emoji_values = {
            "😀": 1,
            "😐": 0,
            "☹": -1
        }
        return emoji_values.get(emoji)


def setup(bot):
    bot.add_cog(Pods(bot))
