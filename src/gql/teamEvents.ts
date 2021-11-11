import { subscriberFactory } from './client';
import {
  OnProjectCreatedDocument,
  OnProjectCreatedSubscription,
  OnProjectEditedDocument,
  OnProjectEditedSubscription,
  OnProjectDeletedDocument,
  OnProjectDeletedSubscription,
} from './teamEvents.query';

export const projectCreated = subscriberFactory({ query: OnProjectCreatedDocument });
export const projectEdited = subscriberFactory({ query: OnProjectEditedDocument });
export const projectDeleted = subscriberFactory({ query: OnProjectDeletedDocument });

export { OnProjectCreatedSubscription, OnProjectEditedSubscription, OnProjectDeletedSubscription };
