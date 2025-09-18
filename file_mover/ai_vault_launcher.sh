#!/bin/bash
# AI Vault Mover Launcher - Manages the background daemon for moving AI chat files.

set -euo pipefail

# --- Configuration ---
APP_NAME="ai-vault-mover"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODE_SCRIPT="$SCRIPT_DIR/ai-vault-mover.js"
MAX_STARTUP_WAIT=10
CHECK_INTERVAL=2

# --- Globals ---
LOG_FILE="/tmp/${APP_NAME}-launcher.log"
PID_FILE="/tmp/${APP_NAME}.pid"
START_TIME=$(date +%s)

# --- Functions ---

log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

notify() {
  local message="$1"
  if command -v osascript &>/dev/null; then
    osascript -e "display notification \"${message//\"/\\\"}\" with title \"$APP_NAME\""
  elif command -v notify-send &>/dev/null; then
    notify-send "$APP_NAME" "$message"
  fi
}

check_if_running() {
  if [[ -f "$PID_FILE" ]]; then
    local old_pid
    old_pid=$(cat "$PID_FILE")
    if [[ -n "$old_pid" ]] && kill -0 "$old_pid" &>/dev/null; then
      log "$APP_NAME already running (PID: $old_pid)"
      notify "$APP_NAME is already running"
      exit 0
    else
      log "Found stale PID file. Removing."
      rm -f "$PID_FILE"
    fi
  fi
}

install_dependencies() {
  local package_json="$SCRIPT_DIR/package.json"

  if [[ ! -f "$package_json" ]]; then
    log "FATAL: package.json not found in $SCRIPT_DIR"
    exit 1
  fi

  if [[ ! -d "$SCRIPT_DIR/node_modules" ]]; then
    log "Installing Node.js dependencies..."
    cd "$SCRIPT_DIR"

    local pm="npm" # Default to npm
    if command -v bun &>/dev/null; then pm="bun";
    elif command -v pnpm &>/dev/null; then pm="pnpm"; fi

    log "Using '$pm' to install dependencies..."
    if ! "$pm" install --prefer-offline --no-progress >>"$LOG_FILE" 2>&1; then
      log "FATAL: Dependency installation failed with '$pm'. Check $LOG_FILE for details."
      notify "$APP_NAME failed: Dependency installation"
      exit 1
    fi
  fi
}

start_daemon() {
    log "Starting $APP_NAME daemon..."
    cd "$SCRIPT_DIR"

    # Launch daemon in the background, ensuring it's detached
    nohup node "$NODE_SCRIPT" >"/tmp/${APP_NAME}-daemon.log" 2>&1 &
    local daemon_pid=$!

    # Disown the process so it doesn't get killed when the shell closes
    disown "$daemon_pid"

    # Wait for the daemon to create its own PID file
    for ((i=0; i<MAX_STARTUP_WAIT; i++)); do
        if [[ -f "$PID_FILE" ]] && [[ "$(cat $PID_FILE)" == "$daemon_pid" ]]; then
             log "Daemon started successfully (PID: $daemon_pid)"
             notify "$APP_NAME daemon is running"
             return 0
        fi
        sleep 1
    done

    log "ERROR: Daemon process started (PID: $daemon_pid) but failed to create its own PID file within ${MAX_STARTUP_WAIT}s."
    notify "$APP_NAME failed to start"
    return 1
}

stop_daemon() {
  if [[ ! -f "$PID_FILE" ]]; then
    log "$APP_NAME is not running (no PID file)"
    return
  fi

  local pid
  pid=$(cat "$PID_FILE")

  if [[ -n "$pid" ]] && kill -0 "$pid" &>/dev/null; then
    log "Stopping $APP_NAME (PID: $pid)..."
    if kill "$pid"; then
      # Wait for the PID file to be removed by the daemon's cleanup handler
      for ((i=0; i<5; i++)); do
        if [[ ! -f "$PID_FILE" ]]; then
          log "$APP_NAME stopped successfully."
          notify "$APP_NAME stopped"
          return 0
        fi
        sleep 1
      done
      log "Warning: PID file was not removed after stopping. Force removing."
      rm -f "$PID_FILE"
    else
      log "Failed to send stop signal to $APP_NAME (PID: $pid)."
    fi
  else
    log "$APP_NAME is not running (stale PID file)"
    rm -f "$PID_FILE"
  fi
}

check_status() {
  if [[ ! -f "$PID_FILE" ]]; then
    echo "$APP_NAME is not running."
    return
  fi

  local pid
  pid=$(cat "$PID_FILE")

  if [[ -n "$pid" ]] && kill -0 "$pid" &>/dev/null; then
    echo "$APP_NAME is running (PID: $pid)"
  else
    echo "$APP_NAME is not running (stale PID file)."
  fi
}

# --- Main Execution Logic ---
main() {
    case "${1:-start}" in
      start)
        check_if_running
        install_dependencies
        start_daemon
        ;;
      stop)
        stop_daemon
        ;;
      status)
        check_status
        ;;
      restart)
        stop_daemon
        sleep 2
        check_if_running
        install_dependencies
        start_daemon
        ;;
      *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
    esac
}

main "$@"
