import { subscriberFactory } from './client';
import {
  OnMemberAddedDocument,
  OnMemberAddedSubscription,
  OnMemberRemovedDocument,
  OnMemberRemovedSubscription,
} from './memberEvents.query';

export const memberAdded = subscriberFactory({ query: OnMemberAddedDocument });
export const memberRemoved = subscriberFactory({ query: OnMemberRemovedDocument });

export { OnMemberAddedSubscription, OnMemberRemovedSubscription };
