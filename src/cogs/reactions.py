import discord
from discord.ext import commands

from db.models import session_creator
from services.gqlservice import GQLService
from services.podservice import PodService


class Reactions(commands.Cog, name="Reactions"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        print("on_raw_reaction_added")
        if self.emoji_is_valid(payload.emoji):
            print("is valid emoji")
            guild: discord.Guild = payload.member.guild
            session = session_creator()

            pod = PodService.get_pod_by_channel_id(
                str(payload.channel_id), session)
            if pod is not None:
                print("pod is not none")
                showcase_user = str(await GQLService.get_showcase_user_from_discord_id(str(payload.member.id)))
                team_that_reacted = await GQLService.get_showcase_team_by_showcase_user(showcase_user)
                channel: discord.DMChannel = guild.get_channel(
                    int(payload.channel_id))
                message = await channel.fetch_message(payload.message_id)
                user_who_posted_message = message.author
                print("made it here1")
                if user_who_posted_message == self.bot.user.id:
                    print("made it here2")
                    await GQLService.send_team_reacted(str(team_that_reacted.id), str(showcase_user.username),
                                                       float(self.emoji_to_value(payload.emoji)))
            session.commit()
            session.close()

    def emoji_is_valid(self, emoji):
        return emoji == "😀" or emoji == "😐" or emoji == "☹"

    def emoji_to_value(self, emoji):
        emoji_values = {
            "😀": 1,
            "😐": 0,
            "☹": -1
        }
        return emoji_values.get(emoji)


def setup(bot):
    bot.add_cog(Reactions(bot))
