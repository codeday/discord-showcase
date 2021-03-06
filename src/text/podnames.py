from random import shuffle

"""
    The purpose of this class is to provide pod names for the bot to use
"""


class PodNames:
    # The list below shows all possible names that a pod can have.
    available_names = [name.capitalize() for name in ["Urchin", "Anemone", "Jellyfish", "Oyster", "Clam", "Shell", "Octopus", "Squid", "Crab",
                       "Shrimp", "Lobster", "Isopod",
                       "Metis", "Adrastea", "Amalthea", "Thebe", "Io", "Europa", "Ganymede", "Callisto", "Themisto",
                       "Leda", "Himalia", "Lysithea", "Elara", "Dia", "Carpo", "Euporie", "Thelxinoe", "Euanthe",
                       "Helike", "Orthosie", "Iocaste", "Praxidike", "Harpalyke", "Mneme", "Hermippe", "Thyone",
                       "Ananke", "Herse", "Aitne", "Kale", "Taygete", "Chaldene", "Erinome", "Aoede", "Kallichore",
                       "Kalyke", "Carme", "Callirrhoe", "Eurydome", "Pasithee", "Kore", "Cyllene", "Eukelade",
                       "Pasiphaë", "Hegemone", "Arche", "Isonoe", "Sinope", "Sponde", "Autonoe", "Megaclite",
                       "Adrastea", "Alnilam", "Alnitak", "Alpha", "Centauri", "Amalthea", "Ananke", "Bellatrix",
                       "Betelgeuse", "Callisto", "Carme", "Ceres", "Charon", "Demeter", "Elara", "Enceladus", "Eris",
                       "Europa", "Ganymede", "Himalia", "Io", "Jupiter", "Leda", "Lysithea", "Mars", "Mercury",
                       "Methone", "Metis", "Mimas", "Neptune", "Pallene", "Pasiphae", "Pluto", "Rigel", "Saturn",
                       "Sinope", "Sirius", "Thebe", "Titan", "Uranus", "Venus", "Anchovy", "Anglerfish", "Barb",
                       "Barracuda", "Barramundi", "Bass", "Betta", "Blenny", "Bluefin", "Bluegill", "Bonito", "Bream",
                       "Brill", "Brisling", "Capelin", "Carp", "Catfish", "Caviar", "Chubb", "Clown", "Knife",
                       "Clownfish", "Cod", "Coding", "Conger", "Corydora", "Cuttlefish", "Dab", "Dovii",
                       "Drum", "Eel", "Eelpout", "Flounder", "Flying", "Fish", "Frostfish",
                       "Fusilier", "Garfish", "Gaspargou", "Gilt", "Head", "Bream", "Goatfish", "Gobbleguts",
                       "Goldfish", "Green", "Terror", "Grayling", "Grilled", "Grouper", "Guppy", "Gurnard", "Haddock",
                       "Hake", "Halibut", "Herring", "Horse", "Mackerel", "Joey", "John", "Dory", "Koi", "Ling",
                       "Mackerel", "Managuense", "Marlin", "Meagre", "Minnow", "Monkfish", "Moray", "Morwong", "Mullet",
                       "Muskey", "Nudibranch", "Octopus", "Oilfish", "Oscar", "Parrot", "Perch", "Pike",
                       "Pilchard", "Piranha", "Plaice", "Platty", "Pollack", "Pompano", "Pout",
                       "Red", "Bream", "Redfish", "Remora", "Sailfish", "Saithe", "Salmon", "Sandeel",
                       "Sardine", "Sardinella", "Scorpionfish", "Sea", "Bream", "Shark",
                       "Sheepshead", "Smelt", "Smoked", "Snapper", "Sockeye", "Sole",
                       "Sprat", "Squid", "Stickleback", "Stockfish", "Sturgeon", "Sunfish", "Sunny", "Swordfish",
                       "Talapia", "Talma", "Tarpon", "Tench", "Tetra", "Trimac", "Trout", "Trumpeter", "Tub", "Gurnard",
                       "Tuna", "Turbot", "Walleye", "Weever", "Whipray", "Hake", "Wirrah",
                       "Wobbegong", "Wrasse"]]
    shuffle(available_names)

    # Name Archive: Elements
    # available_names = ["Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon", "Nitrogen",
    #                    "Oxygen", "Fluorine", "Neon", "Sodium", "Magnesium", "Aluminum", "Silicon",
    #                    "Phosphorus", "Sulfur", "Chlorine", "Argon", "Potassium", "Calcium", "Scandium",
    #                    "Titanium", "Vanadium", "Chromium", "Manganese", "Iron", "Cobalt", "Nickel",
    #                    "Copper", "Zinc", "Gallium", "Germanium", "Arsenic", "Selenium", "Bromine",
    #                    "Krypton", "Rubidium", "Strontium", "Yttrium", "Zirconium", "Niobium",
    #                    "Molybdenum", "Technetium", "Ruthenium", "Rhodium", "Palladium", "Silver",
    #                    "Cadmium", "Indium", "Tin", "Antimony", "Tellurium", "Iodine", "Xenon",
    #                    "Caesium", "Barium", "Lanthanum", "Cerium", "Praseodymium", "Neodymium",
    #                    "Promethium", "Samarium", "Europium", "Gadolinium", "Terbium", "Dysprosium",
    #                    "Holmium", "Erbium", "Thulium", "Ytterbium", "Lutetium", "Hafnium", "Tantalum",
    #                    "Tungsten", "Rhenium", "Osmium", "Iridium", "Platinum", "Gold", "Mercury", "Thallium",
    #                    "Lead", "Bismuth", "Polonium", "Astatine", "Radon", "Francium", "Radium", "Actinium",
    #                    "Thorium", "Protactinium", "Uranium", "Neptunium", "Plutonium", "Americium", "Curium",
    #                    "Berkelium", "Californium", "Einsteinium", "Fermium", "Mendelevium", "Nobelium", "Lawrencium",
    #                    "Rutherfordium", "Dubnium", "Seaborgium", "Bohrium", "Hassium", "Meitnerium", "Darmstadtium",
    #                    "Roentgenium", "Copernicium", "Nihonium", "Flerovium", "Moscovium", "Livermorium", "Tennessine",
    #                    "Oganesson"]
