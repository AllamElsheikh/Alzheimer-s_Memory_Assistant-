module.exports = {
  root: true,
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
  ],
  parser: '@typescript-eslint/parser',
  plugins: ['react', 'react-hooks', '@typescript-eslint'],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  env: {
    browser: true,
    es2020: true,
    node: true,
    jest: true,
  },
  rules: {
    // Relaxed rules for development
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    'react/prop-types': 'off', // We use TypeScript for prop validation
    'react/react-in-jsx-scope': 'off', // Not needed in React 17+
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
    'no-console': ['warn', { allow: ['warn', 'error'] }],
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
  ignorePatterns: ['node_modules/', 'babel.config.js', 'metro.config.js'],
}; 