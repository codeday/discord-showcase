/* eslint-disable no-await-in-loop */
/* eslint-disable sonarjs/no-duplicate-string */
/* eslint-disable @typescript-eslint/no-non-null-assertion */
/* eslint-disable sonarjs/no-identical-functions */
import { SlashCommandSubcommandBuilder } from '@discordjs/builders';
import { CacheType, CommandInteraction } from 'discord.js';
import debugFactory from 'debug';
import { membersInChannel, projectCreated } from '../../gql';
import prisma from '../../prisma';
import { requireTeamSupport, assignProject } from '../../utils';

const DEBUG = debugFactory('showcase.discord.commands.merge');

export const channels = [
  (new SlashCommandSubcommandBuilder())
    .setDescription('Checks in with all teams')
    .addChannelOption((option) => option
      .setName('from')
      .setDescription('Channel to merge teams from')
      .setRequired(true))
    .addChannelOption((option) => option
      .setName('to')
      .setDescription('Channel to merge teams to')
      .setRequired(true)),
  async (interaction: CommandInteraction<CacheType>): Promise<void> => {
    requireTeamSupport(interaction);
    const fromId = interaction.options.getChannel('from')!.id;
    const toId = interaction.options.getChannel('to')!.id;

    if ((await prisma.channel.count({ where: { id: { in: [fromId, toId ] } } })) !== 2) {
      throw new Error(`Channels are not part of a pool.`);
    }

    interaction.reply('Beginning merge...');

    await prisma.welcomeMessage.deleteMany({ where: { channelId: fromId } });
    await prisma.channel.delete({ where: { id: fromId } });

    const fromTeams = (await membersInChannel(fromId)).showcase?.projects || [];

    const replyHeader = `__Merging ${ fromTeams.length} teams from <#${ fromId }> to <#${ toId }>.__`;
    interaction.editReply(replyHeader);

    DEBUG(`Merging ${fromTeams.length} teams from ${fromId} -> ${toId}.`);

    const merged = [];
    const failed = [];
    for (const team of fromTeams) {
      try {
        DEBUG(`... Re-assigning ${team.name}.`)
        await assignProject(team, toId);
        merged.push(team.name);
        DEBUG(`... Done!`);
      } catch (ex) {
        failed.push(team.name);
        DEBUG(`... Couldn't reassign.`);
      }
      interaction.editReply(
        `${replyHeader}\n**Merged:** ${merged.join(', ')}\n**Failed:** ${failed.join(', ')}`
      );
    }
    DEBUG(`Merge complete. Merged ${merged.join(', ')}, failed ${failed.join(', ')}.`);
    interaction.editReply(
      `**__Merge complete.__**\n**Merged:** ${merged.join(', ')}\n**Failed:** ${failed.join(', ')}`
    );
  },
];
