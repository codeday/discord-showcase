import discord
from discord.ext import commands

from db.models import session_creator
from services.podgqlservice import GQLService


class Reactions(commands.Cog, name="Reactions"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if self.emoji_is_valid(str(payload.emoji)):
            session = session_creator()

            pod = PodService.get_pod_by_channel_id(
                str(payload.channel_id), session)
            if pod is not None:
                guild: discord.Guild = payload.member.guild
                channel: discord.DMChannel = guild.get_channel(int(payload.channel_id))
                message = await channel.fetch_message(payload.message_id)
                user_who_posted_message = message.author.id
                if user_who_posted_message == self.bot.user.id:
                    if payload.member.id != self.bot.user.id:
                        showcase_user = await GQLService.get_showcase_user_from_discord_id(str(payload.member.id))
                        team_that_reacted = await GQLService.get_showcase_team_by_showcase_user(showcase_user['username'])
                        for team in team_that_reacted:
                            await GQLService.send_team_reacted(str(team['id']), str(showcase_user['username']),
                                                               self.emoji_to_value(str(payload.emoji)))
            session.commit()
            session.close()

    def emoji_is_valid(self, emoji):
        return emoji == "😀" or emoji == "😐" or emoji == "☹"

    def emoji_to_value(self, emoji) -> float:
        emoji_values = {
            "😀": 1.0,
            "😐": 0.0,
            "☹": -1.0
        }
        return emoji_values.get(emoji)


def setup(bot):
    bot.add_cog(Reactions(bot))
