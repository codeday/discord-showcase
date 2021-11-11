import debugFactory from 'debug';
import { TextChannel } from 'discord.js';
import { ProjectInformationWithMembersFragment, MemberInformationFragment, setProjectChannel } from '../gql';
import discord from '../discord';
import prisma from '../prisma';
import config from '../config';
import { getBestPodChannel } from './getBestPodChannel';
import { updateWelcomeMessage } from './updateWelcomeMessage';

const DEBUG = debugFactory('showcase.utils.assignProject');

export async function assignProject(
  project: ProjectInformationWithMembersFragment,
  forcePodChannel?: string,
): Promise<string | null> {
  DEBUG(`Assigning project ${project.name} to a pool and pod channel.`);

  const podChannel = forcePodChannel ? forcePodChannel : await getBestPodChannel(project);
  DEBUG(`... Pod channel assignment: ${podChannel}`);
  if (!podChannel) return null;

  const discordChannel = await discord.channels.fetch(podChannel);
  if (!discordChannel?.isText()) return null;

  await setProjectChannel(project.id, podChannel);
  DEBUG(`... Set pod channel metadata.`);

  for (const member of project.members as MemberInformationFragment[]) {
    try {
      if (!member.account?.discordId) throw new Error('No discord ID');
      const user = (await discord.users.fetch(member.account.discordId));
      await (discordChannel as TextChannel).permissionOverwrites.create(user, config.discord.defaultMemberPermissions);
      DEBUG(`... Added permissions for ${member.username} (${member.account.discordId}).`);
    } catch (ex) {
      DEBUG(`... Could not add permissions for ${member.username} (${member?.account?.discordId}).`);
    }
  }

  await prisma.channel.update({
    where: { id: podChannel },
    data: {
      teamCount: { increment: 1 },
    },
  });
  DEBUG('... Updated channel capacity.');

  await updateWelcomeMessage(podChannel);


  const tags = (project.members as MemberInformationFragment[])
    .map((m) => m.account?.discordId ? `<@${m.account.discordId}>` : m.username)
    .join(',');
  discordChannel.send(`Project **${project.name}** has joined! ${tags}`);
  return podChannel;
}
