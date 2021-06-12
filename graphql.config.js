/* eslint-disable */
const { sign } = require('jsonwebtoken');

require('dotenv').config({ path: `.env` });

const token = sign(
  { a: true },
  process.env.SHOWCASE_SECRET,
  { audience: process.env.SHOWCASE_AUDIENCE, expiresIn: '1h' }
);

module.exports = {
  schema: "schema.graphql",
  documents: "src/**/*.gql",
  extensions: {
    endpoints: {
      default: {
        url: `https://graph.codeday.org/`,
        headers: {
          'X-Showcase-Authorization': `Bearer ${token}`,
        }
      }
    }
  }
}
