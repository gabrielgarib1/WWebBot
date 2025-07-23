"""
Bot WhatsApp para Gestão de Empresa (4 pessoas)
Funcionalidades: Tarefas, Wiki, Comunicação organizada
"""
# Imports
from whatsapp_bot import CompanyWhatsAppBot
import schedule
import logging
import selenium.common.exceptions
from inputimeout import inputimeout, TimeoutOccurred
import json

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("WDM").setLevel(logging.WARNING)
def main():
    # Main function to choose between scheduled and manual bot modes
    print("🤖 Starting Company WhatsApp Bot...")
    groups = ["Testes-chatbot"]
    who = groups[0] #configure to use just one group for testing
    bot = CompanyWhatsAppBot(groups)  # mode='test' by default
    bot.set_mode('schedule')     #default='manual' or 'schedule'
    print("👍Mode: ", bot.mode)
    # print("Loaded file\n", bot.tarefas)
    # Initialize WhatsApp Web
    if not bot.initialize_driver():
        print("❌ Error initializing. Check your connection.")
        return
        
    try:
        if bot.mode == 'schedule':
            print("🚀 Bot running in scheduled mode!")
            print("📱 Automatic messages configured:\n")
            print("\n⚠️  Keep this program running!")
            while True:
                try:
                    bot.driver.title  # This will raise if browser is closed
                    try:    
                        schedule.run_pending()
                        command = inputimeout(prompt="Enter command: \n > ", timeout=10).strip().lower()
                    except TimeoutOccurred:
                        continue  # Timeout, loop again to check browser status
                    match command:
                        case 's':
                            # message=input("\nType message:\n")
                            # date=input("\nType date(YYYY-MM-DD): \n")
                            # time=input("\nType time(HH:MM 24-hour format): \n")
                            message="test message scheduled"
                            date="2025-07-23"
                            time="16:21:20"
                            bot.schedule_message_datetime(date,time,message,who,print_info=True)
                        case 't':#nao implementado
                            timer=15
                            bot.schedule_message_timer(timer,message,who,print_info=True)
                        case 'd':   #implementar detecção de lista de schedule vazia
                            while True:
                                try:
                                    index_to_remove= inputimeout(prompt="   Enter index of the message to be removed: \n>",
                                                         timeout=5).strip().lower()
                                    index_to_remove=int(index_to_remove)
                                    # print("tipo: ",type(index_to_remove),"\n valor: ",index_to_remove,
                                    #       "\n first condition: ",index_to_remove>=0,"\n second condition: "
                                    #       , index_to_remove<bot.message_id,"\n")
                                    if index_to_remove>=0 and index_to_remove<bot.message_id:
                                        print("worked")
                                        bot.remove_schedule(index_to_remove)#não está funcionando
                                        break
                                    else:
                                        print("\n   Index don't exist. Please insert a valid index or 'q' to back to menu.\n")
                                        continue
                                except TimeoutOccurred:
                                    break   
                                except:
                                    if index_to_remove=='q':
                                        break
                                    else:
                                        print("\n   Not valid. Please insert a valid index or 'q' to back to menu.\n")
                                        continue   
                        case 'l':
                            print("\n Number of scheduled messages: ",len(bot.scheduled_list))
                            for dicts in bot.scheduled_list:
                                print(dicts)
                                # print(json.dumps(dicts,indent=4))
                        case 'c':
                            bot.remove_schedule(all=True)
                        case 'q':
                            break
                        case _:
                            print("Invalid command. Type:\n" \
                            "1. 's' to datetime scheduled  message\n" \
                            "2. 't' to timer scheduled message \n" \
                            "3. 'd' to delete a scheduled messages\n" \
                            "4. 'l' to list all scheduled messages\n"
                            "5. 'c' to clear all scheduled messages\n"
                            "6. 'q' to quit.\n")
                except selenium.common.exceptions.WebDriverException as e:
                    if "invalid session id" in str(e) or "disconnected" in str(e) or "marionette" in str(e):
                        print("🛑 The browser was closed. Shutting down the bot.")
                        break
                    else:
                        raise
        elif bot.mode == 'test':
            print("🚀 Bot running in test mode!")
            while True:
                try:
                    # Check browser status before waiting for input
                    bot.driver.title
                    try:
                        command = inputimeout(prompt="Enter command: \n> ", timeout=10).strip().lower()
                    except TimeoutOccurred:
                        continue  # Timeout, loop again to check browser status
                    match command:
                        case 's':
                            success = bot.find_contact(who)
                            if success:
                                # inputimeout(prompt="press enter to send message: ", timeout=5).strip().lower()
                                bot.send_message("Mensagem de teste ativada manualmente!")
                            else:
                                print("❌ Error finding the test group.")
                        case 'q':
                            break
                        case _:
                            print("Invalid command. Type:\n" \
                            "1. 's' to send a test message\n " \
                            "2. 'q' to quit.\n")
                except selenium.common.exceptions.WebDriverException as e:
                    if "invalid session id" in str(e) or "disconnected" in str(e) or "marionette" in str(e):
                        print("🛑 The browser was closed. Shutting down the bot.")
                        break
                    else:
                        raise
        else:
            print("❌ Invalid mode selected. Exiting.")
    except KeyboardInterrupt:
        print("\n🛑 Bot interrupted by user")
    except Exception as e:
        logging.error(f"Error in main loop: {e}")
    finally:
        if bot.driver:
            bot.driver.quit()
            return

if __name__ == "__main__":
    main()