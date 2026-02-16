# Antigravity Mission Instructions: Theta Data V3

## Workspace Context
- **Root:** `~/projects/thetadata/`
- **Scripts:** `./scripts/`
- **Docs:** `../docs/V3_MASTER_REFERENCE.md`
- **Terminal:** `../bin/ThetaTerminalv3.jar`

## Environment Setup
- Always use the `.venv` in the `scripts` folder.
- If Port 25503 is closed, run: `nohup java -jar ../bin/ThetaTerminalv3.jar > ../bin/terminal_log.txt 2>&1 &`

## Coding Rules
1. **Reference Docs:** Always read `../docs/V3_MASTER_REFERENCE.md` before writing data-fetching logic.
2. **Syntax:** Use `ThetaClient(port=25503)`. Never use `Stream` or pagination loops.
3. **Validation:** Use `curl "http://127.0.0.1:25503/v3/calendar/open_today"` to verify the bridge is active before execution.
