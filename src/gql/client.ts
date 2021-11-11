import { print } from 'graphql';
import { GraphQLClient } from 'graphql-request';
import debugFactory from 'debug';
import WebSocket from 'ws';
import { TypedDocumentNode } from '@graphql-typed-document-node/core';
import { WebSocketLink } from '@apollo/client/link/ws';
import { ApolloClient, InMemoryCache } from '@apollo/client/core';
import config from '../config';
import { getToken } from './token';

const DEBUG = debugFactory('showcase.gql');
const DEBUG_REQ = debugFactory('req');

const wsLink = new WebSocketLink({
  uri: config.graphQl.ws,
  options: {
    reconnect: true
  },
  webSocketImpl: WebSocket,
});

const apolloSubscriptionsClient = new ApolloClient({
  link: wsLink,
  cache: new InMemoryCache(),
});

type QueryAst<T, V> = { query: TypedDocumentNode<T>, variables?: V };
type Handlers<T> = { onData(data: T): Promise<void> };

export function subscribe<T, V>(
  {
    query, variables, onData, ...rest
  }: QueryAst<T, V> & Handlers<T>,
): void {
  const queryOperation = query.definitions
    .filter((d) => d.kind === 'OperationDefinition')[0] as { name?: { value?: string } } | undefined;
  const queryName = queryOperation?.name?.value;

  DEBUG(`Subscription started for query ${queryName}`);
  apolloSubscriptionsClient
    .subscribe({ query, variables })
    .subscribe({
      next(data) {
        if (data.data) {
          DEBUG_REQ(data.data);
          onData(data.data);
        } else {
          DEBUG(`Error in query ${queryName}: ${data.errors?.map((e) => e.message).join(',')}`)
        }
      },
    });
}

export function subscriberFactory<T, V>(opt: QueryAst<T, V>): (fn: (data: T) => Promise<void>) => void {
  type SubType = (data: T) => Promise<void>;
  const subscribers: SubType[] = [];
  subscribe({
    ...opt,
    async onData(data: T) {
      subscribers.forEach((fn) => fn(data));
    },
  });
  return (fn: SubType): void => { subscribers.push(fn); };
}

export function request<T, V>({ query, variables }: QueryAst<T, V>): Promise<T> {
  const httpClient = new GraphQLClient(config.graphQl.http, {
    headers: {
      'X-Showcase-Authorization': `Bearer ${getToken()}`,
    },
  });
  DEBUG_REQ({ query: print(query), variables });
  return httpClient.request<T, V>(query, variables);
}
