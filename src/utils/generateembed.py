import discord

"""
    The purpose of this class is to generate embeds such as for when a project gets added to a pod or when a user joins
    or leaves a particular pod.
"""


class GenerateEmbed:

    @staticmethod
    def generate_embed(showcase_team) -> discord.Embed:
        member_mentions = []
        for showcase_member in showcase_team["members"]:
            member_mentions.append(f"<@{str(showcase_member['account']['discordId'])}>")
        embed = discord.Embed(title=f"Project {showcase_team['name']} has joined the pod!",
                              url=f"https://showcase.codeday.org/project/{showcase_team['id']}", color=0xff6766)
        embed.add_field(name=f"Project member(s): ", value=f"{', '.join(member_mentions)}", inline=False)
        return embed
