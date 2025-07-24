/**
 * Environment Variable Checker
 * 
 * This script checks if all required environment variables are set.
 * Run with: node scripts/check-env.js
 */

require('dotenv').config();
const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

// Define required environment variables
const requiredVars = [
  { name: 'GEMMA_API_KEY', description: 'Google Gemma API Key' }
];

// Define optional environment variables
const optionalVars = [
  { name: 'OPENAI_API_KEY', description: 'OpenAI API Key for speech-to-text' }
];

// Check if .env file exists
const envPath = path.join(__dirname, '..', '.env');
if (!fs.existsSync(envPath)) {
  console.log(chalk.yellow('⚠️  Warning: .env file not found'));
  console.log(chalk.blue('ℹ️  Tip: Copy env.example to .env and add your API keys'));
} else {
  console.log(chalk.green('✅ .env file found'));
}

// Check required variables
let missingRequired = false;
console.log('\n' + chalk.underline('Required Environment Variables:'));

requiredVars.forEach(variable => {
  const value = process.env[variable.name];
  if (!value) {
    console.log(chalk.red(`❌ ${variable.name}: Missing (${variable.description})`));
    missingRequired = true;
  } else {
    const maskedValue = value.substring(0, 4) + '...' + value.substring(value.length - 4);
    console.log(chalk.green(`✅ ${variable.name}: Set (${maskedValue})`));
  }
});

// Check optional variables
console.log('\n' + chalk.underline('Optional Environment Variables:'));

optionalVars.forEach(variable => {
  const value = process.env[variable.name];
  if (!value) {
    console.log(chalk.yellow(`⚠️  ${variable.name}: Not set (${variable.description})`));
  } else {
    const maskedValue = value.substring(0, 4) + '...' + value.substring(value.length - 4);
    console.log(chalk.green(`✅ ${variable.name}: Set (${maskedValue})`));
  }
});

// Final summary
console.log('\n' + chalk.underline('Summary:'));
if (missingRequired) {
  console.log(chalk.red('❌ Some required environment variables are missing'));
  console.log(chalk.blue('ℹ️  Tip: Add the missing variables to your .env file'));
  process.exit(1);
} else {
  console.log(chalk.green('✅ All required environment variables are set'));
  console.log(chalk.blue('ℹ️  The app is ready to run!'));
  process.exit(0);
} 