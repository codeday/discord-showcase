/* eslint-disable sonarjs/no-duplicate-string */
/* eslint-disable @typescript-eslint/no-non-null-assertion */
/* eslint-disable sonarjs/no-identical-functions */
import { SlashCommandSubcommandBuilder } from '@discordjs/builders';
import { CacheType, CommandInteraction } from 'discord.js';
import debugFactory from 'debug';
import prisma from '../../prisma';
import discord from '..';
import { requireTeamSupport } from '../../utils';

const DEBUG = debugFactory('showcase.discord.commands.broadcast');
export const send = [
  (new SlashCommandSubcommandBuilder())
    .setDescription('Sends a message to all teams.')
    .addStringOption((option) => option
      .setName('message')
      .setDescription('Message to send')
      .setRequired(true))
    .addStringOption((option) => option
      .setName('pool')
      .setDescription('Unique pool ID')
      .setRequired(false)),
  async (interaction: CommandInteraction<CacheType>): Promise<void> => {
    requireTeamSupport(interaction);
    const channels = await prisma.channel.findMany({
      where: { poolId: interaction.options.getString('pool') ?? undefined },
    });
    const message = interaction.options.getString('message');
    DEBUG(`Sending to ${channels.length} channels: ${message}`);
    for (const channel of channels) {
      // eslint-disable-next-line no-await-in-loop
      const discordChannel = await discord.channels.fetch(channel.id);
      if (discordChannel?.isText()) {
        // eslint-disable-next-line no-await-in-loop
        await discordChannel.send(`${message}\n@everyone`);
      }
    }
  },
];
