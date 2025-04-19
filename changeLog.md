# Changelog

## [Released] - 2025-04-19

### Added

- **`MIDI_bank_select` MCP Tool:** Implemented a new tool in `mcp_midi_server.py`.
  - **Purpose:** Allows MCP clients to send MIDI Bank Select MSB (CC 0) and LSB (CC 32) messages, typically used before a Program Change.
  - **Parameters:**
    - `bank_msb` (int): Bank Select MSB value (0-127).
    - `bank_lsb` (int): Bank Select LSB value (0-127).
    - `channel` (int, optional): MIDI channel (0-15). Defaults to 0.
  - **Functionality:** Sends two Control Change messages (CC 0 for MSB, CC 32 for LSB) using `python-rtmidi`. Includes input validation. Returns success status and messages.

- **`send_program_change` MCP Tool:** Implemented a new tool in `mcp_midi_server.py` named `send_program_change`.
  - **Purpose:** Allows MCP clients to send MIDI Program Change messages.
  - **Parameters:**
    - `program` (int): The MIDI program number (0-127) to select.
    - `channel` (int, optional): The MIDI channel (0-15) to send the message on. Defaults to 0.
  - **Functionality:** Constructs and sends a standard MIDI Program Change message (Status byte `0xC0` + channel) using the `python-rtmidi` library. Includes input validation for program and channel numbers. Returns a success status and message upon completion.
- **`mcp_midi_tools.py` Module:** Created a new module to hold helper functions.
  - Moved `play_note_with_timing` function from `mcp_midi_server.py` to this new module.

### Changed

- **MCP Tool Naming:** Renamed all MCP tools in `mcp_midi_server.py` to use the `MIDI_` prefix instead of `send_` (e.g., `send_note_on` -> `MIDI_note_on`).
- **Modularization:** Refactored `mcp_midi_server.py` to import and use `play_note_with_timing` from the new `mcp_midi_tools.py` module.
- **Documentation:** Updated the `## API Methods` section in `README.md` to accurately reflect the current MCP tools available in `mcp_midi_server.py`, including correcting names and adding missing tools (`MIDI_program_change`, `MIDI_bank_select`).
