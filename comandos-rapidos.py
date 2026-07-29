
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException
import sys

COMANDOS_LENTOS = {"save", "reset counters interface"}


def enviar_comandos_ssh(ip, username, password, comandos):
    device = {
        "device_type": "huawei",
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
        for cmd in comandos:
            cmd_formatado = cmd.replace("{ip}", ip)
            timeout_cmd = 15 if cmd_formatado in COMANDOS_LENTOS else 3

            resposta = conn.send_command_timing(
                cmd_formatado,
                read_timeout=timeout_cmd,
                strip_prompt=False,
                strip_command=False,
            )
            output_total = resposta

            # Verifica SÓ a resposta mais recente (não o texto acumulado)
            while "[Y/N]" in resposta or "(y/n)" in resposta.lower():
                resposta = conn.send_command_timing(
                    "y",
                    read_timeout=timeout_cmd,
                    strip_prompt=False,
                    strip_command=False,
                )
                output_total += resposta

            print(f"[{ip}] >> {cmd_formatado}")
            print(output_total)

        print(f"✅ Finalizado: {ip}")

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


# IPs e credenciais
lista_ips = ler_ips_arquivo('6730-huawei-ipv4-instalados.txt')
username = "jean"
password = "portugal@1985"

# Lista dos comandos (sem os "y" manuais - agora é automático)
comandos = [
    "system-view",

    "snmp-agent community read prtg@toledo",
    "quit",
]

# Roda para cada IP
for ip in lista_ips:
    enviar_comandos_ssh(ip, username, password, comandos)
