
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException
import sys
import os
from datetime import datetime

def enviar_comandos_ssh(ip, username, password, comandos):
    device = {
        "device_type": "alcatel_sros",
        "host": ip,
        "username": username,
        "password": password,
        "timeout": 10,
    }

    try:
        conn = ConnectHandler(**device)
        print(f"\n✅ Conectado com sucesso ao {ip}")
    except NetmikoAuthenticationException:
        print(f"❌ Falha de autenticação ao conectar ao {ip}.")
        return
    except NetmikoTimeoutException:
        print(f"❌ Timeout ao conectar ao {ip}.")
        return
    except Exception as e:
        print(f"❌ Erro ao conectar ao {ip}: {str(e)}")
        return

    try:
        output_hostname = conn.send_command("show system information", read_timeout=10)

        hostname = "unknown-host"
        for line in output_hostname.splitlines():
            if "System Name" in line:
                hostname = line.split(":")[1].strip()
                break
        print(f"📛 Hostname detectado: {hostname}")

        datahora = datetime.now().strftime("%Y%m%d-%H%M")
        saida_completa = f"### Comando: show system information\n{output_hostname}"

        for cmd in comandos:
            cmd_formatado = cmd.replace("{ip}", ip)
            output = conn.send_command_timing(cmd_formatado, read_timeout=10)

            # Trata prompt de confirmação Y/N, caso apareça
            if "(y/n)" in output.lower() or "[y/n]" in output.lower():
                output += conn.send_command_timing("y")

            print(f"[{ip}] >> {cmd_formatado}")
            print(output)
            saida_completa += f"\n\n### Comando: {cmd_formatado}\n{output}"

        caminho_backup = f"/home/jtech/backup-routers/{hostname}-{ip}-{datahora}.txt"
        with open(caminho_backup, 'w', encoding='utf-8') as f:
            f.write(saida_completa)

        print(f"✅ Backup salvo em {caminho_backup}")

    except Exception as e:
        print(f"❌ Erro ao enviar comandos para {ip}: {str(e)}")

    conn.disconnect()


def ler_ips_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            ips = [linha.strip() for linha in arquivo if linha.strip()]
            if not ips:
                print("❌ Arquivo de IPs está vazio.")
                sys.exit(1)
            return ips
    except FileNotFoundError:
        print(f"❌ Arquivo {nome_arquivo} não encontrado.")
        sys.exit(1)


if not os.path.exists('/home/jtech/backup-routers/'):
    os.makedirs('/home/jtech/backup-routers/')

lista_ips = ler_ips_arquivo('/home/jtech/script-huawei/7750-nokia-ipv4.txt')
username = "jean"
password = "yCpv9tj9"

comandos = [
    "admin save",
    "environment no more",
    "admin display-config",
]

for ip in lista_ips:
    enviar_comandos_ssh(ip, username, password, comandos)
