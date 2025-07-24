/**
 * Husky Initialization Script
 * 
 * This script initializes husky git hooks.
 * Run with: node scripts/init-husky.js
 */

const { execSync } = require('child_process');
const chalk = require('chalk');

console.log(chalk.blue('🐶 Initializing Husky git hooks...'));

try {
  // Navigate to project root and initialize husky
  execSync('cd .. && npx husky install mobile/.husky', { stdio: 'inherit' });
  console.log(chalk.green('✅ Husky git hooks initialized successfully!'));
  
  // Add pre-commit hook
  console.log(chalk.blue('📝 Adding pre-commit hook...'));
  execSync('npx husky add .husky/pre-commit "cd mobile && npx lint-staged"', { stdio: 'inherit' });
  
  // Add pre-push hook
  console.log(chalk.blue('📤 Adding pre-push hook...'));
  execSync('npx husky add .husky/pre-push "cd mobile && npm run lint && npm run check-env"', { stdio: 'inherit' });
  
  // Make hooks executable
  execSync('chmod +x .husky/pre-commit .husky/pre-push', { stdio: 'inherit' });
  
  console.log(chalk.green('✅ Git hooks added and made executable!'));
  console.log(chalk.blue('ℹ️  Husky will now run checks before commits and pushes.'));
} catch (error) {
  console.error(chalk.red(`❌ Error initializing Husky: ${error.message}`));
  process.exit(1);
} 