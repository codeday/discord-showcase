import debugFactory from 'debug';
import { ProjectInformationFragment } from '../gql';
import prisma from '../prisma';

const DEBUG = debugFactory('showcase.utils.getBestPodChannel');

export async function getBestPodChannel(project: ProjectInformationFragment): Promise<string | null> {
  if (project.podChannel) throw new Error(`${project.name} already has a team.`);

  DEBUG(
    `Finding a pool for ${project.name}`
    + ` (e=${project.eventId},g=${project.eventGroupId},r=${project.regionId},p=${project.programId})`
  );

  const availablePools = await prisma.poolInclusionCriteria.findMany({
    where: {
      OR: [
        { eventGroupId: null, eventId: null, regionId: null, programId: null },
        ...(project.eventGroupId ? [{ eventGroupId: project.eventGroupId }] : []),
        ...(project.eventId ? [{ eventId: project.eventId }] : []),
        ...(project.programId ? [{ programId: project.programId }] : []),
        ...(project.regionId ? [{ eventGroupId: project.regionId }] : []),
      ],
      pool: { channels: { some: {} } },
    },
    include: { pool: { include: { channels: { orderBy: { teamCount: 'asc' } } } } },
  });
  DEBUG(`... ${availablePools.length} available.`);


  const bestPools = availablePools
    .filter((e) => {
      if (e.eventId && e.eventId !== project.eventId) return false;
      if (e.eventGroupId && e.eventGroupId !== project.eventGroupId) return false;
      if (e.programId && e.programId !== project.programId) return false;
      if (e.regionId && e.regionId !== project.regionId) return false;
      return true;
    })
    .sort((a, b) => {
      if (a.eventId && !b.eventId) return -1;
      if (b.eventId && !a.eventId) return 1;
      if (a.eventGroupId && !b.eventGroupId) return -1;
      if (b.eventGroupId && !a.eventGroupId) return 1;
      if (a.programId && !b.programId) return -1;
      if (b.programId && !a.programId) return 1;
      if (a.regionId && !b.regionId) return -1;
      if (b.regionId && !a.regionId) return 1;
      return -1;
    });
  DEBUG(`${bestPools[0]?.id} best meets criteria.`)

  if (bestPools.length === 0) return null;

  return bestPools[0].pool.channels[0].id;
}
