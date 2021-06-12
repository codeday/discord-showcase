import { print } from 'graphql';
import { GraphQLClient } from 'graphql-request';
import WebSocket from 'ws';
import { TypedDocumentNode } from '@graphql-typed-document-node/core';
import { createClient, SubscribePayload } from 'graphql-ws';
import config from '../config';
import { getToken } from './token';

const subscriptionsClient = createClient({
  url: config.graphQl.ws,
  lazy: true,
  webSocketImpl: WebSocket,
});

type QueryAst<T, V> = { query: TypedDocumentNode<T>, variables?: V };
type Handlers<T> = { onData(data: T): Promise<void> };
type SubscriberOpt<T, V> = Omit<SubscribePayload, 'query' | 'variables'> & QueryAst<T, V>;

export function subscribe<T, V>(
  {
    query, variables, onData, ...rest
  }: SubscriberOpt<T, V> & Handlers<T>,
): void {
  subscriptionsClient
    .subscribe({
      query: print(query),
      variables: <Record<string, unknown>> variables,
      ...rest,
    }, {
      next(data) { onData(<T>data); },
      // eslint-disable-next-line no-console
      error: console.error,
      // eslint-disable-next-line no-console
      complete: console.debug,
    });
}

export function subscriberFactory<T, V>(opt: SubscriberOpt<T, V>): (fn: (data: T) => Promise<void>) => void {
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
  return httpClient.request<T, V>(print(query), variables);
}
