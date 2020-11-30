from idlelib.undo import CommandSequence

import discord
from discord.ext import commands
from os import getenv

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

used_names = []

available_mentors = []
used_mentors = []


def find_a_suitable_pod_name():
    name = available_names[0]
    used_names.add(name)
    available_names.remove(name)
    return name


class Pods(commands.Cog, name="Pods"):
    """Contains information pertaining to Pods"""

    def __init__(self, bot):
        self.bot: discord.ext.commands.Bot = bot
        self.staff_role = int(getenv("ROLE_STAFF", 689960285926195220))
        self.mentor_role = int(getenv("ROLE_MENTOR", 782363834836975646))
        self.category = int(getenv("CATEGORY", 690001823347769430))
        self.teamsPerPod = 3
        self.numOfMentors = 50

    @commands.command(name='create_pod')  # create_pod hello 3 @asdawd
    # @checks.requires_staff_role()
    async def create_pod(self, ctx: commands.Context, pod_name, size, mentor):
        """Creates a POD for a team"""

        """Create a text channel"""
        guild: discord.Guild = ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),  # Default User Access to a Pod
            guild.get_role(self.staff_role): discord.PermissionOverwrite(**dict(discord.Permissions.text())),
            # Staff Access to a Pod
            # guild.get_member(id_from_mention(mentor)): discord.PermissionOverwrite(**dict(discord.Permissions.text())),  # Mentor Access to Pod
            guild.me: discord.PermissionOverwrite(read_messages=True, read_message_history=True),
        }

        tc = await guild.create_text_channel("team " + pod_name, overwrites=overwrites, category=guild.get_channel(self.category),
                                             reason=None)

        PodService.create_pod(pod_name, tc.id, id_from_mention(mentor))

        pass

    @commands.command(name='create_pods')
    @checks.requires_staff_role()
    async def create_pods(self, ctx: commands.Context, size):
        """Creates all PODS for all TEAMS"""
        # api call to get number of teams
        allTeams = GQLService.get_all_teams()
        for x in range(0, self.numOfMentors):
            await self.create_pod(ctx, find_a_suitable_pod_name(), self.teamsPerPod, self.find_a_suitable_mentor())

    @commands.command(name='assign_pod')
    @checks.requires_staff_role()
    async def assign_pod(self, ctx: commands.Context, team_id, pod_name):
        """Assigns a TEAM to a particular POD"""
        current_pod = PodService.get_pod_by_name(pod_name)
        showcase_team = GQLService.get_showcase_team_by_id(team_id)
        if len(current_pod.teams) <= self.teamsPerPod:
            # Team can be put into pod without brute force
            PodService.add_team_to_pod(current_pod, team_id)
        pass

    @commands.command(name='assign_pods')
    @checks.requires_staff_role()
    async def assign_pods(self, ctx: commands.Context, team_name, pod_name):
        """Assigns remaining TEAMS to PODS"""
        all_teams_without_pods = GQLService.get_all_teams_without_pods()
        all_pods = PodService.get_all_pods()
        pointer = 0

        # Fill current pods with remaining teams
        for pod in all_pods:
            if len(pod.teams) <= self.teamsPerPod:
                # add team to pod
                await self.assign_pod(ctx, all_teams_without_pods[pointer], pod)
                pointer += 1

        # Put all other teams that could not fit into a pod, into an overflow pod
        for x in range(pointer, len(all_teams_without_pods)):
            await self.assign_pod(ctx, all_teams_without_pods[pointer], "overflow")

    @commands.command(name='list_teams')
    @checks.requires_staff_role()
    async def list_teams(self, ctx: commands.Context, team_name, pod_name):
        """Displays TEAMS of a POD in CHANNEL"""
        pass

    @commands.command(name='list_pods')
    @checks.requires_staff_role()
    async def list_pods(self, ctx: commands.Context, team_name, pod_name):
        """Displays PODS in CHANNEL"""
        
        pass

    def find_a_suitable_mentor(self):
        # Get List of Mentors from Discord Role and see if they're already in the taken mentors list
        guild: discord.Guild = self.bot.get_guild(689917520370598055)
        role: discord.Role = guild.get_role(self.mentor_role)
        for user in role.members:
            if PodService.get_pod_by_mentor_id(user.id) is None:
                # Mentor is Suitable, return that mentor object
                return user
        return None  # No Mentor was available


def setup(bot):
    bot.add_cog(Pods(bot))
