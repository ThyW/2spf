from .constants import flag_debug, flag_silent

def msg(type: str, message: str) -> None:
    # FIXME: Use a match statement here!
    if not flag_silent: 
        if type == "w":
            print(f"[WARNINIG] {message}")
        if type == "e":
            print(f"[ERROR] {message}")
        if type == "m":
            print(f"[MESSAGE] {message}")

def debug(message: str) -> None:
    if flag_debug:
        print(f"[DEBUG] {message}")
