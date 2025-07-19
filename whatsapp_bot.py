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


class EmpresaWhatsAppBot:
    def __init__(self, grupos,mode='test'):

        #code variables
        self.driver = None

        #configurations
        self.set_mode(mode)
        self.grupos = grupos #limita o acesso a grupos específicos

        #static data
        # self.bd_path =os.getcwd(), "BD_enterprise")# Ensure BD_enterprise folder exists
        datas=["tarefas","processos","clientes","funcionarios"]
        self.criar_bd(datas)        
        # self.tarefas = self.carregar_dados('tarefas.json')
        # self.processos = self.carregar_dados('processos.json')
        # self.clientes = self.carregar_dados('clientes.json')
        # self.funcionarios = self.carregar_dados('funcionarios.json')


    def criar_bd(self, list_json, bd_name='BD_enterprise'):
        bdfolder_path = os.path.join(os.getcwd(), bd_name)
        os.makedirs(bdfolder_path, exist_ok=True)
        self.bd_path = bdfolder_path  # Salva o caminho para uso posterior
        for file in list_json:
            path = os.path.join(bdfolder_path, file + ".json")
            # Cria o arquivo se não existir
            if not os.path.exists(path):
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump({}, f, indent=2, ensure_ascii=False)
            # Carrega o conteúdo do arquivo (ou dicionário vazio) em self.<file>
            with open(path, 'r', encoding='utf-8') as f:
                setattr(self, file, json.load(f))
                
    def set_mode(self,mode):
        self.mode= mode
        print('You set mode to: ',mode)
        return
        
    def salvar_dados(self, dados, arquivo):
        # Saves data to a JSON file
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

    def inicializar_driver(self,profile_path=os.getcwd()):
        # Initializes and configures the Firefox WebDriver for WhatsApp Web
        #switch between two service options based on OS
        try:
            firefox_options = webdriver.FirefoxOptions()
            profile_path+="/User_Data"
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
            print("🚀 Inicializando WhatsApp Web com Firefox...")
            print("📱 Se for o primeiro login neste perfil, escaneie o QR Code com seu celular.")
            print("⏰ Aguardando login...")
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            print("✅ Login realizado com sucesso!")
            return True
        except Exception as e:
            logging.error(f"Erro ao inicializar driver: {e}")    
            return False
    
    def encontrar_contato(self,who):
        # Finds and selects a WhatsApp contact or group by name
        if who in self.grupos:
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
                logging.error(f"Erro ao encontrar contato {who}: {e}")
                return False
        else:
            logging.error("Contato não foi habilitado para enviar mensagens.")

    def enviar_mensagem(self, mensagem):
        # Sends a message to the currently open WhatsApp chat
        try:
            message_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            message_box.click()  # Ensure the box is focused
            for char in mensagem:
                message_box.send_keys(char)
                # time.sleep(0.01)  # Small delay can help with reliability
            message_box.send_keys(Keys.ENTER)
            logging.info(f"Mensagem enviada: {mensagem}...")
            return True
        except Exception as e:
            logging.error(f"Erro ao enviar mensagem: {e}")
            return False
        
    def schedule_message(self, date,time,message,who):
        """
        Schedules a message to be sent at a specific time.
        :param date_str: Date in 'YYYY-MM-DD' format (e.g., '2024-07-20')
        :param time_str: Time in 'HH:MM' 24-hour format (e.g., '14:30')
        :param who: Name of the contact or group
        :param message: Message to send
        """
    
        schedule.day.at(time).do(self.enviar_mensagem(message,who))
    def remove_schedule(self,all=False):
        if all:
            pass
            #remove a all messages
        elif  not all: 
            pass
            #remove a certain message

    # def lembrete_reuniao(self, horario, assunto):
    #     # Sends a meeting reminder message to the operational group
    #     mensagem = f"""📅 LEMBRETE DE REUNIÃO

    #     ⏰ Horário: {horario}
    #     📋 Assunto: {assunto}
    #     📍 Local: Sala de reunião

    #     Confirmem presença: 👍 = Sim | 👎 = Não"""
    #     if self.encontrar_contato(self.grupos[0]):
    #         self.enviar_mensagem(mensagem)


    def consultar_processo(self, nome_processo):   
        '''
        pass implementation, maybe can be a consulter for links in a chat group 
        for machine - use for obtaining any info
        '''
        pass         


    def adicionar_tarefa(self, usuario, descricao):
        '''weekly_checkin
        Another mathod to a future implementation of chat user - machine
        '''
        pass


    def listar_tarefas_pendentes(self):
        '''
        Another mathod to a future implementation of chat user - machine
        '''
        pass


    def processar_mensagens_recebidas(self):
        ''' Method very simple, maybe a set of methods will do this'''
        pass



