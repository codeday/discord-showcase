import 'reflect-metadata';
import { registerEventHandlers } from './events';
import { registerDiscord } from './discord';
import { registerSync } from './sync';

registerEventHandlers();
registerDiscord();
registerSync();
