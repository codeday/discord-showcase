import { sign } from 'jsonwebtoken';
import config from '../config';

const LIFETIME = 60 * 60 * 24 * 5;

function makeToken(): string {
  return sign({ a: true }, config.showcase.secret, { audience: config.showcase.audience, expiresIn: LIFETIME });
}

let token = makeToken();
setInterval(() => { token = makeToken(); }, LIFETIME / 2);

export function getToken(): string {
  return token;
}
