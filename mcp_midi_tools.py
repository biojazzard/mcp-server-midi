import asyncio
import rtmidi # Assuming rtmidi.MidiOut is needed for type hinting or potential future use within this module

async def play_note_with_timing(
    midiout: rtmidi.MidiOut, # Added midiout parameter
    note, velocity, channel, duration, start_time,
    sequence_start, event_index, results
):
    """Helper function to play a single note with proper timing."""
    # Calculate absolute times
    now = asyncio.get_event_loop().time()
    time_elapsed = now - sequence_start

    # Wait until it's time to start this note
    if start_time > time_elapsed:
        await asyncio.sleep(start_time - time_elapsed)

    # Send Note On
    try:
        status_on = 0x90 | channel
        message_on = [status_on, note, velocity]
        midiout.send_message(message_on)
        on_msg = f"Sent Note On: ch={channel}, note={note}, vel={velocity}"
        print(on_msg)
        results.append({
            "status": "note_on_sent",
            "message": on_msg,
            "event_index": event_index
        })

        # Wait for the note duration
        await asyncio.sleep(duration)

        # Send Note Off
        status_off = 0x80 | channel
        message_off = [status_off, note, 0]  # Note Off with velocity 0
        midiout.send_message(message_off)
        off_msg = f"Sent Note Off: ch={channel}, note={note}"
        print(off_msg)
        results.append({
            "status": "note_off_sent",
            "message": off_msg,
            "event_index": event_index
        })
    except Exception as e:
        error_msg = f"Event {event_index}: Error processing event: {e}"
        print(error_msg)
        results.append({
            "status": "error",
            "message": error_msg,
            "event_index": event_index
        })
