import math

import discord

"""
    The purpose of this class is to generate embeds such as for when a project gets added to a pod or when a user joins
    or leaves a particular pod.
"""


class GenerateEmbed:

    @staticmethod
    def for_single_showcase_team(showcase_team, join_message=True) -> discord.Embed:
        member_mentions = []
        for showcase_member in showcase_team["members"]:
            member_mentions.append(f"<@{str(showcase_member['account']['discordId'])}>")
        embed = None
        if join_message:
            embed = discord.Embed(title=f"Project {showcase_team['name']} has joined the pod!",
                                  url=f"https://showcase.codeday.org/project/{showcase_team['id']}", color=0xff6766)
        else:
            embed = discord.Embed(title=f"Project {showcase_team['name']}",
                                  url=f"https://showcase.codeday.org/project/{showcase_team['id']}", color=0xff6766)
        embed.add_field(name=f"Project member(s): ", value=f"{', '.join(member_mentions)}", inline=False)
        return embed

    @staticmethod
    def for_all_showcase_teams(teams) -> list[discord.Embed]:
        embeds = []
        number_of_embeds = math.ceil(len(teams) / 25)
        count = 0
        for i in range(0, number_of_embeds):
            embed = None
            if i == 0:
                embed = discord.Embed(title=f"There are a total of {len(teams)} teams.",
                                      url=f"https://showcase.codeday.org/", color=0xff6766)
            else:
                embed = discord.Embed(title=f"Continuing to display teams... Panel {i+1} out of {number_of_embeds}",
                                      url=f"https://showcase.codeday.org/", color=0xff6766)

            for i in range(count, count+25):
                try:
                    if teams[i] is not None:
                        embed.add_field(name=f"{teams[i]['name']}:", value=f"https://showcase.codeday.org/project/{teams[i]['id']}",
                                        inline=True)
                except IndexError:
                    print("Teams out of bound when generating embeds")
                count += 1
            embeds.append(embed)
        return embeds