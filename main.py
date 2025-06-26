"""
Bot WhatsApp para Gestão de Empresa (4 pessoas)
Funcionalidades: Tarefas, Wiki, Comunicação organizada
"""
#Imports
from whatsapp_bot import EmpresaWhatsAppBot
import schedule
import logging
# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logging.getLogger("WDM").setLevel(logging.WARNING)
def configurar_horarios(bot):
    # Schedules all automatic message times
    # Example: schedule.every().monday.at("09:00").do(bot.weekly_checkin)
    schedule.every().monday.at("09:00").do(bot.weekly_checkin)
    schedule.every().friday.at("16:00").do(bot.status_semanal)
    logging.info("✅ Horários configurados com sucesso! (incluindo troubleshooting)")

def main():
    # Main function to choose between scheduled and manual bot modes
    print("🤖 Iniciando Bot WhatsApp da Empresa...")
    
    # modo = 'schedule'     #'manual' ou 'schedule'
    modo = 'manual'
    print("👍Modo: ", modo)
    grupos = {"test": "Bot testes"}
    bot = EmpresaWhatsAppBot(grupos)
    
    # Inicializar WhatsApp Web
    if not bot.inicializar_driver():
        print("❌ Erro ao inicializar. Verifique sua conexão.")
        return
        
    try:
        if modo == 'schedule':
            configurar_horarios(bot)
            print("🚀 Bot funcionando em modo agendado!")
            print("📱 Mensagens automáticas configuradas:\n")
            print("   • 09:00 - Check-in semanal")
            print("   • 16:00 - Relatório semanal (Sexta)")
            print("\n⚠️  Mantenha este programa rodando!")
            print("🛑 Pressione Ctrl+C para parar")
            while True:
                schedule.run_pending()
        elif modo == 'manual':
            print("🚀 Bot funcionando em modo manual! Digite 'send' para enviar uma mensagem de teste ou 'quit' para sair.")
            while True:
                comando = input("> ").strip().lower()
                if comando == 'send':
                    success = bot.encontrar_contato(bot.grupos[0])
                    if success:
                        bot.enviar_mensagem("Mensagem de teste ativada manualmente!")
                    else:
                        print("❌ Erro ao encontrar o grupo de teste.")
                elif comando == 'quit':
                    break
                else:
                    print("Comando inválido. Digite 'send' ou 'quit'.")
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