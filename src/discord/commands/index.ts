/* eslint-disable @typescript-eslint/no-var-requires */
/* eslint-disable @typescript-eslint/ban-types */
/* eslint-disable global-require */
/* eslint-disable import/no-dynamic-require */
import fs from 'fs';
import debugFactory from 'debug';
import {
  SlashCommandBuilder,
  SlashCommandSubcommandBuilder,
  SlashCommandSubcommandGroupBuilder,
  SlashCommandSubcommandsOnlyBuilder,
} from '@discordjs/builders';
import { Routes } from 'discord-api-types/v9';
import { CacheType, Interaction } from 'discord.js';
import rest from '../rest';
import config from '../../config';

type SubCommandHandler = (options: Interaction<CacheType>) => Promise<void> | void;
type SubCommandRegistration = [SlashCommandSubcommandBuilder, SubCommandHandler];
type SubCommandFile = Record<string, SubCommandRegistration>;
type SubCommandGroupDetails = { group: SlashCommandSubcommandGroupBuilder, handlers: Record<string, SubCommandHandler>};
type SubCommandGroups = Record<string, SubCommandGroupDetails>;

const DEBUG = debugFactory('showcase.discord.commands');

export const allFiles: SubCommandGroups = fs.readdirSync(__dirname)
  .filter((name: string): boolean => name !== 'index.ts')
  .map((name: string) => {
    const [basename] = name.split('.');
    const file = <SubCommandFile>require(`./${name}`);
    let group = (new SlashCommandSubcommandGroupBuilder())
      .setName(basename)
      .setDescription(`Functionality related to ${basename}`);

    DEBUG(`Found command group ${basename}`);

    const handlers: Record<string, SubCommandHandler> = {};

    for (const commandName of Object.keys(file)) {
      DEBUG(`... Found command ${commandName}`);

      const [builder, handler] = file[commandName];
      group = group.addSubcommand(builder.setName(commandName));
      handlers[commandName] = handler;
    }

    return { basename, group, handlers };
  })
  .reduce((accum, { basename, ...e }): SubCommandGroups => ({ ...accum, [basename]: e }), {});

export async function registerCommands(): Promise<void> {
  let commands: SlashCommandSubcommandsOnlyBuilder = (new SlashCommandBuilder())
    .setName('showcase')
    .setDescription('Provides team help at CodeDay');
  Object.values(allFiles)
    .forEach((f) => { commands = commands.addSubcommandGroup(f.group); });

  DEBUG(`Registering command.`);
  await rest.put(
    Routes.applicationGuildCommands(config.discord.clientId, config.discord.guildId),
    { body: [commands.toJSON()] },
  );
  DEBUG(`... Registered!`);
}

export async function handle(interaction: Interaction<CacheType>): Promise<void> {
  if (!interaction.isCommand()) return;
  const groupId = interaction.options.getSubcommandGroup();
  const commandId = interaction.options.getSubcommand();
  const data = JSON.stringify(interaction.options.data);
  DEBUG(`Processing command ${groupId}.${commandId} from ${interaction.user.tag} in ${interaction.channelId}: ${data}`);

  if (!(groupId in allFiles)) { DEBUG('... group not found'); return; }
  if (!(commandId in allFiles[groupId].handlers)) { DEBUG('... command not found'); return; }

  const command = allFiles[groupId].handlers[commandId];
  try {
    await command(interaction);
    if (!interaction.replied) {
      try {
        await interaction.reply('Ok!');
      } catch (ex) {}
    }
  } catch (err) {
    DEBUG(err);
    const message = 'Sorry, something went wrong. Please ask someone to check the logs.';
    if (interaction.replied) await interaction.followUp(message);
    else interaction.reply(message);
  }
}
