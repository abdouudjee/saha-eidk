
# you get those from https://my.telegram.org/apps
api_id = 123
api_hash = "a hash"
greet="hello!"

import os
import sys
import asyncio
from readchar import readkey, key
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from telethon.sync import TelegramClient
from telethon.tl.types import User, InputPeerEmpty
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.contacts import GetContactsRequest

# ANSI Color Codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"


# Reshapes Arabic characters and applies the BiDi algorithm for terminal display.
def fix_text(text: str) -> str:
    return get_display(reshape(text))


with TelegramClient('name', api_id, api_hash) as client:
    
    async def main():
        
        HISTORY_FILE = "sent_users.txt"
        sent_ids = set()
        
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                sent_ids = {int(line.strip()) for line in f if line.strip()}
        
        
        # Fetch contact list
        result = {}
        contacts_res = await client(GetContactsRequest(hash=0))
        for u in contacts_res.users:
            if isinstance(u, User) and not u.bot and not u.deleted:
                result[u.id] = u
       #fetch active chats 
        active_dialogs = await client(GetDialogsRequest(offset_date=None, offset_id=0, offset_peer=InputPeerEmpty(), limit=100, hash=0, folder_id=0))
        for u in active_dialogs.users:
            if isinstance(u, User) and not u.bot and not u.deleted:
                result[u.id] = u
    
       #fetch archived chats            
        archived_dialogs = await client(GetDialogsRequest(offset_date=None, offset_id=0, offset_peer=InputPeerEmpty(), limit=100, hash=0, folder_id=1))
        for u in archived_dialogs.users:
            if isinstance(u, User) and not u.bot and not u.deleted:
                result[u.id] = u
                
        # Force standard output to support UTF-8 formatting explicitly
        sys.stdout.reconfigure(encoding='utf-8')
        
        
        for user_id, user in result.items():
            first_name = user.first_name or ""
            last_name = user.last_name or ""
            full_name = f"{first_name} {last_name}".strip() or "Unknown Contact"
        
            phone = user.phone or "No Phone"
            contact = fix_text(full_name)
            if user_id in sent_ids:
                status_tag = f"{MAGENTA}[ALREADY SENT]{RESET} "
                prompt_msg = "Resend the greeting? YES [ENTER] / No [DELETE] / exit [ESCAPE]"
            else:
                status_tag = ""
                prompt_msg = "Send this contact a greeting? YES [ENTER] / No [DELETE] / exit [ESCAPE]"
            
            print(f"{status_tag}{CYAN}Contact: {contact}|+{phone}{RESET}")
            print(prompt_msg)
            
            # Block and wait until either Enter or Delete is pressed
            abort = False
            while True:
                # Read a single key down event
                k = readkey()

                if k == key.ENTER:
                    print(f"{GREEN}Greeting sent to {contact}!{RESET}")    
                    await client.send_message(user.id, greet)
                    # Append the user ID to tracking file if they weren't in it yet
                    if user_id not in sent_ids:
                        sent_ids.add(user_id)
                        with open(HISTORY_FILE, "a") as f:
                            f.write(f"{user_id}\n")
                    break
                elif k == key.BACKSPACE or k == key.DELETE:
                    print(f"{RED}Skipped.{RESET}")
                    break
                elif k == key.ESC:
                    print(f"\n{YELLOW}Aborting execution...{RESET}")
                    abort = True
                    break
                # Yield control to allow async tasks to run smoothly
                await asyncio.sleep(0.01)  
            if abort:
                break  
                
    client.loop.run_until_complete(main())