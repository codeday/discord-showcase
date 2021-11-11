// https://stackoverflow.com/a/29202760/154044
function chunkSubstr(str: string, size: number): string[] {
  const numChunks = Math.ceil(str.length / size);
  const chunks = new Array(numChunks);

  // eslint-disable-next-line no-plusplus
  for (let i = 0, o = 0; i < numChunks; ++i, o += size) {
    chunks[i] = str.substr(o, size);
  }

  return chunks;
}

export function chunkStrlen(messages: string[], join: string, maxLength: number): string[] {
  const chunks: string[] = [];
  for (const message of messages) {
    const i = chunks.length - 1;
    if (chunks.length === 0 || chunks[i].length + join.length + message.length > maxLength) {
      if (message.length > maxLength) {
        chunks.push(...chunkSubstr(message, maxLength));
      } else {
        chunks.push(message);
      }
    } else {
      chunks[i] = chunks[i] + join + message;
    }
  }

  return chunks;
}
