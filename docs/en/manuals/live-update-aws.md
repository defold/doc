---
title: Migrating Live Update publishing from Amazon S3
brief: This manual explains how to migrate projects that used Defold's built-in Amazon S3 publisher.
---

# Migrating from built-in S3 publishing

Defold 1.14.2 removes the built-in Amazon S3 publisher from the editor and Bob. Bundling with legacy **Amazon** settings fails when external packages are requested.

To keep using S3 to host your content, select **Zip** or **Folder** in the [legacy Live Update settings](/manuals/live-update/#legacy-live-update-settings), or configure a ZIP or Folder package in an [archive manifest](/manuals/live-update/#archive-manifests). Upload the exported content to your bucket as a separate step in your release process. Keep the filenames and URLs expected by the game, or update your download code when you change the layout.
