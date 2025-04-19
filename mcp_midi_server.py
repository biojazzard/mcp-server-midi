import os
import rtmidi
import asyncio
from fastmcp import FastMCP
from dotenv import load_dotenv
from mcp_midi_tools import play_note_with_timing # Import the function

load_dotenv()

# --- MIDI Setup ---
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
target_port_name = os.getenv("MIDI_PORT_NAME", "loopMIDI Port") # Default or from .env

port_index = -1
if available_ports:
    print("Available MIDI output ports:")
    for i, port in enumerate(available_ports):
        print(f"{i}: {port}")
        # Try to find the port by the name specified in .env or the default
        if target_port_name in port:
            port_index = i
            break # Use the first match

    if port_index != -1:
        try:
            midiout.open_port(port_index)
            print(f"Opened MIDI port: {available_ports[port_index]}")
        except rtmidi.RtMidiError as e:
            print(f"Error opening MIDI port {port_index} ('{available_ports[port_index]}'): {e}")
            print("Please ensure the MIDI port is available and not in use.")
            print(f"Make sure a virtual MIDI driver like loopMIDI is running and provides a port named '{target_port_name}'.")
            exit()
    else:
        print(f"Error: Could not find MIDI port containing the name '{target_port_name}'.")
        print("Please ensure a virtual MIDI driver like loopMIDI is running or specify the correct port name in the .env file using MIDI_PORT_NAME.")
        if not available_ports:
            print("No MIDI output ports found at all.")
        exit()
else:
    print("Error: No MIDI output ports found.")
    print("Please ensure a MIDI interface or virtual MIDI driver (like loopMIDI) is installed and running.")
    exit()

# --- MCP Server Setup ---
mcp = FastMCP(
    name="MCP MIDI Server",
    instructions="Sends MIDI commands received via MCP.",
    settings={
        "port": os.getenv("PORT")
    }
)

# --- MCP Methods ---
# We will define methods here to handle MIDI messages

# Example: Send Note On
@mcp.tool()
async def MIDI_note_on(
    note: int,
    velocity: int = 127,
    channel: int = 0
):
    """Sends a MIDI Note On message.

    Args:
        note: MIDI note number (0-127).
        velocity: Note velocity (0-127, default 127).
        channel: MIDI channel (0-15, default 0).
    """
    if not 0 <= note <= 127:
        raise ValueError("Note must be between 0 and 127")
    if not 0 <= velocity <= 127:
        raise ValueError("Velocity must be between 0 and 127")
    if not 0 <= channel <= 15:
        raise ValueError("Channel must be between 0 and 15")

    # MIDI Note On status byte: 0x90 | channel
    status = 0x90 | channel
    message = [status, note, velocity]
    midiout.send_message(message)
    msg = f"Sent Note On: ch={channel}, note={note}, vel={velocity}"
    print(msg)
    return {"status": "success", "message": msg}

# Example: Send Note Off
@mcp.tool()
async def MIDI_note_off(
    note: int,
    velocity: int = 64,
    channel: int = 0
):
    """Sends a MIDI Note Off message.

    Args:
        note: MIDI note number (0-127).
        velocity: Note off velocity (0-127, default 64).
        channel: MIDI channel (0-15, default 0).
    """
    if not 0 <= note <= 127:
        raise ValueError("Note must be between 0 and 127")
    if not 0 <= velocity <= 127:
        raise ValueError("Velocity must be between 0 and 127")
    if not 0 <= channel <= 15:
        raise ValueError("Channel must be between 0 and 15")

    # MIDI Note Off status byte: 0x80 | channel
    status = 0x80 | channel
    message = [status, note, velocity]
    midiout.send_message(message)
    msg = f"Sent Note Off: ch={channel}, note={note}, vel={velocity}"
    print(msg)
    return {"status": "success", "message": msg}

# Example: Send Control Change
@mcp.tool()
async def MIDI_control_change(
    controller: int,
    value: int,
    channel: int = 0
):
    """Sends a MIDI Control Change (CC) message.

    Args:
        controller: CC controller number (0-127).
        value: CC value (0-127).
        channel: MIDI channel (0-15, default 0).
    """
    if not 0 <= controller <= 127:
        raise ValueError("Controller number must be between 0 and 127")
    if not 0 <= value <= 127:
        raise ValueError("Value must be between 0 and 127")
    if not 0 <= channel <= 15:
        raise ValueError("Channel must be between 0 and 15")

    # MIDI CC status byte: 0xB0 | channel
    status = 0xB0 | channel
    message = [status, controller, value]
    midiout.send_message(message)
    msg = f"Sent CC: ch={channel}, cc={controller}, val={value}"
    print(msg)
    return {"status": "success", "message": msg}

# --- New Tool: Send Program Change ---
@mcp.tool()
async def MIDI_program_change(
    program: int,
    channel: int = 0
):
    """Sends a MIDI Program Change message.

    Args:
        program: Program number (0-127).
        channel: MIDI channel (0-15, default 0).
    """
    if not 0 <= program <= 127:
        raise ValueError("Program number must be between 0 and 127")
    if not 0 <= channel <= 15:
        raise ValueError("Channel must be between 0 and 15")

    # MIDI Program Change status byte: 0xC0 | channel
    status = 0xC0 | channel
    message = [status, program]
    midiout.send_message(message)
    msg = f"Sent Program Change: ch={channel}, program={program}"
    print(msg)
    return {"status": "success", "message": msg}

# --- New Tool: Send MIDI Sequence ---
@mcp.tool()
async def MIDI_sequence(events: list):
    """Sends a sequence of MIDI Note On/Off messages with specified durations.

    Args:
        events: A list of event dictionaries. Each dictionary must contain:
            - note: MIDI note number (0-127).
            - velocity: Note velocity (0-127, default 127).
            - channel: MIDI channel (0-15, default 0).
            - duration: Time in seconds to hold the note before sending
              Note Off (float).
            - start_time: Time in seconds when to start the note,
              relative to sequence start (default 0).
    """
    # Start time reference for the entire sequence
    sequence_start = asyncio.get_event_loop().time()
    tasks = []
    results = []

    for i, event in enumerate(events):
        note = event.get("note")
        velocity = event.get("velocity", 127)
        channel = event.get("channel", 0)
        duration = event.get("duration")
        start_time = event.get("start_time", 0)

        # --- Input Validation ---
        error_prefix = f"Event {i}:"
        if note is None:
            raise ValueError(f"{error_prefix} 'note' is required.")
        if duration is None:
            raise ValueError(f"{error_prefix} 'duration' is required.")
        if not isinstance(note, int) or not 0 <= note <= 127:
            raise ValueError(
                f"{error_prefix} Note must be an integer between 0 and 127"
            )
        if not isinstance(velocity, int) or not 0 <= velocity <= 127:
            raise ValueError(
                f"{error_prefix} Velocity must be an integer between 0 and 127"
            )
        if not isinstance(channel, int) or not 0 <= channel <= 15:
            raise ValueError(
                f"{error_prefix} Channel must be an integer between 0 and 15"
            )
        if not isinstance(duration, (int, float)) or duration < 0:
            raise ValueError(
                f"{error_prefix} Duration must be a non-negative number"
            )
        if not isinstance(start_time, (int, float)) or start_time < 0:
            raise ValueError(
                f"{error_prefix} start_time must be a non-negative number"
            )

        # Create async task for this note
        task = asyncio.create_task(
            play_note_with_timing(
                midiout, # Pass midiout object
                note, velocity, channel, duration, start_time,
                sequence_start, i, results
            )
        )
        tasks.append(task)

    # Wait for all notes to complete
    if tasks:
        await asyncio.gather(*tasks)

    num_events = len(events)
    success_msg = f"Successfully processed {num_events} events."
    return {
        "status": "success",
        "message": success_msg,
        "results": results
    }

# --- Main Execution ---
if __name__ == "__main__":
    # Ensure MIDI port is closed properly on exit
    import atexit
    atexit.register(midiout.close_port)

    mcp.run(transport='sse')
    # This part might not be reached if server.run() blocks indefinitely
    # Consider running the server in a separate thread if needed
    # Cleanup is handled by atexit
    # print("Closing MIDI port...")
    # midiout.close_port()
    # print("Server stopped.")
