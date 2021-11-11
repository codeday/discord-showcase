/* eslint-disable no-await-in-loop */
/* eslint-disable sonarjs/no-duplicate-string */
/* eslint-disable @typescript-eslint/no-non-null-assertion */
/* eslint-disable sonarjs/no-identical-functions */
import { SlashCommandSubcommandBuilder } from '@discordjs/builders';
import { CacheType, CommandInteraction } from 'discord.js';
import debugFactory from 'debug';
import prisma from '../../prisma';
import config from '../../config';
import { requireTeamSupport } from '../../utils';
import discord from '..';

const DEBUG = debugFactory('showcase.discord.commands.checkin');

const CHECKIN_MESSAGE = `
  Please let us know which of these emojis best represent how you're feeling right now. @everyone
`;

export const send = [
  (new SlashCommandSubcommandBuilder())
    .setDescription('Checks in with all teams')
    .addStringOption((option) => option
      .setName('pool')
      .setDescription('Unique pool ID')
      .setRequired(false)),
  async (interaction: CommandInteraction<CacheType>): Promise<void> => {
    requireTeamSupport(interaction);
    const channels = await prisma.channel.findMany({
      where: { poolId: interaction.options.getString('pool') ?? undefined },
    });
    DEBUG(`Checking in with ${channels.length} channels.`);
    interaction.reply(`Checking in with ${channels.length} channels.`);
    for (const channel of channels) {
      const discordChannel = await discord.channels.fetch(channel.id);
      // eslint-disable-next-line no-continue
      if (!discordChannel?.isText()) continue;

      const message = await discordChannel.send(CHECKIN_MESSAGE);
      await message.react(config.discord.checkinEmoji.good);
      await message.react(config.discord.checkinEmoji.neutral);
      await message.react(config.discord.checkinEmoji.bad);

      await prisma.channel.update({
        where: { id: channel.id },
        data: { latestCheckinMessageId: message.id },
      });
    }
  },
];
