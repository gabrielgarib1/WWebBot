#Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
import time
import json
import os
from datetime import datetime, timedelta
import logging
import schedule     


class EmpresaWhatsAppBot:
    def __init__(self, grupos):
        #code variables
        self.driver = None
        #configurations
        self.grupos = grupos
        self.dev_mode = True
        self.scheduled_messages = False 
        #insert an if statement to select OS
        #static data
        self.tarefas = self.carregar_dados('tarefas.json')
        self.processos = self.carregar_dados('processos.json')
        self.clientes = self.carregar_dados('clientes.json')
        self.funcionarios = self.carregar_dados('funcionarios.json')
    def carregar_dados(self, arquivo):
        # Loads data from a JSON file
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        
    def set_mode(self,mode):
        self.dev_mode= mode
        print('You set dev_mode to: ',mode)
        return
    def set_schedule_messages(self,state):
        self.scheduled_messages = state
        
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
            firefox_profile = webdriver.FirefoxProfile(profile_path)

            firefox_options.add_argument("-profile")
            # # firefox_options.add_argument(profile_path)
            # firefox_profile.set_preference("media.navigator.permission.disabled", True)
            # firefox_profile.set_preference("dom.webnotifications.enabled", False)
            # firefox_profile.set_preference("media.autoplay.default", 0)
            # self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
            self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options, firefox_profile=firefox_profile)
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
    
    def encontrar_contato(self, who):
        # Finds and selects a WhatsApp contact or group by name
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

    def enviar_mensagem(self, mensagem, who):
        # Sends a message to the currently open WhatsApp chat
        try:
            message_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            linhas = mensagem.split('\n')
            for i, linha in enumerate(linhas):
                message_box.send_keys(linha)
                if i < len(linhas) - 1:
                    message_box.send_keys('\n')
            send_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
            )
            send_button.click()
            logging.info(f"Mensagem enviada: {mensagem[:50]}...")
            return True
        except Exception as e:
            logging.error(f"Erro ao enviar mensagem: {e}")
            return False
        
    def schedule_message(self, date,time,message,who):
        """
        Schedules a message to be sent at a specific time.
        :param time_str: Time in 'HH:MM' 24-hour format (e.g., '14:30')
        :param who: Name of the contact or group
        :param message: Message to send
        """
    
        schedule.day.at(time).do(self.enviar_mensagem(message,who))


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



    