import { REST } from '@discordjs/rest';
import config from '../config';

export default new REST({ version: '9' }).setToken(config.discord.botToken);
