# MCP MIDI Server

A FastMCP Server which allows an LLM to send MIDI sequences into any software that supports MIDI input.

Cloned from [https://github.com/sandst1/mcp-server-midi](https://github.com/sandst1/mcp-server-midi)

## Why the fork?

- I preffer to use uv for virtual environments, and I don't want to install the dependencies globally.
- Had some issues with the original repo when retrieving ports.
- I need Program Change and Control Change messages.
- I need some specific features for my vintage synths: Oberheim Matrix 1000 has an specific way to send the program change messages.

## Features

- Creates a virtual MIDI output port
- Sends MIDI Note On/Off messages
- Sends Control Change (CC) messages
- Sequences MIDI events with precise timing
- Can be used as a MIDI input device in any application that supports MIDI

## Requirements

- Python 3.7+
- rtmidi
- fastmcp
- python-dotenv
- asyncio

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd mcp-server-midi
   ```

2. Create a virtual env with uv, and install the dependencies:

   ```bash
   uv venv .venv
   .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration:

   ```bash
   cp .env.example .env
   
4. Edit the `.env` file to set your desired configuration. For example:

   ```
   PORT=8123
   MIDI_PORT_NAME="loopMIDI"
   ```

5. Install the required MIDI driver for your OS if you haven't so (e.g., loopMIDI for Windows, IAC Driver for macOS).

I highly recommend using [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) for Windows, as it is a lightweight and easy-to-use virtual MIDI port driver.

## Usage

Run the server:

```bash
uv run mcp_midi_server.py
```

The server creates a virtual MIDI port named "MCP MIDI Out" that can be used as a MIDI input device in other applications. This means you can:

- Connect digital audio workstations (DAWs) like Ableton Live, Logic Pro, or FL Studio to receive MIDI from this server
- Use the server to control hardware synthesizers through your computer's MIDI interface
- Connect to any other software that accepts MIDI input (virtual instruments, lighting controllers, etc.)

Simply select "MCP MIDI Out" as a MIDI input device in your preferred MIDI-compatible application.

## MCP Config

The server uses Server-Sent Events (SSE):

Create a .vscode/mcp.json file in your project directory with the following content:

This is a "per workspace" aproach, you can consolidate it globally later.

```json
{
   "servers": {
      "midi": {
         "type": "sse",
         "url": "http://localhost:8123/sse"
      }
   }
}
```

## API Methods

### `MIDI_note_on`

Sends a MIDI Note On message.

Parameters:

- `note`: MIDI note number (0-127).
- `velocity`: Note velocity (0-127, default 127).
- `channel`: MIDI channel (0-15, default 0).

### `MIDI_note_off`

Sends a MIDI Note Off message.

Parameters:

- `note`: MIDI note number (0-127).
- `velocity`: Note off velocity (0-127, default 64).
- `channel`: MIDI channel (0-15, default 0).

### `MIDI_control_change`

Sends a MIDI Control Change (CC) message.

Parameters:

- `controller`: CC controller number (0-127).
- `value`: CC value (0-127).
- `channel`: MIDI channel (0-15, default 0).

### `MIDI_program_change`

Sends a MIDI Program Change message.

Parameters:

- `program`: Program number (0-127).
- `channel`: MIDI channel (0-15, default 0).

### `MIDI_bank_select`

Sends MIDI Bank Select messages (CC 0 and CC 32). These messages are typically sent before a Program Change to select the desired sound bank.

Parameters:

- `bank_msb`: Bank Select MSB value (0-127). Controller 0.
- `bank_lsb`: Bank Select LSB value (0-127). Controller 32.
- `channel`: MIDI channel (0-15, default 0).

### `MIDI_sequence`

Sends a sequence of MIDI Note On/Off messages with specified durations.

Parameters:

- `events`: A list of event dictionaries. Each dictionary must contain:
    - `note`: MIDI note number (0-127).
    - `velocity`: Note velocity (0-127, default 127).
    - `channel`: MIDI channel (0-15, default 0).
    - `duration`: Time in seconds to hold the note before sending Note Off (float).
    - `start_time`: Time in seconds when to start the note, relative to sequence start (default 0).

## Example

Using the API to play a C major chord:

```python
events = [
    {"note": 60, "velocity": 100, "duration": 1.0, "start_time": 0.0},  # C4
    {"note": 64, "velocity": 100, "duration": 1.0, "start_time": 0.0},  # E4
    {"note": 67, "velocity": 100, "duration": 1.0, "start_time": 0.0},  # G4
]
# Send to the MCP MIDI Server API
```

## License

MIT
