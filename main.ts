// GTA 6 clipper entry (Node 22, standard library only).
//
// The entry itself is a YouTube Short: this agent cut a GTA 6 moment into a
// vertical clip (clip.mp4 in this repository), the clip goes up on the
// person's channel as a public Short, and VIDEO.json at the repository root
// names that video. The house reads the video's views straight from YouTube,
// so this program only has to hand the gate the address: it copies VIDEO.json
// from the repository into the output directory, byte for byte, and prints
// nothing when that works.
//
// VIDEO.json ships here as a placeholder. Before submitting, replace its url
// with the published Short's address (https://www.youtube.com/shorts/<id>);
// until then the gate refuses the entry, which is expected. The clip file
// itself is deliberately not copied to /output: the gate never reads it.
//
// Deterministic: the same VIDEO.json always produces the same output bytes,
// so two runs write identical files.
//
// Run the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const repoDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = join(repoDir, 'VIDEO.json');
const target = join(outDir, 'VIDEO.json');

mkdirSync(outDir, { recursive: true });

let payload: Buffer;
try {
  payload = readFileSync(source);
} catch (err) {
  console.error(`cannot read VIDEO.json from ${repoDir}: ${(err as Error).message}`);
  process.exit(1);
}

try {
  writeFileSync(target, payload);
} catch (err) {
  console.error(`cannot write VIDEO.json to ${outDir}: ${(err as Error).message}`);
  process.exit(1);
}
