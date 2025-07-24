/**
 * Environment Setup Script
 * 
 * This script copies the env.example file to .env if it doesn't exist.
 * Run with: node scripts/setup-env.js
 */

const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

const rootDir = path.join(__dirname, '..');
const envExamplePath = path.join(rootDir, 'env.example');
const envPath = path.join(rootDir, '.env');

// Check if .env file already exists
if (fs.existsSync(envPath)) {
  console.log(chalk.yellow('⚠️  .env file already exists. Skipping setup.'));
  console.log(chalk.blue('ℹ️  If you want to reset to defaults, delete the .env file and run this script again.'));
  process.exit(0);
}

// Check if env.example file exists
if (!fs.existsSync(envExamplePath)) {
  console.log(chalk.red('❌ env.example file not found. Cannot set up environment.'));
  process.exit(1);
}

try {
  // Copy env.example to .env
  fs.copyFileSync(envExamplePath, envPath);
  console.log(chalk.green('✅ Successfully created .env file from env.example'));
  console.log(chalk.blue('ℹ️  Please edit the .env file to add your API keys.'));
  
  // Read the .env file content
  const envContent = fs.readFileSync(envPath, 'utf8');
  console.log('\n' + chalk.underline('Current .env file:'));
  console.log(envContent);
  
  console.log('\n' + chalk.yellow('⚠️  Remember to add your actual API keys to the .env file.'));
} catch (error) {
  console.error(chalk.red(`❌ Error creating .env file: ${error.message}`));
  process.exit(1);
} 