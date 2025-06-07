#!/usr/bin/env node
import { Command } from 'commander';
import { copy } from 'fs-extra';
import { join, resolve } from 'node:path';
import { existsSync } from 'node:fs';

const program = new Command();
program
  .name('acf-sparc')
  .description('Initialize a SPARC-aligned Roo Code workspace')
  .command('init [target]')
  .action(async (target = '.') => {
    const dest = resolve(process.cwd(), target);
    if (existsSync(join(dest, '.roo'))) {
      console.error('🛑 Project already contains .roo; aborting.');
      process.exit(1);
    }
    const src = join(import.meta.url.replace('file://', ''), '..', 'templates', 'base');
    await copy(src, dest, { overwrite: false });
    console.log(`✅ Roo Code SPARC scaffold created in ${dest}`);
  });

program.parse();
