/* eslint-disable node/no-process-env */
import { config as loadEnv } from 'dotenv';

loadEnv();

[
  'DATABASE_URL',
  'DISCORD_CLIENT_ID',
  'DISCORD_BOT_TOKEN',
  'DISCORD_GUILD_ID',
  'DISCORD_TEAM_SUPPORT_CHANNEL_ID',
  'SHOWCASE_AUDIENCE',
  'SHOWCASE_SECRET',
].forEach((e) => {
  if (!process.env[e]) throw Error(`The environment variable ${e} is required.`);
});

const config = {
  debug: process.env.NODE_ENV !== 'production',
  discord: {
    clientId: process.env.DISCORD_CLIENT_ID!,
    botToken: process.env.DISCORD_BOT_TOKEN!,
    guildId: process.env.DISCORD_GUILD_ID!,
    teamSupportChannelId: process.env.DISCORD_TEAM_SUPPORT_CHANNEL_ID!,
    checkinEmoji: {
      good: '🥳',
      neutral: '😕',
      bad: '😓',
    },
    defaultMemberPermissions: {
      VIEW_CHANNEL: true,
      READ_MESSAGE_HISTORY: true,
      SEND_MESSAGES: true,
      EMBED_LINKS: true,
      ATTACH_FILES: true,
      ADD_REACTIONS: true,
    },
  },
  showcase: {
    audience: process.env.SHOWCASE_AUDIENCE!,
    secret: process.env.SHOWCASE_SECRET!,
  },
  graphQl: {
    http: process.env.GRAPHQL_HTTP || 'https://graph.codeday.org/',
    ws: process.env.GRAPHQL_WS || 'ws://graph.codeday.org/subscriptions',
  },
};

export default config;
