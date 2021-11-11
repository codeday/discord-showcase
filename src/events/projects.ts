import debugFactory from 'debug';
import discord from '../discord';
import { MemberInformationFragment, projectCreated, projectDeleted, projectEdited } from '../gql';
import prisma from '../prisma';
import { assignProject, isPodChannelCurrent, updateWelcomeMessage } from '../utils';

const DEBUG = debugFactory('showcase.events.projects')

export function projectCreatedHandler() {
  projectCreated(async (data) => {
    const { name, members } = data.projectCreated;

    DEBUG(`Project ${name} was created. `);
    const podChannel = await assignProject(data.projectCreated);
    if (!podChannel) {
      DEBUG(`... Not in any current pool.`);
      return;
    }
  });
}

export function projectDeletedHandler() {
  projectDeleted(async (data) => {
    const { name, podChannel } = data.projectDeleted;
    if (!podChannel || !isPodChannelCurrent(podChannel)) return;

    DEBUG(`Project ${name} was deleted (pod ${podChannel})`);
    await updateWelcomeMessage(podChannel);
    await prisma.channel.update({
      where: { id: podChannel },
      data: {
        teamCount: { decrement: 1 },
      },
    });
    DEBUG(`...Updated team count.`);
  });
}
