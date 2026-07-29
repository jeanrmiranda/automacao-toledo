#!/usr/bin/env python3
"""
Conecta em cada switch Huawei, roda 'display vsi' para ver o status geral
das VSIs da lista, depois roda 'display vsi name <nome> verbose' em cada
uma pra detalhar o status (up/down) de cada peer.

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
VLANS = [22, 254, 750, 1008, 1029, 1037, 1051, 1055,
         1060, 1077, 1105, 2120, 2121, 2801, 2810, 3000]

ARQUIVO_IPS = "6730-huawei-ipv4-instalados.txt"
USERNAME = "jean"
PASSWORD = "portugal@1985"


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

        vsis_up = []
        vsis_down = []
        vsis_nao_encontradas = []

        for vlan in VLANS:
            nome = f"tunnel-{vlan}"
            estado = vsis.get(nome)
            if estado is None:
                vsis_nao_encontradas.append(nome)
            elif estado == "up":
                vsis_up.append(nome)
            else:
                vsis_down.append(nome)

        print(f"\n--- VSIs UP ({len(vsis_up)}) ---")
        for nome in vsis_up:
            print(f"  ✅ {nome}")

        print(f"\n--- VSIs DOWN ({len(vsis_down)}) ---")
        for nome in vsis_down:
            print(f"  ❌ {nome}")

        if vsis_nao_encontradas:
            print(f"\n--- Nao encontradas nesse switch ({len(vsis_nao_encontradas)}) ---")
            for nome in vsis_nao_encontradas:
                print(f"  ⚠️  {nome}")

        print("\n--- DETALHE DE PEERS ---")
        for nome in vsis_up + vsis_down:
            saida_verbose = conn.send_command(f"display vsi name {nome} verbose")
            peers = parse_display_vsi_verbose(saida_verbose)

            print(f"\n{nome}:")
            if not peers:
                print("    (nenhum peer encontrado)")
            for peer_ip, estado_peer in peers:
                icone = "✅" if estado_peer == "up" else "❌"
                print(f"    {icone} peer {peer_ip} -> {estado_peer}")

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
