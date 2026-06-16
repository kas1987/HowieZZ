import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';

const ROOT = process.cwd();
const MARKDOWN_SUFFIX = '.md';
const TASK_ID_PATTERN = /^\s*-?\s*task_id\s*:/im;
const PDR_PATH_PATTERN = /^\s*-?\s*pdr_path\s*:\s*(.+)$/gim;

const SCAN_DIRS = [
  'docs/handoffs',
  'docs/pdr/recovery-pack'
];

const REQUIRED_TASK_FILES = [
  'AGENTS.md',
  'CLAUDE.md',
  'CODEX.md'
];

let failures = 0;

function walkMarkdownFiles(dirPath, out) {
  if (!existsSync(dirPath)) return;
  for (const entry of readdirSync(dirPath)) {
    const fullPath = join(dirPath, entry);
    const stats = statSync(fullPath);
    if (stats.isDirectory()) {
      walkMarkdownFiles(fullPath, out);
    } else if (stats.isFile() && fullPath.toLowerCase().endsWith(MARKDOWN_SUFFIX)) {
      out.push(fullPath);
    }
  }
}

function getPdrPaths(content) {
  const matches = [];
  for (const match of content.matchAll(PDR_PATH_PATTERN)) {
    const pathValue = (match[1] || '').trim().replace(/^`|`$/g, '');
    if (pathValue.length > 0) {
      matches.push(pathValue);
    }
  }
  return matches;
}

function validateTaskFile(filePath) {
  const rel = relative(ROOT, filePath).replace(/\\/g, '/');
  const content = readFileSync(filePath, 'utf8');

  if (!TASK_ID_PATTERN.test(content)) return;

  const pdrPaths = getPdrPaths(content);
  if (pdrPaths.length === 0) {
    console.error(`ERROR ${rel}: task file has task_id but no pdr_path`);
    failures += 1;
    return;
  }

  for (const pdrPath of pdrPaths) {
    const resolved = join(ROOT, pdrPath);
    if (!existsSync(resolved)) {
      console.error(`ERROR ${rel}: pdr_path does not exist -> ${pdrPath}`);
      failures += 1;
    }
  }
}

function validateRequiredTaskDocs() {
  for (const relPath of REQUIRED_TASK_FILES) {
    const fullPath = join(ROOT, relPath);
    if (!existsSync(fullPath)) {
      console.error(`ERROR ${relPath}: required policy file is missing`);
      failures += 1;
      continue;
    }

    const content = readFileSync(fullPath, 'utf8');
    if (!/PDR_PATH/i.test(content)) {
      console.error(`ERROR ${relPath}: missing PDR_PATH policy text`);
      failures += 1;
    }
  }
}

function main() {
  console.log('Running PDR_PATH task-file guard...');

  validateRequiredTaskDocs();

  const markdownFiles = [];
  for (const dir of SCAN_DIRS) {
    walkMarkdownFiles(join(ROOT, dir), markdownFiles);
  }

  for (const filePath of markdownFiles) {
    validateTaskFile(filePath);
  }

  if (failures > 0) {
    console.error(`PDR_PATH validation failed with ${failures} error(s).`);
    process.exit(1);
  }

  console.log('PDR_PATH guard passed.');
}

main();
