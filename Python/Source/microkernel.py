
import sys
import os
import gc
import argparse
import time
import importlib
import inspect
import glob

# Data
TASK_REGISTRY = {}
_task_stack = []
_flags = { "debug": True, "attention": True , "error": True}
last_time = time.time()

def init():
    global _flags
   
   # Run this once when your script starts
    task_importer()

   # CLI: Parser
    cli_parser = argparse.ArgumentParser(description="VoxCore: Stack-based execution engine.")
    cli_parser.add_argument("--flags", nargs='+', default=[], choices=['debug', 'attention', 'error'], help="Enable flags. Options: debug, attention, error.")
    cli_parser.add_argument("--intent_file", nargs='+', help="Path to one or more .dspec files in the data folder.")
    for task_class in TASK_REGISTRY.values():
        cli_parser.add_argument(task_class.command, action="store_true", help=f"Add {task_class.__name__} to the execution stack.")
    cli_args = cli_parser.parse_args()
    
    # Flags
    for flag in cli_args.flags:
        if flag in _flags:
            _flags[flag] = not _flags[flag]

    # Add tasks
    # Argparse strips the dashes and converts hyphens to underscores for the dictionary key
    for arg in sys.argv[1:]:
        if arg in TASK_REGISTRY:
            task_toggle(arg)

    # Intent files
    if cli_args.intent_file:
        process_command("--ui_spacer")
        for file_path in cli_args.intent_file:
            if _flags.get("debug"):
                process_command(f"--ui_header [CLI ARGS] {file_path}")
            process_command(f"--intent_file {file_path}")

    # Run
    last_time = time.time()
    while True:
        try:
            # 1. Calculate the Delta (Time elapsed since the last loop)
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time

            # 2. Execute EVERY task in the stack
            for task in _task_stack:
                    task.run(delta_time)

            # 3. Small sleep to prevent 100% CPU usage (Optional)
            time.sleep(0.001)

        except KeyboardInterrupt:
            break


TASK_REGISTRY = {}

def task_importer():
    # Add the script directory to sys.path so importlib can import the files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
        
    # Search for files exactly in the script's directory
    search_pattern = os.path.join(script_dir, "task_*.py")
    for file_path in glob.glob(search_pattern):
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        try:
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if hasattr(obj, 'command') and obj.command.startswith("--task_"):
                    TASK_REGISTRY[obj.command] = obj
        except ImportError as e:
            print(f"Failed to load {module_name}: {e}")

def task_toggle(task_command):
    global _task_stack

    # Guard: Registry
    if not TASK_REGISTRY[task_command]:
        process_command(f"--ui_error Service '{task_command}' not found in registry.")
        return
    
    # Terminate
    for task in _task_stack:
        if task.command == task_command:
            task.terminate()
            _task_stack.remove(task)
            return
        
    # Boot
    new_task = TASK_REGISTRY[task_command](process_command,_flags)
    _task_stack.append(new_task)
    new_task.boot()

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
        for task in _task_stack:
                task.terminate()
        gc.collect() 
        process_command("--ui_clear")
        os._exit(0)

    # Intent: File
    if command_lower.startswith("--intent_file "):
        filepath = text[14:].strip()
        if filepath:
            intents = dspec_parse_section_from_file(filepath, ".intent")
            for intent in intents:
                process_command(f"--intent_add {intent}", source="task")
            if len(intents) > 0 and _flags.get("debug"):
                 process_command(f"--ui_spacer")
        return
        
    # Tasks
    target_task = next((s for s in TASK_REGISTRY.values() if s.command == command_lower), None)
    if target_task:
        task_toggle(target_task.command)
        return
    
    # Process commands by tasks (UI catches UI commands here!)
    else: 
        for task in _task_stack:
            handled = task.on_command(text)
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