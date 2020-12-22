import discord
from discord.ext import commands, tasks

from cogs.pods import Pods
from db.models import session_creator
from services.gqlservice import GQLService
from services.podservice import PodService
from utils.subscriptions import subscribe


class ListenCog(commands.Cog, name="Listen"):
    """Listen to showcase api for team updates"""

    def __init__(self, bot):
        self.bot = bot
        self.on_project_created.start(self)
        self.on_project_member_added.start(self)
        self.on_project_member_removed.start(self)
        self.on_project_edited.start(self)

    def cog_unload(self):
        self.on_project_created.stop()
        self.on_project_member_added.stop()
        self.on_project_member_removed.stop()
        self.on_project_edited.stop()

    @subscribe(GQLService.team_created_listener)
    async def on_project_created(self, project):
        await Pods.assign_pods_helper(self.bot)

    @subscribe(GQLService.member_added_listener)
    async def on_project_member_added(self, member_with_project):
        await Pods.add_or_remove_user_to_pod_tc(self.bot, member_with_project, False)

    @subscribe(GQLService.member_removed_listener)
    async def on_project_member_removed(self, member_with_project):
        await Pods.add_or_remove_user_to_pod_tc(self.bot, member_with_project, True)

    @subscribe(GQLService.team_edited_listener)
    async def on_project_edited(self, project):
        pass

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
                    await GQLService.send_team_reacted(str(team_that_reacted.id), str(showcase_user.username),
                                                       float(self.emoji_to_value(payload.emoji)))
            session.commit()
            session.close()

    @staticmethod
    def emoji_is_valid(emoji):
        return emoji == "😀" or emoji == "😐" or emoji == "☹"

    @staticmethod
    def emoji_to_value(emoji):
        emoji_values = {
            "😀": 1,
            "😐": 0,
            "☹": -1
        }
        return emoji_values.get(emoji)


def setup(bot):
    bot.add_cog(ListenCog(bot))
