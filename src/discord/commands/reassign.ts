/* eslint-disable no-await-in-loop */
/* eslint-disable sonarjs/no-duplicate-string */
/* eslint-disable @typescript-eslint/no-non-null-assertion */
/* eslint-disable sonarjs/no-identical-functions */
import { SlashCommandSubcommandBuilder } from '@discordjs/builders';
import { CacheType, CommandInteraction, TextChannel } from 'discord.js';
import debugFactory from 'debug';
import { membersInChannel, projectById, projectCreated } from '../../gql';
import prisma from '../../prisma';
import { requireTeamSupport, assignProject } from '../../utils';
import discord from '..';

const DEBUG = debugFactory('showcase.discord.commands.reassign');

export const team = [
  (new SlashCommandSubcommandBuilder())
    .setDescription('Moves a team')
    .addStringOption((option) => option
      .setName('team')
      .setDescription('Showcase ID')
      .setRequired(true))
    .addChannelOption((option) => option
      .setName('to')
      .setDescription('Channel to move teams to')
      .setRequired(true)),
  async (interaction: CommandInteraction<CacheType>): Promise<void> => {
    requireTeamSupport(interaction);
    const projectId = interaction.options.getString('team')!;
    const toId = interaction.options.getChannel('to')!.id;

    if ((await prisma.channel.count({ where: { id: toId } })) !== 1) {
      throw new Error(`Channel is not part of a pool.`);
    }

    interaction.reply('Ok.');

    const team = (await projectById(projectId!)).showcase?.project;
    if (!team) {
      throw new Error(`Team does not exist.`);
    }

    if (team?.podChannel) {
      const discordFromChannel = await discord.channels.fetch(team.podChannel);
      await (discordFromChannel as TextChannel).send(`${team.name} is being moved to another pod.`);
      const discordMembers = (team.members || []).filter((member) => member.account?.discordId);
      for (const member of discordMembers) {
        try {
          const user = (await discord.users.fetch(member.account.discordId));
          await (discordFromChannel as TextChannel).permissionOverwrites.delete(user);
        } catch (ex) {}
      }
    }

    await assignProject(team, toId);
  },
];
