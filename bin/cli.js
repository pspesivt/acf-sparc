#!/usr/bin/env node
import { Command } from 'commander';
import { copy } from 'fs-extra';
import { join, resolve, dirname } from 'node:path';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const program = new Command();
program
  .name('acf-sparc')
  .description('Initialize an ACF-SPARC-aligned Roo Code workspace')
  .command('init [target]')
  .action(async (target = '.') => {
    const dest = resolve(process.cwd(), target);
    
    // If target is not current directory, create it first
    if (target !== '.') {
      const { mkdir } = await import('fs/promises');
      await mkdir(dest, { recursive: true });
    }
    
    // Check if .roo already exists
    if (existsSync(join(dest, '.roo'))) {
      console.error('🛑 Project already contains .roo; aborting.');
      process.exit(1);
    }
    
    // Get the correct path to templates
    const packageRoot = join(__dirname, '..');
    const src = join(packageRoot, 'templates', 'base');
    
    if (!existsSync(src)) {
      console.error(`🛑 Template directory not found: ${src}`);
      process.exit(1);
    }
    
    await copy(src, dest, { overwrite: false });
    console.log(`✅ Roo Code ACF-SPARC scaffold created in ${dest}`);
  });

program.parse();
