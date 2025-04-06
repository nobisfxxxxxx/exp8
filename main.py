from instagrapi import Client
import time
import os
from keep_alive import keep_alive

# --- CONFIG ---
SESSION_FILE = "session.json"
REPLY_MESSAGE = "oii massage maat kar warna lynx ki maa shod ke feekkk dunga"
# ---------------

keep_alive()

cl = Client()

if os.path.exists(SESSION_FILE):
    try:
        cl.load_settings(SESSION_FILE)
        cl.login(cl.username, cl.password)
        print("✅ Logged in using session file.")
    except Exception as e:
        print(f"⚠️ Session login failed: {e}")
        exit(1)
else:
    print("❌ Session file not found. Please run the session creation script first.")
    exit(1)

def auto_reply_all_groups():
    while True:
        try:
            threads = cl.direct_threads()
            for thread in threads:
                if thread.inviter is None:
                    continue
                if len(thread.users) > 2:
                    thread_id = thread.id
                    try:
                        thread_data = cl.direct_thread(thread_id)
                        if thread_data is None:
                            print(f"Warning: cl.direct_thread({thread_id}) returned None")
                            continue
                        messages = thread_data.messages
                    except Exception as e:
                        print(f"Error fetching thread {thread_id}: {e}")
                        continue

                    for msg in reversed(messages):
                        if msg.user_id != cl.user_id:
                            try:
                                username = cl.user_info(msg.user_id).username
                                reply = f"@{username} {REPLY_MESSAGE}"
                                cl.direct_send(reply, thread_ids=[thread_id])
                                print(f"Replied to @{username} in group {thread_id}")
                            except Exception as e:
                                print(f"Error replying to message: {e}")
                            break
            time.sleep(10)
        except Exception as e:
            print(f"Main loop error: {e}")
            time.sleep(10)

auto_reply_all_groups()