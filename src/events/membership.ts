import debugFactory from 'debug';
import { TextChannel } from 'discord.js';
import config from '../config';
import discord from '../discord';
import { memberAdded, memberRemoved } from '../gql';
import { updateWelcomeMessage, isPodChannelCurrent } from '../utils';

const DEBUG = debugFactory('showcase.events.membership');

export function memberAddedHandler() {
  memberAdded(async (data) => {
    const { username, account, project } = data.memberAdded;
    const { name, podChannel } = project;
    if (!isPodChannelCurrent(podChannel)) return;

    const discordChannel = await discord.channels.fetch(podChannel);
    if (!discordChannel?.isText() || !account.discordId) return;

    DEBUG(`Member ${username} (discord ${account?.discordId}) joined project ${name} (pod ${podChannel})`);

    if (!account.discordId) {
      DEBUG(`... No Discord ID.`);
      return;
    }

    await updateWelcomeMessage(podChannel);

    try {
      const user = (await discord.users.fetch(account.discordId));
      await (discordChannel as TextChannel).permissionOverwrites.create(user, config.discord.defaultMemberPermissions);
      DEBUG(`... Added permissions for ${username} (${account.discordId}).`);
    } catch (ex) {
      DEBUG(`... Could not add permissions for ${username} (${account.discordId}).`);
    }

    await discordChannel.send(`<@${account.discordId}> joined ${project.name}. Welcome!`);
  });
}

export function memberRemovedHandler() {
  memberRemoved(async (data) => {
    const { username, account, project } = data.memberRemoved;
    const { name, podChannel } = project;
    if (!isPodChannelCurrent(podChannel)) return;

    DEBUG(`Member ${username} (discord ${account?.discordId}) left project ${name} (pod ${podChannel})`);
    await updateWelcomeMessage(podChannel);
  });
}
