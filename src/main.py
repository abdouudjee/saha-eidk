
# you get those from https://my.telegram.org/apps
api_id = 123
api_hash = "a hash"
greet="hello!"


import asyncio
import keyboard
from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import User, InputPeerEmpty
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import sys

# ANSI Color Codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


# Reshapes Arabic characters and applies the BiDi algorithm for terminal display.
def fix_text(text: str) -> str:
    return get_display(reshape(text))


with TelegramClient('name', api_id, api_hash) as client:
    
    async def main():
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
            
            print(f"{CYAN}Contact: {contact}|+{phone}{RESET}")
            print("Send this contact a greeting? YES [ENTER] / No [DELETE] / exit [ESCAPE]")
            
            # Block and wait until either Enter or Delete is pressed
            abort = False
            while True:
                # Read a single key down event
                event = keyboard.read_event()
                
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == 'enter':
                        print(f"{GREEN}Greeting sent to {contact}!{RESET}")    
                        await client.send_message(user.id, greet)
                        break
                    elif event.name == 'backspace' or event.name == "delete":
                        print(f"{RED}Skipped.{RESET}")
                        break
                    elif event.name == "esc":
                        print(f"\n{YELLOW}Aborting execution...{RESET}")
                        abort = True
                        break
                # Yield control to allow async tasks to run smoothly
                await asyncio.sleep(0.01)  
            if abort:
                break  
                
    client.loop.run_until_complete(main())