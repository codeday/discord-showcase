import { Client as Discord } from 'discord.js';
import config from '../config';

export const discord = new Discord({ partials: ['MESSAGE', 'REACTION'] });
// eslint-disable-next-line no-console
discord.on('ready', () : void => console.log('Listening on Discord'));
discord.login(config.discord.botToken);
