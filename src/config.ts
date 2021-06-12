/* eslint-disable node/no-process-env */
import { config as loadEnv } from 'dotenv';

loadEnv();

[
  'DISCORD_BOT_TOKEN',
  'DISCORD_GUILD_ID',
  'DISCORD_POD_CATEGORY_ID',
  'DISCORD_TEAM_SUPPORT_CHANNEL_ID',
  'SHOWCASE_AUDIENCE',
  'SHOWCASE_SECRET',
  'SHOWCASE_EVENT_GROUP_ID',
].forEach((e) => {
  if (!process.env[e]) throw Error(`The environment variable ${e} is required.`);
})

const config = {
  debug: process.env.NODE_ENV !== 'production',
  discord: {
    botToken: process.env.DISCORD_BOT_TOKEN!,
    guildId: process.env.DISCORD_GUILD_ID!,
    podCategoryId: process.env.DISCORD_POD_CATEGORY_ID!,
    teamSupportChannelId: process.env.DISCORD_TEAM_SUPPORT_CHANNEL_ID!,
  },
  showcase: {
    audience: process.env.SHOWCASE_AUDIENCE!,
    secret: process.env.SHOWCASE_SECRET!,
    eventGroupId: process.env.SHOWCASE_EVENT_GROUP_ID!,
  },
  graphQl: {
    http: process.env.GRAPHQL_HTTP || 'https://graph.codeday.org/',
    ws: process.env.GRAPHQL_WS || 'ws://graph.codeday.org/',
  },
};

export default config;
