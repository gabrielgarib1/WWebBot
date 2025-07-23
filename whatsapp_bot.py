#Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
import time
import json
import os
from datetime import datetime, timedelta
import logging
import schedule     


class CompanyWhatsAppBot:   
    def __init__(self, groups, mode='test'):

        #code variables
        self.driver = None
        self.message_id=0

        #configurations
        self.set_mode(mode)
        
        #dinamic data
        self.scheduled_list = [] #lista de dicionários de mensagens agendadas
        #static data
        self.groups = groups #limita o acesso a grupos específicos em lista
        data_files = ["tarefas", "processos", "clientes", "funcionarios"]
        self.create_db(data_files)        
        

    def create_db(self, list_json, db_name='DB_enterprise'):
        dbfolder_path = os.path.join(os.getcwd(), db_name)
        os.makedirs(dbfolder_path, exist_ok=True)
        self.db_path = dbfolder_path  # Salva o caminho para uso posterior
        for file in list_json:
            path = os.path.join(dbfolder_path, file + ".json")
            # Cria o arquivo se não existir
            if not os.path.exists(path):
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump({}, f, indent=2, ensure_ascii=False)
            # Carrega o conteúdo do arquivo (ou dicionário vazio) em self.<file>
            with open(path, 'r', encoding='utf-8') as f:
                setattr(self, file, json.load(f))
                
    def set_mode(self, mode):
        self.mode = mode
        return
        
    def save_data(self, data, file):
        # Saves data to a JSON file
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def initialize_driver(self, profile_path=os.getcwd()):
        # Initializes and configures the Firefox WebDriver for WhatsApp Web
        #switch between two service options based on OS
        try:
            firefox_options = webdriver.FirefoxOptions()
            profile_path += "/User_Data"
            # # Create directory if it doesn't exist
            os.makedirs(profile_path, exist_ok=True)    
            firefox_options.add_argument(f'-profile')
            firefox_options.add_argument(profile_path)
            # firefox_options.add_argument(f"user-data-dir={profile_path}")
            firefox_options.set_preference("media.navigator.permission.disabled", True)#disable permission prompts
            firefox_options.set_preference("dom.webnotifications.enabled", False)#disable notification popus
            firefox_options.set_preference("media.autoplay.default", 0)#allows all media to autoplay
            firefox_options.set_preference("permissions.default.microphone", 2)  # Block microphone
            firefox_options.set_preference("permissions.default.camera", 2)      # Block camera
            firefox_options.set_preference("permissions.default.desktop-notification", 2)  # Block notifications
            firefox_options.set_preference("privacy.donottrackheader.enabled", True)       # Enable Do Not Track
            firefox_options.set_preference("browser.download.folderList", 2)               # Use custom download dir
            # firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  # Auto-download PDFs
            firefox_options.set_preference("pdfjs.disabled", True)                         # Disable built-in PDF viewer

            # self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
            self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), 
                                            options=firefox_options)
            self.driver.get('https://web.whatsapp.com/')
            print("🚀 Initializing WhatsApp Web with Firefox...")
            print("📱 If this is the first login for this profile, scan the QR Code with your phone.")
            print("⏰ Waiting for login...")
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            print("✅ Login successful!")
            return True
        except Exception as e:
            logging.error(f"³Error initializing driver: {e}")    
            return False
    
    def find_contact(self, who):
        # Finds and selects a WhatsApp contact or group by name
        if who in self.groups:
            try:
                search_box = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
                )
                search_box.clear()
                search_box.send_keys(who)
                contact = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f'//span[@title="{who}"]'))
                )
                contact.click()
                return True
            except Exception as e:
                logging.error(f"³Error finding contact {who}: {e}")
                return False
        else:
            logging.error("³Contact is not enabled to receive messages.")

    def send_message(self, message):
        # Sends a message to the currently open WhatsApp chat
        try:
            message_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            message_box.click()  # Ensure the box is focused
            for char in message:
                message_box.send_keys(char)
                # time.sleep(0.01)  # Small delay can help with reliability
            message_box.send_keys(Keys.ENTER)
            logging.info(f"³Message sent: {message}...")
            return True
        except Exception as e:
            logging.error(f"³Error sending message: {e}")
            return False
        
    def schedule_message_datetime(self, date, time, message, who,print_info=False,everyday=False):
        """
        Schedules a message to be sent at a specific time.
        :param date_str: Date in 'YYYY-MM-DD' format (e.g., '2024-07-20')
        :param time_str: Time in 'HH:MM' 24-hour format (e.g., '14:30')
        :param who: Name of the contact or group
        :param message: Message to send
        """
        
        
        def automate_send():
            self.find_contact(who)
            self.send_message(message)
            if not everyday:
            #se everyday=True, irá mandar a mensagem todo dia 
                return schedule.CancelJob
        schedule.every().day.at(time).do(automate_send).tag(date,time,message).tag(id)
        self.scheduled_list.append({"ID":self.message_id,"Datetime":date+" "+ time ,"Message":message, "Who": who})
        self.message_id+=1
        
        if print_info:
            logging.info(f"³Message scheduled: {message}...")
            # print("INFO - Message scheduled to: ",time,", ",date)


    def schedule_message_timer(self, timer,message, who, print_info=False):
        # timer são minutes antes de mandar a mensagem
        #datetime.now() retorna YYYY-MM-DD HH:MM:SS.\mu_seconds (6 casas decimais)
        send_time = (datetime.now() + timedelta(minutes=timer))  #formato aceito por schedule é HH:MM:SS 
        
    
    def remove_schedule(self,tag_id='', all=False):
        """
        remove mensagens agendadas, no while loop, dado um id tag(schedule)
        inicializado com o ponteiro mensagem
        """
        if all:
            schedule.clear()
            self.scheduled_list.clear()
            #remove a all messages
        elif not all: 
            schedule.clear(tag_id)
            #loop nao funciona, deleta mais de uma(ainda nao sei quais está deletando)
            for index in range(len(self.scheduled_list)):
                for dict in self.scheduled_list:
                    if dict["ID"]==tag_id:
                        self.scheduled_list.pop(index)
                        break
          

            #remove a certain message
    def generate_ai_message(self,context):
        """
        use api AI to generate message
        """
        AImessage="... in development"
        return AImessage
    # def meeting_reminder(self, time, subject):
    #     # Sends a meeting reminder message to the operational group
    #     message = f"""📅 MEETING REMINDER

    #     ⏰ Time: {time}
    #     📋 Subject: {subject}
    #     📍 Location: Meeting room

    #     Confirm attendance: 👍 = Yes | 👎 = No"""
    #     if self.find_contact(self.groups[0]):
    #         self.send_message(message)

    def consult_process(self, process_name):   
        '''
        pass implementation, maybe can be a consulter for links in a chat group 
        for machine - use for obtaining any info
        '''
        pass         

    def add_task(self, user, description):
        '''weekly_checkin
        Another mathod to a future implementation of chat user - machine
        '''
        pass

    def list_pending_tasks(self):
        '''
        Another mathod to a future implementation of chat user - machine
        '''
        pass

    def process_received_messages(self):
        ''' Method very simple, maybe a set of methods will do this'''
        pass



