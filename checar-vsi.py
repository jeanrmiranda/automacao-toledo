#!/usr/bin/env python3
"""
Conecta em cada switch Huawei, roda 'display vsi' para pegar TODAS as VSIs
do equipamento (up e down), depois roda 'display vsi name <nome> verbose'
em cada VSI que estiver UP para checar se algum peer dela esta down.

Ao final, imprime por switch:
  - Lista de VSIs UP
  - Lista de VSIs DOWN
  - Lista de VSIs UP que tem peer(s) DOWN

Uso:
  python3 check_vsi_status.py

Requisitos:
  pip install netmiko --break-system-packages
"""

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException
import re
import sys

# ------------------------------------------------------------------
# EDITE AQUI
# ------------------------------------------------------------------
ARQUIVO_IPS = "6730-huawei-ipv4-instalados.txt"
USERNAME = "jean"
PASSWORD = "SUA_SENHA_AQUI"


def parse_display_vsi(output):
    """
    Parseia a saida de 'display vsi' e retorna dict {vsi_name: state}
    Linha exemplo:
    tunnel-254    --   ldp   unqualify vlan   1600  up
    """
    vsis = {}
    for linha in output.splitlines():
        linha = linha.strip()
        m = re.match(r'^(tunnel-\d+)\s+.*\s+(up|down)\s*$', linha)
        if m:
            vsis[m.group(1)] = m.group(2)
    return vsis


def parse_display_vsi_verbose(output):
    """
    Parseia a saida de 'display vsi name X verbose' e retorna lista
    de tuplas (peer_ip, session_state).
    """
    peers = []
    peer_ip_atual = None
    for linha in output.splitlines():
        linha = linha.strip()

        m_ip = re.match(r'\*Peer Router ID\s*:\s*(\S+)', linha)
        if m_ip:
            peer_ip_atual = m_ip.group(1)
            continue

        m_session = re.match(r'Session\s*:\s*(\S+)', linha)
        if m_session and peer_ip_atual:
            peers.append((peer_ip_atual, m_session.group(1)))
            peer_ip_atual = None

    return peers


def checar_switch(ip, username, password):
    device = {
        "device_type": "huawei",
        "host": ip,
        "username": username,
        "password": password,
        "timeout": 10,
    }

    print(f"\n{'=' * 70}")
    print(f"Switch: {ip}")
    print("=" * 70)

    try:
        conn = ConnectHandler(**device)
        print(f"✅ Logado com sucesso em {ip}")
    except NetmikoAuthenticationException:
        print(f"❌ Falha de autenticacao em {ip}")
        return
    except NetmikoTimeoutException:
        print(f"❌ Timeout ao conectar em {ip}")
        return
    except Exception as e:
        print(f"❌ Erro ao conectar em {ip}: {e}")
        return

    try:
        saida_vsi = conn.send_command("display vsi")
        vsis = parse_display_vsi(saida_vsi)

        # Loop por TODAS as VSIs encontradas no display vsi (sem filtro de lista fixa)
        vsis_up = [nome for nome, estado in vsis.items() if estado == "up"]
        vsis_down = [nome for nome, estado in vsis.items() if estado == "down"]

        # Para cada VSI up, checa o verbose e guarda quais peers estao down
        vsis_up_com_peer_down = {}
        for nome in vsis_up:
            saida_verbose = conn.send_command(f"display vsi name {nome} verbose")
            peers = parse_display_vsi_verbose(saida_verbose)
            peers_down = [p for p, estado_peer in peers if estado_peer != "up"]
            if peers_down:
                vsis_up_com_peer_down[nome] = peers_down

        # ---------------- RESUMO FINAL ----------------
        print(f"\n--- VSIs UP ({len(vsis_up)}) ---")
        for nome in sorted(vsis_up):
            print(f"  ✅ {nome}")

        print(f"\n--- VSIs DOWN ({len(vsis_down)}) ---")
        for nome in sorted(vsis_down):
            print(f"  ❌ {nome}")

        print(f"\n--- VSIs UP mas com peer(s) DOWN ({len(vsis_up_com_peer_down)}) ---")
        for nome in sorted(vsis_up_com_peer_down):
            peers_down = vsis_up_com_peer_down[nome]
            print(f"  ⚠️  {nome}: peer(s) down -> {', '.join(peers_down)}")

    except Exception as e:
        print(f"❌ Erro ao processar comandos em {ip}: {e}")

    finally:
        conn.disconnect()


def ler_ips_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, "r") as arquivo:
            ips = [linha.strip() for linha in arquivo if linha.strip()]
            if not ips:
                print("❌ Arquivo de IPs esta vazio.")
                sys.exit(1)
            return ips
    except FileNotFoundError:
        print(f"❌ Arquivo {nome_arquivo} nao encontrado.")
        sys.exit(1)


def main():
    lista_ips = ler_ips_arquivo(ARQUIVO_IPS)

    for ip in lista_ips:
        checar_switch(ip, USERNAME, PASSWORD)


if __name__ == "__main__":
    main()
