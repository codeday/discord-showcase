import { ProjectInformationFragment } from '../showcase';

export interface PodInformation {
  channel: string
  name: string
  message: string
}

export async function getPodForTeam(project: ProjectInformationFragment): Promise<PodInformation> {
  const channel = project.podChannel;
  const name = project.podName;
  const message = project.podMessage;
  if (!channel) {
    // TODO(@tylermenezes) Create pod in showcase
    // TODO(@tylermenezes) Fetch
  }

  return { channel, name, message };
}
