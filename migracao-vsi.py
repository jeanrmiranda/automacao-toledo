
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

    "vsi tunnel-19",
    "description Mgmt: TELEFONIA",
    "pwsignal ldp",
    "vsi-id 19",
    "flow-label both",
    "peer 172.16.11.100",
    "mtu 1600",
    "quit",
    "interface Vlanif 19",
    "description Mgmt: TELEFONIA",
    "l2 binding vsi tunnel-19",
    "quit",

    "vsi tunnel-22",
    "description Mgmt: Cameras SEGURANCA Toledo",
    "pwsignal ldp",
    "vsi-id 22",
    "flow-label both",
    "peer 172.16.11.100",
    "mtu 1600",
    "quit",
    "interface Vlanif22",
     "description Mgmt: Cameras SEGURANCA Toledo",
    "l2 binding vsi tunnel-22",
    "quit",

    "vsi tunnel-25",
     "description Mgmt: rede corportativa Toledo",
    "pwsignal ldp",
    "vsi-id 25",
    "flow-label both",
    "peer 172.16.11.100",
    "mtu 1600",
    "quit",
    "interface Vlanif25",
    "description Mgmt: rede corportativa Toledo",
    "l2 binding vsi tunnel-25",
    "quit",

    "vsi tunnel-254",
    "description Mgmt: GERENCIA OLT HUAWEI",
    "pwsignal ldp",
    "vsi-id 254",
    "flow-label both",
    "peer 172.16.11.100",
    "mtu 1600",
    "quit",
    "interface Vlanif254",
    "description Mgmt: GERENCIA OLT HUAWEI",
    "l2 binding vsi tunnel-254",
    "quit",

    "vsi tunnel-80",
    "description Mgmt: DM-SW TOLEDO GERENCIA",
    "pwsignal ldp",
    "vsi-id 80",
    "flow-label both",
    "peer 172.16.11.100",
    "mtu 1600",
    "quit",
    "interface Vlanif80",
    "description Mgmt: DM-SW TOLEDO GERENCIA",
    "l2 binding vsi tunnel-80",
    "quit",

    "vsi tunnel-81",
    "description Mgmt: DM-SW B2B CLIENTE",
    "pwsignal ldp",
    "vsi-id 81",
    "flow-label both",
    "peer 172.16.11.100",
    "mtu 1600",
    "quit",
    "interface Vlanif81",
    "description Mgmt: DM-SW B2B CLIENTE",
    "l2 binding vsi tunnel-81",
    "quit",

    "vsi tunnel-84",
    "description Mgmt: gerencia MONITORY TOLEDO",
    "pwsignal ldp",
    "vsi-id 84",
    "flow-label both",
    "peer 172.16.11.100",
    "mtu 1600",
    "quit",
    "interface Vlanif84",
    "description Mgmt: gerencia MONITORY TOLEDO",
    "l2 binding vsi tunnel-84",
    "quit",
]

# Roda para cada IP
for ip in lista_ips:
    enviar_comandos_ssh(ip, username, password, comandos)
