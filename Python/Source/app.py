import sys
import os
import gc
import argparse
import time

import service_command_keys_mac
import service_input_hotkeys
import service_input_whisper
import service_intent_rapidfuzz
import service_ui_terminal

SERVICE_REGISTRY = {
    s.command: s for s in {
        service_command_keys_mac.ServiceCommandKeysMac,
        service_input_hotkeys.ServiceInputHotkeys,
        service_input_whisper.ServiceInputWhisper,
        service_intent_rapidfuzz.ServiceIntentRapidFuzz,
        service_ui_terminal.ServiceUITerminal,
    }
}

debug = False
_service_stack = []

def init():
    global debug
   
   # CLI: Parser
    cli_parser = argparse.ArgumentParser(description="VoxCore: Stack-based execution engine.")
    cli_parser.add_argument("--debug", action="store_true", help="Enable debugging.")
    cli_parser.add_argument("--intent_file", nargs='+', help="Path to one or more .dspec files in the data folder.")
    for service_class in SERVICE_REGISTRY.values():
        cli_parser.add_argument(service_class.command, action="store_true", help=f"Add {service_class.__name__} to the execution stack.")
    cli_args = cli_parser.parse_args()
    
    # Debug
    debug = cli_args.debug

    # Add services
    # Argparse strips the dashes and converts hyphens to underscores for the dictionary key
    for arg in sys.argv[1:]:
        if arg in SERVICE_REGISTRY:
            service_toggle(arg)

    # Intent files
    if cli_args.intent_file:
        process_command("--ui_spacer")
        for file_path in cli_args.intent_file:
            process_command(f"--ui_header [CLI ARGS] {file_path}")
            process_command(f"--intent_file {file_path}")

    # Run
    blocking_service = next((sys for sys in _service_stack if hasattr(sys, 'run')), None)
    if blocking_service:
        blocking_service.run()
    else:
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

def service_toggle(service_command):
    global _service_stack

    # Guard: Registry
    if not SERVICE_REGISTRY[service_command]:
        process_command(f"--ui_error Service '{service_command}' not found in registry.")
        return
    
    # Remove
    for service in _service_stack:
        if service.command == service_command:
            service.stop()
            _service_stack.remove(service)
            return
        
    # Add
    new_service = SERVICE_REGISTRY[service_command](process_command)
    _service_stack.append(new_service)
    new_service.start()

def process_command(text: str, source: str = "Unknown"):
    global debug
    
    # Guard
    if text == "": return

    # Command
    command = text.strip()
    command_lower = command.lower()
    if not command: return

    # Exit
    if source.lower() == "keyboard" and command_lower.rstrip('.') in ['--exit', '--end', '--quit', '--stop']:
        for service in _service_stack:
            if hasattr(service, 'stop'):
                service.stop()
        gc.collect() 
        process_command("--ui_clear")
        os._exit(0)

    # Intent: File
    if command_lower.startswith("--intent_file "):
        filepath = text[14:].strip()
        if filepath:
            for intent in dspec_parse_section_from_file(filepath, ".intent"):
                process_command(f"--intent_add {intent}", source="system")
        return
        
    # Services
    target_service = next((s for s in SERVICE_REGISTRY.values() if s.command == command_lower), None)
    if target_service:
        service_toggle(target_service.command)
        return
    
    # Process commands by services (UI catches UI commands here!)
    else: 
        for service in _service_stack:
            handled = service.on_command(text)
            if handled:
                return

def dspec_parse_section_from_file(filepath: str, section_name: str = ".intent"):
    # Resolve relative paths to the sibling 'data' folder
    if not os.path.isabs(filepath):
        filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", filepath)

    if not os.path.exists(filepath):
        return []

    results = []
    in_section = False
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Section logic: Start at target, stop at next dot
            if line.startswith('.'):
                if line.lower() == section_name.lower():
                    in_section = True
                    continue
                elif in_section:
                    break 
            
            # Content logic: ignore empty lines and # comments
            if in_section and line and not line.startswith('#'):
                results.append(line)
                
    return results

if __name__ == "__main__":
    init()