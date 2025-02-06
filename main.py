import asyncio
import time
import re
from util import *
from util import roll_slot_machine
from fish import earnings, cast_line, update_user, get_user, press_key

cs_path = "S:\\SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\game\\csgo\\console.log" #change to your path
log_dir = "S:\\SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\game\\csgo\\console.log" #change to your path
exec_dir = "S:\\SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\game\\csgo\\cfg\\message.cfg" #you need to make a message.cfg file, leave it empty and put the path to it here

chat_char_limit = 222
chat_delay = 0.5
last_log = ''
each_key_delay = 0.2
last_command_time = 0

fishing_delay = 5

async def handle_chat():
    user_last_command_time = {}

    while True:
        new_lines = get_last_chat(log_dir)

        if not new_lines:
            await asyncio.sleep(0.1) 
            continue

        for line in new_lines:
            if '  [ALL] ' in line or '  [T] ' in line or '  [CT] ' in line:  
                match = re.search(r'\[.*?\]\s(.*?)\s?(?:\[DEAD\])?:', line)
                if match:
                    username = match.group(1).strip()
                    data = line.split(': ', 1)
                    message = data[1].strip() if len(data) > 1 else ""

                    current_time = time.time()
                    if username in user_last_command_time:
                        time_since_last = current_time - user_last_command_time[username]
                        if time_since_last < fishing_delay:
                            if message in ['!fish', '!balance', '!gamble']:
                                remaining_time = fishing_delay - time_since_last
                                print(f"Command ignored for '{username}' wait {int(remaining_time)} seconds.")
                            continue

                    user_last_command_time[username] = current_time

                    if message == '!fish':
                        print(f"Player '{username}' has cast their line!")
                        await cast_line(username) 

                    elif message == '!balance':
                        print(f"Fetching Balance for '{username}'...")
                        await earnings(username)

                    elif message.startswith('!gamble'):
                        try:
                            gamble_parts = message.split(' ')
                            if len(gamble_parts) < 2:
                                    raise ValueError("Missing amount")
                            
                            if gamble_parts[1].lower() == 'all':
                                gamble_amount = get_user(username)['balance']
                            else:
                                gamble_amount = float(gamble_parts[1])
                            
                            if gamble_amount <= 0:
                                write_command(f"say [ERROR] {username}: Please gamble a positive amount.")
                                press_key()
                                continue

                            current_balance = get_user(username)['balance']

                            if current_balance < gamble_amount:
                                write_command(f"say [ERROR] {username}: You don't have enough balance to gamble ${gamble_amount}.Fucking broky XDD")
                                press_key()
                                continue

                            update_user(username, balance=-gamble_amount)
                            await asyncio.sleep(1)
                            symbols, winnings = roll_slot_machine(gamble_amount)
                            net_result = winnings - gamble_amount if winnings > 0 else -gamble_amount
                            update_user(username, balance=max(0, winnings))

                            symbol_display = ' '.join(symbols)
                            if net_result > 0:
                                result_message = (
                                    f"{username} has rolled [{symbol_display}] "
                                    f"and won ${net_result:.2f}!"
                                )
                            elif net_result < 0:
                                result_message = (
                                    f"{username} has rolled [{symbol_display}] "
                                    f"and lost ${abs(net_result):.2f}."
                                )
                            else:
                                result_message = (
                                    f"{username} has rolled [{symbol_display}] "
                                    f"and broke even!"
                                )
                            
                            write_command(f"say [GAMBLE] {username} has pulled the lever on the slot machine...")
                            press_key()
                            await asyncio.sleep(1)
                            write_command(f"say [GAMBLE] {result_message}")
                            press_key()

                        except (ValueError, IndexError):
                            write_command(f"say [ERROR] {username}: Invalid command. Usage: !gamble <amount> or !gamble all if you are feeling lucky")
                            press_key()

        await asyncio.sleep(0.1)



 

if __name__ == "__main__":
    print("Fishing bot is running... Press Ctrl+C to stop.")
    try:
        asyncio.run(handle_chat())
    except KeyboardInterrupt:
        print("Bot stopped.")
