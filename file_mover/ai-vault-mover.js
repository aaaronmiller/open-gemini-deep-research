#!/usr/bin/env node
// ai-vault-mover.js - Background daemon for moving AI chat captures to Obsidian vault

const fs = require('fs').promises;
const path = require('path');
const os = require('os');
const chokidar = require('chokidar'); // npm install chokidar

// --- Configuration ---
const APP_NAME = "ai-vault-mover";
const DOWNLOADS_DIR = path.join(os.homedir(), 'Downloads');
// Corrected vault path to be consistent with the main application, adding a 'captures' subfolder.
const VAULT_PATH = '/Users/macuser/Documents/ChetasVault/captures';
const FILE_PATTERN = /^ai-session-.*\.md$/;
const CHECK_INTERVAL = 2; // seconds
const MAX_RUNTIME_HOURS = 12; // Auto-restart after this time
const LOG_FILE = `/tmp/${APP_NAME}.log`;
const PID_FILE = `/tmp/${APP_NAME}.pid`;

// --- Globals ---
const START_TIME = Date.now();
let watcher = null;

// --- Functions ---

function log(message) {
  const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 19);
  const logEntry = `${timestamp} - ${message}`;
  console.log(logEntry);

  // Append to log file
  fs.appendFile(LOG_FILE, logEntry + '\n').catch(() => {});
}

function notify(message) {
  if (process.platform === 'darwin') {
    require('child_process').exec(
      `osascript -e 'display notification "${message.replace(/"/g, '\\"')}" with title "${APP_NAME}"'`
    );
  } else if (process.platform === 'linux') {
    require('child_process').exec(`notify-send "${APP_NAME}" "${message}"`);
  }
}

function calculateRuntime() {
  const runtime = Math.floor((Date.now() - START_TIME) / 1000);
  const hours = Math.floor(runtime / 3600);
  const minutes = Math.floor((runtime % 3600) / 60);
  const seconds = runtime % 60;
  return `${hours}h ${minutes}m ${seconds}s`;
}

async function cleanup(exitCode = 0) {
  const runtime = calculateRuntime();

  if (watcher) {
    await watcher.close();
    log('File watcher stopped');
  }

  try {
    await fs.unlink(PID_FILE);
  } catch (error) {
    // PID file might not exist
  }

  if (exitCode === 0) {
    log(`Clean exit completed. Session runtime: ${runtime}`);
  } else {
    log(`Exit with error (code ${exitCode}). Session runtime: ${runtime}`);
  }

  process.exit(exitCode);
}

// Set up signal handlers
process.on('SIGINT', () => cleanup(0));
process.on('SIGTERM', () => cleanup(0));
process.on('uncaughtException', (error) => {
  log(`FATAL ERROR: ${error.message}`);
  cleanup(1);
});

async function checkIfRunning() {
  try {
    const pidData = await fs.readFile(PID_FILE, 'utf8');
    const oldPid = parseInt(pidData.trim());

    if (oldPid) {
      try {
        process.kill(oldPid, 0); // Check if process exists
        log(`${APP_NAME} already running (PID: ${oldPid}). Exiting.`);
        notify(`${APP_NAME} is already running`);
        process.exit(0);
      } catch (error) {
        log('Found stale PID file. Removing.');
        await fs.unlink(PID_FILE);
      }
    }
  } catch (error) {
    // PID file doesn't exist, continue
  }
}

async function ensureVaultExists() {
  try {
    // Use fs.mkdir with recursive option to ensure the full path exists.
    await fs.mkdir(VAULT_PATH, { recursive: true });
    log(`✓ Obsidian vault path ensured: ${VAULT_PATH}`);
  } catch (error) {
    log(`✗ FATAL: Could not create or access vault path: ${VAULT_PATH}`);
    log('Please check permissions and update VAULT_PATH in this script if needed.');
    notify(`${APP_NAME} failed: Vault path issue`);
    process.exit(1);
  }
}

async function moveFile(sourcePath, filename) {
  try {
    const targetPath = path.join(VAULT_PATH, filename);
    let finalTargetPath = targetPath;
    let counter = 1;

    while (true) {
      try {
        await fs.access(finalTargetPath);
        const ext = path.extname(filename);
        const base = path.basename(filename, ext);
        finalTargetPath = path.join(VAULT_PATH, `${base}-${counter}${ext}`);
        counter++;
      } catch (error) {
        break;
      }
    }

    await fs.rename(sourcePath, finalTargetPath);
    log(`✓ Moved: ${filename} → ${path.basename(finalTargetPath)}`);
    notify(`AI chat saved: ${path.basename(finalTargetPath)}`);

  } catch (error) {
    log(`✗ Failed to move ${filename}: ${error.message}`);
    notify(`Failed to move ${filename}`);
  }
}

async function startWatching() {
  await checkIfRunning();
  await ensureVaultExists();

  await fs.writeFile(PID_FILE, process.pid.toString());

  log(`--- Starting ${APP_NAME} (PID: ${process.pid}) ---`);
  log(`🔍 Watching Downloads: ${DOWNLOADS_DIR}`);
  log(`📁 Target Vault: ${VAULT_PATH}`);
  log(`🎯 File Pattern: ${FILE_PATTERN}`);

  watcher = chokidar.watch(DOWNLOADS_DIR, {
    ignored: /^\./,
    persistent: true,
    ignoreInitial: true, // Only watch for new files
    depth: 1, // Watch main downloads folder and one level deep
    awaitWriteFinish: {
      stabilityThreshold: 1000,
      pollInterval: 100
    }
  });

  watcher.on('add', (filePath) => {
    const filename = path.basename(filePath);
    if (FILE_PATTERN.test(filename)) {
      log(`📋 Detected AI chat file: ${filename}`);
      setTimeout(() => moveFile(filePath, filename), 500);
    }
  });

  watcher.on('error', (error) => log(`Watcher error: ${error.message}`));

  notify(`${APP_NAME} started - watching for AI chats`);
}

// --- Entry Point ---
startWatching().catch((error) => {
  log(`FATAL: ${error.message}`);
  notify(`${APP_NAME} failed to start`);
  process.exit(1);
});
