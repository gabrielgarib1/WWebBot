"""
Bot WhatsApp para Gestão de Empresa (4 pessoas)
Funcionalidades: Tarefas, Wiki, Comunicação organizada
"""
#Imports
from whatsapp_bot import EmpresaWhatsAppBot
import schedule
import logging
import selenium.common.exceptions
from inputimeout import inputimeout, TimeoutOccurred

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("WDM").setLevel(logging.WARNING)
# def configurar_horarios(bot):
#     # Schedules all automatic message times
#     # Example: schedule.every().monday.at("09:00").do(bot.weekly_checkin)
#     schedule.every().monday.at("09:00").do(bot.weekly_checkin)
#     schedule.every().friday.at("16:00").do(bot.status_semanal)
#     logging.info("✅ Horários configurados com sucesso! (incluindo troubleshooting)")

def main():
    # Main function to choose between scheduled and manual bot modes
    print("🤖 Iniciando Bot WhatsApp da Empresa...")
    
    # modo = 'schedule'     #'manual' ou 'schedule'
    
    grupos = ["Testes-chatbot"]
    who=grupos[0]
    bot = EmpresaWhatsAppBot(grupos)#mode='test' by default
    print("👍Modo: ",bot.mode)
    print("Arquivo carregado\n", bot.tarefas)
    # Inicializar WhatsApp Web
    if not bot.inicializar_driver():
        print("❌ Erro ao inicializar. Verifique sua conexão.")
        return
        
    try:
        if bot.mode == 'schedule':
            print("🚀 Bot funcionando em modo agendado!")




            print("📱 Mensagens automáticas configuradas:\n")
            print("\n⚠️  Mantenha este programa rodando!")
            while True:
                try:
                    bot.driver.title  # This will raise if browser is closed
                    try:    
                        schedule.run_pending()
                        comando = inputimeout(prompt="> ", timeout=5).strip().lower()
                    except TimeoutOccurred:
                        continue  # Timeout, loop again to check browser statu
                    if comando == 'r':
                        bot.remove_schedule()
                except selenium.common.exceptions.WebDriverException as e:
                    if "invalid session id" in str(e) or "disconnected" in str(e):
                        print("🛑 O navegador foi fechado. Encerrando o bot.")
                        break
                    else:
                        raise
        elif bot.mode == 'test':
            print("🚀 Bot funcionando em modo manual! Digite 's' para enviar uma mensagem de teste ou 'q' para sair.")
            while True:
                try:
                    # Check browser status before waiting for input
                    bot.driver.title
                    # comando = input("> ")
                    try:
                        comando = inputimeout(prompt="> ", timeout=5).strip().lower()
                    except TimeoutOccurred:
                        continue  # Timeout, loop again to check browser statu
                    if comando == 's':
                        success = bot.encontrar_contato(who)
                        if success:
                            # inputimeout(prompt="press enter to send message: ", timeout=5).strip().lower()
                            bot.enviar_mensagem("Mensagem de teste ativada manualmente!")
                        else:
                            print("❌ Erro ao encontrar o grupo de teste.")
                    elif comando == 'q':
                        break
                    else:
                        print("Comando inválido. Digite 'send' ou 'quit'.")
                except selenium.common.exceptions.WebDriverException as e:
                    if "invalid session id" in str(e) or "disconnected" in str(e):
                        print("🛑 O navegador foi fechado. Encerrando o bot.")
                        break
                    else:
                        raise
        else:
            print("❌ Modo inválido selecionado. Saindo.")
    except KeyboardInterrupt:
        print("\n🛑 Bot interrompido pelo usuário")
    except Exception as e:
        logging.error(f"Erro no loop principal: {e}")
    finally:
        if bot.driver:
            bot.driver.quit()
            return

if __name__ == "__main__":
    main()