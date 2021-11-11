import { Client as Discord } from 'discord.js';
import debugFactory from 'debug';
import config from '../config';
import rest from './rest';
import { handle, registerCommands } from './commands';

const DEBUG = debugFactory('showcase.discord');

const discord = new Discord({ partials: ['MESSAGE', 'REACTION'], intents: [] });
discord.on('interactionCreate', handle);
discord.on('ready', async () => {
  DEBUG('Listening on Discord');
  registerCommands();
});
discord.on('error', (error) => DEBUG(error.message));

export function registerDiscord(): void {
  discord.login(config.discord.botToken);
}

export default discord;
export { rest };
