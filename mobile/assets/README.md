# Assets Directory

This directory contains all static assets used in the فاكر؟ (Faker?) Memory Assistant app.

## Structure

- **fonts/** - Contains Cairo font family for Arabic text
  - Cairo-Regular.ttf
  - Cairo-Bold.ttf
  - Cairo-SemiBold.ttf

- **images/** - Contains app images and placeholders
  - **app/** - App icons and branding
    - icon.png - Main app icon
    - splash.png - Splash screen
    - adaptive-icon.png - Android adaptive icon
    - notification-icon.png - Notification icon
    - favicon.png - Web favicon
  
  - **placeholders/** - Placeholder images for memory prompts
    - family-placeholder.jpg - Family photo placeholder
    - place-placeholder.jpg - Place photo placeholder
    - activity-placeholder.jpg - Activity photo placeholder
    - food-placeholder.jpg - Food photo placeholder
    - birthday-placeholder.jpg - Birthday photo placeholder

## Usage

These assets are referenced in the app code and configuration files. The fonts are loaded in App.tsx, and the images are used in various screens and components.

## Font Attribution

Cairo font is licensed under the SIL Open Font License (OFL).
- Designer: Mohamed Gaber
- Source: https://fonts.google.com/specimen/Cairo

## Image Attribution

Placeholder images are used for demonstration purposes only. In a production environment, these should be replaced with actual patient photos or culturally appropriate images. 