import socket
import time
import sys
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# ── Configurações ──────────────────────────────────────────────────────────────
DEFAULT_START = 2000
DEFAULT_END   = 6000
TIMEOUT       = 0.3
MAX_WORKERS   = 50
# ───────────────────────────────────────────────────────────────────────────────

lock        = Lock()
open_ports  = []
scanned     = 0

# ── Cabeçalho ASCII ────────────────────────────────────────────────────────────
def print_header():
    sys.stdout.write("\033[H\033[J")
    print(r"""
██╗   ██╗ ██████╗ ██╗   ██╗ █████╗ ██████╗  █████╗ 
╚██╗ ██╔╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗
 ╚████╔╝ ██║  ███╗██║   ██║███████║██████╔╝███████║
  ╚██╔╝  ██║   ██║██║   ██║██╔══██║██╔══██╗██╔══██║
   ██║   ╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║  ██║
   ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝

        🔧 YGUARA TOOLS — PORT SCANNER 🔧
    """)
# ───────────────────────────────────────────────────────────────────────────────

def scan_port(ip: str, port: int) -> int | None:
    global scanned
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            result = s.connect_ex((ip, port))
    except Exception:
        result = 1
    with lock:
        scanned += 1
    return port if result == 0 else None


def run_scan(ip: str, start: int, end: int) -> list[int]:
    global open_ports, scanned
    open_ports = []
    scanned    = 0
    ports      = list(range(start, end + 1))
    total      = len(ports)
    last_found: deque = deque(maxlen=5)
    start_time = time.time()

    print_header()
    print(f"\033[1m🔎 Escaneando {ip}  |  portas {start}–{end}  |  threads: {MAX_WORKERS}\033[0m\n")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(scan_port, ip, p): p for p in ports}

        for future in as_completed(futures):
            result = future.result()
            with lock:
                cur_scanned = scanned
                if result:
                    open_ports.append(result)
                    open_ports.sort()
                    last_found.append(result)
                cur_open = list(open_ports)

            percent = (cur_scanned / total) * 100
            filled  = int(percent // 2)
            bar     = "█" * filled + "░" * (50 - filled)

            print_header()
            print(f"\033[1m🔎 Escaneando {ip}  |  portas {start}–{end}  |  threads: {MAX_WORKERS}\033[0m\n")
            print(f"[{bar}] {percent:.1f}%  ({cur_scanned}/{total})")

            elapsed = time.time() - start_time
            rate    = cur_scanned / elapsed if elapsed > 0 else 0
            eta     = (total - cur_scanned) / rate if rate > 0 else 0
            print(f"⚡ {rate:.0f} portas/s  |  ⏱ decorrido: {elapsed:.1f}s  |  ETA: {eta:.1f}s\n")

            print("🔓 Portas abertas encontradas:")
            if cur_open:
                for p in cur_open:
                    print(f"  ✅ {p}")
            else:
                print("  Nenhuma ainda")

            sys.stdout.flush()

    elapsed = time.time() - start_time
    print(f"\n\n{'='*50}")
    print(f"  RESULTADO FINAL — {ip}  |  {start}–{end}")
    print(f"{'='*50}")
    if open_ports:
        for p in open_ports:
            print(f"  🔓 Porta aberta: {p}")
    else:
        print("  Nenhuma porta aberta encontrada.")
    print(f"\n  ⏱ Tempo total: {elapsed:.2f}s  |  {total/elapsed:.0f} portas/s")
    print(f"{'='*50}\n")
    return list(open_ports)


def main():
    print_header()
    ip = input("Digite o IP para escanear: ").strip()

    start_input = input(f"Porta inicial [{DEFAULT_START}]: ").strip()
    end_input   = input(f"Porta final   [{DEFAULT_END}]: ").strip()

    start = int(start_input) if start_input else DEFAULT_START
    end   = int(end_input)   if end_input   else DEFAULT_END

    while True:
        run_scan(ip, start, end)
        again = input("🔄 Escanear novamente? (s/n): ").strip().lower()
        if again != "s":
            print("👋 Encerrando.")
            break


if __name__ == "__main__":
    main()
