import prisma from '../prisma';

export async function isPodChannelCurrent(channelId?: string | null): Promise<boolean> {
  if (!channelId) return false;
  return (await prisma.channel.count({ where: { id: channelId, pool: { enabled: true } } })) > 0;
}
