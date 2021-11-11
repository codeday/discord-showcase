import { Pool, PoolInclusionCriteria, Channel } from '@prisma/client';
import debugFactory from 'debug';
import { projectsWhere, ProjectInformationWithMembersFragment, MemberInformationFragment } from '../gql';
import prisma from '../prisma';
import discord from '../discord';
import { buildShowcaseInclusionFilter, assignProject } from '../utils';
import { TextChannel } from 'discord.js';
import config from '../config';

type DeepPool = Pool & { inclusionCriteria: PoolInclusionCriteria[], channels: Channel[]};

const DEBUG = debugFactory('showcase.sync');
const SYNC_INTEVAL = 60 * 60 * 30 * 1000;
let syncRunning = false;

export async function syncPool(pool: DeepPool): Promise<void> {
  DEBUG(`Syncing ${pool.id}.`);
  let projects: ProjectInformationWithMembersFragment[] = [];
  for (const poolCriteria of pool.inclusionCriteria) {
    const existingIds = projects.map((p) => p.id);
    const where = buildShowcaseInclusionFilter(poolCriteria);
    const addProjects: ProjectInformationWithMembersFragment[] = (await projectsWhere(where))
      .showcase.projects;
    projects.push(...addProjects.filter((p) => !existingIds.includes(p.id)));
  }
  DEBUG(`...Found ${projects.length} projects in this criteria.`);

  for (const project of projects) {
    DEBUG(`... Validating ${project.name}`)
    if (!project.podChannel) {
      DEBUG(`...... ${project.name} matches with no channel assignment.`);
      await assignProject(project);
    } else {
      DEBUG(`...... Checking members.`);
      const discordChannel = await discord.channels.fetch(project.podChannel);
      if (!discordChannel || !discordChannel.isText()) DEBUG(`......... ${project.podChannel} doesn't exist.`);
      const permissions = (discordChannel as TextChannel).permissionOverwrites.valueOf();

      // Check each member for permissions
      for (const member of project.members as MemberInformationFragment[]) {
        if (!member.account.discordId) {
          DEBUG(`......... ${member.username} has no linked Discord account.`);
        }
        if (!permissions.has(member.account.discordId)) {
          DEBUG(`......... Adding permissions for ${member.username} in ${project.podChannel}.`);
          const user = await discord.users.fetch(member.account.discordId);
          try {
            await (discordChannel as TextChannel).permissionOverwrites
              .create(user, config.discord.defaultMemberPermissions);
          } catch (ex) {
            DEBUG(`............ Failed.`);
          }
        }
      }
    }
  }
}

export async function syncAll(): Promise<void> {
  if (syncRunning) return;
  syncRunning = true;
  DEBUG('Starting full sync.');

  const pools = await prisma.pool.findMany({
    where: { enabled: true },
    include: { inclusionCriteria: true, channels: true },
  });

  for (const pool of pools) {
    await syncPool(pool);
  }

  DEBUG('Full sync complete.');
  syncRunning = false;
}

export function registerSync(): void {
  const syncAndReschedule = async () => { await syncAll(); setTimeout(syncAndReschedule, SYNC_INTEVAL); }
  syncAndReschedule();
}

