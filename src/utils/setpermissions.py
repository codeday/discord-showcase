import discord

"""
    The purpose of this class is to set permissions for a particular showcase team, more information on discord
    permissions and setting permissions for a text channel are below.
"""

# For permissions attributes and other information, use the following links:
# https://discordpy.readthedocs.io/en/latest/api.html#discord.Permissions
# https://discordpy.readthedocs.io/en/latest/api.html#discord.TextChannel.set_permissions

class SetPermissions:

    @staticmethod
    async def for_channel_with_showcase_team(bot, text_channel, showcase_team):
        print(showcase_team["members"])
        for showcase_member in showcase_team["members"]:
            discord_id = showcase_member["account"]["discordId"]
            print(discord_id)
            try:
                member = await bot.fetch_user(discord_id)
                await text_channel.set_permissions(member, read_messages=True, read_message_history=True,
                                                   send_messages=True, embed_links=True, attach_files=True,
                                                   external_emojis=True, add_reactions=True)
            except discord.errors.NotFound:
                print("A user was not found within the server")
