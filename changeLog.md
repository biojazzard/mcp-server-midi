# Changelog

## [Unreleased] - 2025-04-19

### Added

- **`send_program_change` MCP Tool:** Implemented a new tool in `mcp_midi_server.py` named `send_program_change`.
  - **Purpose:** Allows MCP clients to send MIDI Program Change messages.
  - **Parameters:**
    - `program` (int): The MIDI program number (0-127) to select.
    - `channel` (int, optional): The MIDI channel (0-15) to send the message on. Defaults to 0.
  - **Functionality:** Constructs and sends a standard MIDI Program Change message (Status byte `0xC0` + channel) using the `python-rtmidi` library. Includes input validation for program and channel numbers. Returns a success status and message upon completion.
