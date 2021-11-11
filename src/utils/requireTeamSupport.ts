import { CacheType, CommandInteraction } from 'discord.js';
import config from '../config';

export function requireTeamSupport(interaction: CommandInteraction<CacheType>): void {
  if (interaction.channelId !== config.discord.teamSupportChannelId) {
    interaction.reply(`Sorry, you can't do that here.`);
    throw new Error('Command not in correct channel.');
  }
}
