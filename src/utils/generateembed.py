import discord


class GenerateEmbed:

    @staticmethod
    def generate_embed(showcase_team):
        member_mentions = []
        for showcase_member in showcase_team["members"]:
            member_mentions.append(f"<@{str(showcase_member['account']['discordId'])}>")
        embed = discord.Embed(title=f"Project {showcase_team['name']} has joined the pod!",
                              url=f"https://showcase.codeday.org/project/{showcase_team['id']}", color=0xff6766)
        embed.add_field(name=f"Project member(s): ", value=f"{', '.join(member_mentions)}", inline=False)
        return embed