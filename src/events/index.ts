/* eslint-disable @typescript-eslint/no-var-requires */
/* eslint-disable @typescript-eslint/ban-types */
/* eslint-disable global-require */
/* eslint-disable import/no-dynamic-require */
import fs from 'fs';
import debugFactory from 'debug';

const DEBUG = debugFactory('showcase.events');

const handlers = fs.readdirSync(__dirname)
  .filter((name: string): boolean => name !== 'index.ts')
  .flatMap((name) => {
    const [basename] = name.split('.');
    DEBUG(`Found handlers group ${basename}.`);
    const exported = require(`./${name}`);
    DEBUG(`... Imported ${basename}.`);
    Object.keys(exported).forEach((handlerName) => DEBUG(`... Found handler ${handlerName}`));
    return <Function[]>Object.values(exported);
  });

export function registerEventHandlers(): void {
  DEBUG(`Registering ${handlers.length} handlers`);
  handlers.forEach((handler) => handler());
  DEBUG(`Handlers registered.`);
}
