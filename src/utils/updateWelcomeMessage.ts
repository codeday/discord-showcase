import debugFactory from 'debug';
import discord from '../discord';
import prisma from '../prisma';
import { ProjectInformationWithMembersFragment, MemberInformationFragment, membersInChannel } from '../gql';
import { chunkStrlen } from './chunkStrlen';

const DEBUG = debugFactory('showcase.utils.updateWelcomeMessage');
const DISCORD_CHARACTER_LIMIT = 2000;

export async function updateWelcomeMessage(
  channelId?: string | null,
): Promise<void> {
  DEBUG(`Updating welcome message for ${channelId}.`);
  if (!channelId) {
    DEBUG(`... No channel to update.`);
    return;
  }

  const podData = await membersInChannel(channelId);
  if (!podData?.showcase?.projects) {
    DEBUG(`... No members in pod.`);
    return;
  }

  const channel = await discord.channels.fetch(channelId);
  if (!channel?.isText()) throw new Error(`${channelId} was not a text channel.`);

  const welcomeMessageLines = podData.showcase.projects
    .flatMap((project: ProjectInformationWithMembersFragment) => [
      `**${project.name}**`,
      ...(project.members || [])
        .map((member: MemberInformationFragment) => (
          member.account?.discordId
            ? `- <@${member.account.discordId}>`
            : `- ${member.username}`
        )),
    ]);

  const messages = chunkStrlen(welcomeMessageLines, `\n`, DISCORD_CHARACTER_LIMIT);
  const priorMessageIds = (await prisma.welcomeMessage.findMany({ where: { channelId } }))
    .map((message) => message.id);

  DEBUG(`Upserting ${messages.length} welcome messages for channel ${channelId} (was ${priorMessageIds.length}).`);

  if (messages.length <= priorMessageIds.length) { // We can edit the messages in-place
    // Edit messages
    await Promise.all(
      messages.map(async (content, i) => {
        const message = await channel.messages.fetch(priorMessageIds[i]);
        await message.edit({ allowedMentions: { users: [] }, content });
      }),
    );
    DEBUG(`... Updated first ${messages.length} old messages.`);

    // Delete extra message, if the number decreased
    const toDeleteMessageIds = priorMessageIds.slice(messages.length);
    if (toDeleteMessageIds.length > 0) {
      await Promise.all(toDeleteMessageIds.map((messageId) => channel.messages.delete(messageId)));
      await prisma.welcomeMessage.deleteMany({ where: { id: { in: toDeleteMessageIds } } });
      DEBUG(`... Deleted ${toDeleteMessageIds.length} unneeded messages.`);
    }
  } else { // Need to delete and create new messages as it's grown longer and we want to keep it together
    await Promise.all(priorMessageIds.map((messageId) => channel.messages.delete(messageId)));
    await prisma.welcomeMessage.deleteMany({ where: { channelId } });
    DEBUG(`... Deleted ${priorMessageIds.length} old welcome messages.`);

    const discordMessages = await Promise.all(
      messages.map(async (content) => {
        const message = await channel.send({ allowedMentions: { users: [] }, content });
        await message.pin();
        return message;
      }),
    );
    await prisma.channel.update({
      where: { id: channelId },
      data: {
        welcomeMessages: { createMany: { data: discordMessages.map((m) => ({ id: m.id })) } },
      },
    });
    DEBUG(`... Created ${messages.length} new messages.`);
  }
}
