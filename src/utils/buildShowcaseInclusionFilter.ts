import { PoolInclusionCriteria } from '@prisma/client';

export function buildShowcaseInclusionFilter(criteria: PoolInclusionCriteria) {
  return {
    eventGroup: criteria.eventGroupId ?? undefined,
    event: criteria.eventId ?? undefined,
    region: criteria.regionId ?? undefined,
    program: criteria.programId ?? undefined,
  };
}
