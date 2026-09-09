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
lista_ips = ler_ips_arquivo('6750-huawei-ipv4-instalados.txt')
username = "jean"
password = "portugal@1985"
backup_password = '''%+%##!!!!!!!!!"!!!!"!!!!*!!!!7LTnVOK_g:%'3B3xh$N,'DuuUzGzuUQV8k4!!!!!2jp5!!!!!!>!!!!i6>#2k$g^MVd4$GsFcK1>9x1.4m|^6'g3TQs\*n>%+%#'''

# Lista dos comandos (sem os "y" manuais - agora é automático)
comandos = [
    "system-view",
    "undo lldp enable",
    "clock timezone Brasilia minus 03:00:00",
    "y",
    "bfd",
    "quit",
    "info-center loghost 10.0.18.120 source-ip {ip} local-time",
    "dns server 177.84.108.138",
    "dns server 177.84.108.139",
    "lnp disable",
    "stp disable",
    "router id {ip}",
    "aaa",
    "local-user jtechsupport user-group manage-ug",
    "y",
    "local-user jtechsupport service-type telnet terminal ssh ftp http",
    "y",
    "local-user jtechsupport password ",
    "Batman@123@RobiN",
    "Batman@123@RobiN",
    "local-user jeanrmiranda user-group manage-ug",
    "y",
    "local-user jeanrmiranda service-type telnet terminal ssh ftp http",
    "y",
    "local-user jeanrmiranda password ",
    "Batman@123@RobiN",
    "Batman@123@RobiN",
    "quit",
    "ssh server cipher aes256_ctr aes128_ctr",
    "ssh server hmac sha2_256",
    "ssh client key-exchange dh_group_exchange_sha256 dh_group_exchange_sha1 dh_group14_sha1 dh_group16_sha512 curve25519_sha256",
    "y",
    "ssh client cipher aes256_ctr aes128_ctr",
    "ssh client hmac sha2_256",
    "ssh server publickey rsa rsa_sha2_512 rsa_sha2_256",
    "ssh server-source all-interface",
    "y",
    "ntp ipv6 server disable",
    "y",
    "ntp server disable",
    "y",
    "ntp server source-interface all disable",
    "y",
    "ntp ipv6 server source-interface all disable",
    "y",
    "undo ntp unicast-peer 172.16.11.5",
    "y",
    "undo ntp unicast-peer 10.0.18.110",
    "y",
    "ntp unicast-peer 10.0.18.140",
    "y",
    "ntp unicast-peer 10.0.18.141",
    "y",
    "ntp server source-interface LoopBack0",
    "y",
    "undo ssh user bolin",
    "ospf 1 router-id {ip}",
    "opaque-capability enable",
    "enable traffic-adjustment",
    "frr",
    "loop-free-alternate",
    "bfd all-interfaces enable",
    "bfd all-interfaces detect-multiplier 3 min-rx-interval 100 min-tx-interval 100",
    "area 0.0.0.0",
    "mpls-te enable",
    "network {ip} 0.0.0.0 description Loopback",
    "quit",
    "quit",
    "undo acl number 2000",
    "acl number 2000",
    "rule 10 permit source 172.16.11.0 0.0.0.255",
    "rule 20 permit source 10.0.18.120 0.0.0.0",
    "rule 21 permit source 10.0.18.111 0.0.0.0",
    "rule 22 permit source 10.0.18.243 0.0.0.0",
    "rule 23 permit source 10.0.18.127 0.0.0.0",
    "rule 24 permit source 10.0.18.118 0.0.0.0",
    "rule 25 permit source 10.0.18.245 0.0.0.0",
    "rule 26 permit source 10.0.18.112 0.0.0.0",
    "rule 30 permit source 10.10.240.0 0.0.0.255",
    "rule 100 deny",
    "rule 10 description Rede Switch",
    "rule 20 description Rede Syslog",
    "rule 21 description Rede Librenms",
    "rule 22 description Rede Zabbix Homologacao",
    "rule 23 description Rede Automacao",
    "rule 24 description Rede Cacti",
    "rule 25 description Rede Flowbix",
    "rule 26 description Rede Flowbix oficial",
    "rule 30 description Rede Corporativo",
    "rule 100 description Bloqueia o resto",
    "quit",
    "undo acl number 2001",
    "yes",
    "mpls lsr-id {ip}",
    "mpls",
    "mpls te",
    "mpls te signaling-delay-trigger enable",
    "mpls te auto-frr",
    "label advertise non-null",
    "mpls rsvp-te",
    "mpls te cspf",
    "mpls te cspf preferred-igp ospf 1",
    "quit",
    "mpls ldp",
    "graceful-restart",
    "y",
    "mpls l2vpn",
    "quit",
    "configuration file auto-save interval 60",
    f"configuration file auto-save backup-to-server server 10.0.18.127 transport-type sftp user jtech password {backup_password} path /home/jtech/backup-metro",
    "snmp-agent",
    "snmp-agent acl 2000",
    "snmp-agent community read zabbix@toledo",
    "snmp-agent sys-info contact Alexandro Andrade Toledo",
    "snmp-agent sys-info location Core Tocantins - Brasil",
    "snmp-agent sys-info version all",
    "snmp-agent protocol source-interface LoopBack0",
    "user-interface con 0",
    "authentication-mode aaa",
    "history-command max-size 256",
    "user-interface vty 0 4",
    "authentication-mode aaa",
    "history-command max-size 256",
    "idle-timeout 0 0",
    "protocol inbound all",
    "ssh user jeanrmiranda",
    "ssh user jeanrmiranda",
    "ssh user jeanrmiranda authentication-type password",
    "ssh user jeanrmiranda service-type all",
    "quit",
    "save",
    "y",
]

# Roda para cada IP
for ip in lista_ips:
    enviar_comandos_ssh(ip, username, password, comandos)
  
