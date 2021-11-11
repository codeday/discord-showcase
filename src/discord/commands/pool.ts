/* eslint-disable sonarjs/no-duplicate-string */
/* eslint-disable @typescript-eslint/no-non-null-assertion */
/* eslint-disable sonarjs/no-identical-functions */
import { SlashCommandSubcommandBuilder } from '@discordjs/builders';
import { CacheType, CommandInteraction } from 'discord.js';
import qs from 'querystring';
import debugFactory from 'debug';
import prisma from '../../prisma';
import { requireTeamSupport } from '../../utils';
import { syncPool } from '../../sync';

const DEBUG = debugFactory('showcase.discord.commands.pool');

export const create = [
  (new SlashCommandSubcommandBuilder())
    .setDescription('Creates a new pool.')
    .addStringOption((option) => option
      .setName('pool')
      .setDescription('Unique pool ID')
      .setRequired(true)),
  async (interaction: CommandInteraction<CacheType>): Promise<void> => {
    requireTeamSupport(interaction);
    const id = interaction.options.getString('pool')!;
    await prisma.pool.create({
      data: {
        id,
      },
    });

    DEBUG(`Created pool ${id}.`);
  },
];

export const remove = [
  (new SlashCommandSubcommandBuilder())
    .setDescription('Removes a pool.')
    .addStringOption((option) => option
      .setName('pool')
      .setDescription('Unique pool ID')
      .setRequired(true)),
  async (interaction: CommandInteraction<CacheType>): Promise<void> => {
    requireTeamSupport(interaction);
    const id = interaction.options.getString('pool')!;
    await prisma.poolInclusionCriteria.deleteMany({ where: { poolId: id } });
    await prisma.channel.deleteMany({ where: { poolId: id } });
    await prisma.pool.delete({
      where: {
        id,
      },
    });

    DEBUG(`Removed pool ${id}`);
  },
];

export const enable = [
  (new SlashCommandSubcommandBuilder())
    .setDescription('Enables a pool.')
    .addStringOption((option) => option
      .setName('pool')
      .setDescription('Unique pool ID')
      .setRequired(true)),
  async (interaction: CommandInteraction<CacheType>): Promise<void> => {
    requireTeamSupport(interaction);
    const id = interaction.options.getString('pool')!;
    await prisma.pool.update({
      where: { id },
      data: { enabled: true },
    });
    await interaction.reply('Ok, starting existing project sync...');

    syncPool(
      await prisma.pool.findUnique({
        where: { id },
        include: { inclusionCriteria: true, channels: true },
        rejectOnNotFound: true,
      }),
    );

    DEBUG(`Enabled ${id}`);
  },
];

export const list = [
  (new SlashCommandSubcommandBuilder())
    .setDescription('Lists all pools.'),
  async (interaction: CommandInteraction<CacheType>): Promise<void> => {
    requireTeamSupport(interaction);
    const pools = await prisma.pool.findMany({
      include: { inclusionCriteria: true, channels: true },
    });

    await interaction.reply(
      pools
        .flatMap((pool) => [
          `${pool.id}:`,
          `- Includes: \`${JSON.stringify(pool.inclusionCriteria)}\``,
          `- Channels: ${pool.channels.map((channel) => `<#${channel.id}>`).join(', ')}`,
        ])
        .join(`\n`),
    );
  },
];

export const include = [
  (new SlashCommandSubcommandBuilder())
    .setDescription('Includes criteria.')
    .addStringOption((option) => option
      .setName('pool')
      .setDescription('Unique pool ID')
      .setRequired(true))
    .addStringOption((option) => option
      .setName('criteria')
      .setDescription('Criteria to include, any combination of program, region, group, event. i.e. program=a&region=b.')
      .setRequired(true)),
  async (interaction: CommandInteraction<CacheType>): Promise<void> => {
    requireTeamSupport(interaction);
    const options = <Record<string, string | undefined>>qs.decode(interaction.options.getString('criteria')!);
    const id = interaction.options.getString('pool')!;
    const createData = {
      programId: options.program ?? undefined,
      regionId: options.region ?? undefined,
      eventGroupId: options.group ?? undefined,
      eventId: options.event ?? undefined,
    };
    await prisma.pool.update({
      where: { id },
      data: {
        inclusionCriteria: {
          create: createData,
        },
      },
    });

    DEBUG(`Added inclusion criteria ${JSON.stringify(createData)} to pool ${id}.`);
  },
];

export const addchannel = [
  (new SlashCommandSubcommandBuilder())
    .setDescription('Adds a channel in a pool.')
    .addStringOption((option) => option
      .setName('pool')
      .setDescription('Unique pool ID')
      .setRequired(true))
    .addChannelOption((option) => option
      .setName('channel')
      .setDescription('Channel to include')
      .setRequired(true)),
  async (interaction: CommandInteraction<CacheType>): Promise<void> => {
    requireTeamSupport(interaction);
    const id = interaction.options.getString('pool')!;
    const channelId = interaction.options.getChannel('channel')!.id;

    await prisma.pool.update({
      where: { id: interaction.options.getString('pool')! },
      data: {
        channels: { create: { id: channelId } },
      },
    });

    DEBUG(`Added channel ${channelId} to pool ${id}.`);
  },
];
