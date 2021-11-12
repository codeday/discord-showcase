import { request } from './client';
import {
  MembersInChannelQuery,
  MembersInChannelDocument,
  MembersInChannelQueryVariables,
  ProjectsWhereQuery,
  ProjectsWhereDocument,
  ProjectsWhereQueryVariables,
  ProjectByIdQuery,
  ProjectByIdDocument,
  ProjectByIdQueryVariables,
  ShowcaseProjectsWhere,
  SetProjectChannelMutation,
  SetProjectChannelDocument,
  SetProjectChannelMutationVariables,
} from './queries.query';

export const membersInChannel = (channel: string) =>
  request<MembersInChannelQuery, MembersInChannelQueryVariables>({
    query: MembersInChannelDocument,
    variables: { channel },
  });

export const setProjectChannel = (project: string, channel: string) =>
  request<SetProjectChannelMutation, SetProjectChannelMutationVariables>({
    query: SetProjectChannelDocument,
    variables: { project, channel },
  });

export const projectsWhere = (where: ShowcaseProjectsWhere) =>
  request<ProjectsWhereQuery, ProjectsWhereQueryVariables>({
    query: ProjectsWhereDocument,
    variables: { where },
  });

export const projectById = (id: string) =>
  request<ProjectByIdQuery, ProjectByIdQueryVariables>({
    query: ProjectByIdDocument,
    variables: { id },
  });

export { MembersInChannelQuery, SetProjectChannelMutation, ProjectsWhereDocument, ProjectByIdDocument };
