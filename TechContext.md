# Technical Context for mcp-server-midi

## Project Goal

This project provides a **FastMCP server** that allows a Large Language Model (LLM) or other MCP clients to send MIDI messages (Note On/Off, Control Change, sequences) to MIDI-compatible software or hardware connected to the host machine. It acts as a bridge between the MCP ecosystem and the MIDI world.

This specific version is a fork of the original `sandst1/mcp-server-midi` repository, incorporating modifications for `uv` environment management, improved MIDI port handling, and potentially specific features for vintage synthesizers (like Oberheim Matrix 1000 program changes, although not explicitly implemented in the current script).

## Architecture

- **Language:** Python 3.7+
- **Framework:** `FastMCP` (built on FastAPI) for creating the MCP server and defining tools.
- **MIDI Backend:** `python-rtmidi` library for interacting with the system's MIDI interfaces and creating/managing virtual MIDI ports.
- **Concurrency:** `asyncio` is used, particularly within the `send_midi_sequence` tool, to handle timed MIDI events precisely.
- **Configuration:** Uses `python-dotenv` to load settings (like server port and target MIDI port name) from a `.env` file.

## Key Technologies & Libraries

- **`fastmcp` / `fastapi`:** Core web framework for the MCP server.
- **`python-rtmidi`:** Essential for MIDI communication.
- **`uvicorn`:** ASGI server to run the FastAPI application.
- **`asyncio`:** For handling asynchronous operations, especially timed MIDI sequences.
- **`python-dotenv`:** For managing environment variables.
- **`uv`:** Preferred tool for Python environment and package management (as per README).

## Core Functionality

1. **Virtual MIDI Port Creation:** On startup, the server attempts to find and open a MIDI output port specified by the `MIDI_PORT_NAME` environment variable (defaulting to "loopMIDI Port"). This port then appears as a standard MIDI input ("MCP MIDI Out" or similar, depending on the driver) in other applications (DAWs, virtual instruments, etc.).
2. **MCP Tools:** Exposes the following tools for MCP clients:
    - `send_note_on(note, velocity, channel)`: Sends a MIDI Note On message.
    - `send_note_off(note, velocity, channel)`: Sends a MIDI Note Off message.
    - `send_control_change(controller, value, channel)`: Sends a MIDI Control Change (CC) message.
    - `send_midi_sequence(events)`: Sends a list of timed MIDI events (Note On followed by Note Off after a duration), allowing for basic sequencing.

## Configuration

- A `.env` file is used to configure:
  - `PORT`: The network port for the FastMCP server (e.g., 8123).
  - `MIDI_PORT_NAME`: The name (or part of the name) of the target MIDI output port to use (e.g., "loopMIDI Port").

## Setup & Running

1. **Environment:** Create a virtual environment using `uv venv .venv`.
2. **Dependencies:** Install dependencies using `uv pip install -r requirements.txt`.
3. **MIDI Driver:** Requires a virtual MIDI driver (like loopMIDI for Windows or IAC Driver for macOS) to be installed and running, providing the port specified in `.env`.
4. **Run:** Execute the server using `uv run mcp_midi_server.py`.

## Style & Constraints (Based on `.clinerules` and Project Structure)

- **Style:** Adheres to standard Python practices (PEP 8).
- **Dependencies:** Only use dependencies listed in `requirements.txt`.
- **Modularity:** Code is primarily within the main `mcp_midi_server.py` script. While relatively short currently, future additions should consider modularity if complexity increases.
- **Environment Management:** Use `uv` for managing the virtual environment and dependencies.
