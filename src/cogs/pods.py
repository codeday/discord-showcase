from discord.ext import commands
from utils import checks

# The list below shows all possible names that a pod can have. There are currently 118 different names.
suitableNames = {"Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon", "Nitrogen",
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
         "Roentgenium", "Copernicium", "Nihonium", "Flerovium", "Moscovium", "Livermorium","Tennessine",
         "Oganesson"}


class Pods(commands.Cog, name="Pods"):
    """Contains information pertaining to Pods"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create pod')
    @checks.requires_staff_role()
    async def create_pod(self, ctx: commands.Context, pod_name, size, mentor):
        """Creates a POD for a team"""
        pass

    @commands.command(name='create pods')
    @checks.requires_staff_role()
    async def create_pods(self, ctx: commands.Context, size):
        """Creates all PODS for all TEAMS"""
        numberOfTeams = 10
        #for x in range(0, numberOfTeams):
        pass

    @commands.command(name='assign pod')
    @checks.requires_staff_role()
    def assign_pod(self, ctx: commands.Context, team_name, pod_name):
        """Assigns a TEAM to a particular POD"""
        pass

    @commands.command(name='assign pods')
    @checks.requires_staff_role()
    def assign_pods(self, ctx: commands.Context, team_name, pod_name):
        """Assigns remaining TEAMS to PODS"""
        pass

    @commands.command(name='list teams')
    @checks.requires_staff_role()
    def list_teams(self, ctx: commands.Context, team_name, pod_name):
        """Displays TEAMS in CHANNEL"""
        pass

    @commands.command(name='list pods')
    @checks.requires_staff_role()
    def list_pods(self, ctx: commands.Context, team_name, pod_name):
        """Displays PODS in CHANNEL"""
        pass

def setup(bot):
    bot.add_cog(Pods(bot))
