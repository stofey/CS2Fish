import winreg

def get_cs_path():
    try:
        hKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\WOW6432Node\\Valve\\cs2')
        path = winreg.QueryValueEx(hKey, 'installpath')[0]
        winreg.CloseKey(hKey)
        return str(path)
    except:
        return None

def roll_slot_machine(bet_amount):
    import random

    symbols = ['♠︎', '♣︎', '◆︎', '♥︎', '♛︎']
    weights = [0.35, 0.25, 0.2, 0.15, 0.05]  # Adjust probabilities for fewer matches

    roll = random.choices(symbols, weights, k=3)

    if roll[0] == roll[1] == roll[2]:
        multiplier = {
            '♠︎': 10, # Multipliers for 3 Matching symbols
            '♣︎': 25,
            '◆︎': 50,
            '♥︎': 100,
            '♛︎': 250,
        }[roll[0]]
        winnings = bet_amount * multiplier
    elif roll[0] == roll[1] or roll[1] == roll[2] or roll[0] == roll[2]:
        multiplier = {
            '♠︎': 1, # Multipliers for 2 Matching symbols
            '♣︎': 1.1,
            '◆︎': 1.25,
            '♥︎': 1.5,
            '♛︎': 2,
        }[roll[0]]
        winnings = bet_amount * multiplier
    else:
        winnings = -bet_amount

    return roll, winnings


last_offset = 0

def get_last_chat(log_dir, n=10):
    global last_offset
    try:
        with open(log_dir, encoding='utf-8', errors='replace') as f:
            f.seek(0, 2)
            file_size = f.tell()

            if last_offset > file_size:
                last_offset = 0

            f.seek(last_offset, 0)
            lines = f.readlines()
            last_offset = f.tell()

            return lines[-n:]
    except Exception as e:
        print(f"Error reading log: {e}")
        return None


def get_last_name_used():
    try:
        hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'SOFTWARE\\Valve\\Steam')
        name = winreg.QueryValueEx(hKey, 'LastGameNameUsed')[0]
        winreg.CloseKey(hKey)
        return name
    except:
        return None

def write_command(command):
    try:
        cfg_path = "S:\\SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\game\\csgo\\cfg\\message.cfg" #you need to make a message.cfg file, leave it empty and put the path to it here
        with open(cfg_path, 'w', encoding='utf-8') as f:
            f.write(command) 

    except Exception as e:
        print(f"Error writing command: {e}")


def press_key():
    import pydirectinput
    pydirectinput.write('p')