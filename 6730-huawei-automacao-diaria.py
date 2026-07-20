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
    "reset counters interface",
    "system-view",
    "undo lldp enable",
    "clock timezone Brasilia minus 03:00:00",
    "bfd",
    "quit",
    "info-center loghost 10.0.18.120 source-ip {ip} local-time",
    "dns server 177.84.108.138",
    "dns server 177.84.108.139",
    "dns server 8.8.8.8",
    "lnp disable",
    "stp disable",
    "router id {ip}",
    "aaa",
    "undo local-aaa-user password policy administrator",
    "local-user jtech password irreversible-cipher %^%#ua-O0Z&Gi$d<UBMD&RkVRNqjGa-eq'u~<},XU6(3%^%#",
    "local-user jtech privilege level 15",
    "local-user jean password irreversible-cipher $1c$@]e&%l;NNH$q<hUA{O66@#;lZU02:lLC|l[!%P].NN0LtK/]J!)$",
    "local-user jtech service-type telnet terminal ssh ftp http",
    "local-user alexandro password irreversible-cipher $1c$y__qXZwM'U$D2kNIFqu2%Nx=<L0z@n:C&TLYLJqo7,2tnT]%XB;$",
    "local-user admin password irreversible-cipher $1c$M.*'->wm/D$VhI>N!`[%6-0d34kQ%G=M<@5K]F9R>#-Hh%{Yx`!$",
    "local-user alexandro ftp-directory flash:",
    "local-user alexandro service-type telnet terminal ssh ftp x25-pad http",
    "quit",
    "ssh server cipher aes256_ctr aes128_ctr",
    "ssh server hmac sha2_256",
    "ssh server key-exchange dh_group16_sha512 dh_group15_sha512 dh_group14_sha256 dh_group_exchange_sha256",
    "ssh client cipher aes256_ctr aes128_ctr",
    "ssh client hmac sha2_256",
    "ssh client key-exchange dh_group16_sha512 dh_group15_sha512 dh_group14_sha256 dh_group_exchange_sha256",
    "ssh server dh-exchange min-len 2048",
    "ssh server publickey rsa rsa_sha2_512 rsa_sha2_256",
    "stelnet server enable",
    "ssh server-source all-interface",
    "ntp-service server disable",
    "undo ntp-service access server",
    "ntp-service ipv6 server disable",
    "ntp-service source-interface LoopBack 0",
    "ntp-service unicast-server 172.16.11.5",
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
    "load-balance-profile MPLS",
    "l2 field smac dmac l2-protocol vlan",
    "ipv6 field sip dip vlan l4-sport l4-dport protocol",
    "ipv4 field sip dip vlan l4-sport l4-dport protocol",
    "mpls field top-label 2nd-label 3rd-label sip dip sport",
    "undo acl number 2001",
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
    "mpls ldp remote-peer 172.16.11.100",
    "remote-ip 172.16.11.100",
    "mpls l2vpn",
    "quit",
    "set save-configuration backup-to-server server 10.0.18.127 transport-type sftp user jtech password portugal@1985 path /home/jtech/backup-metro",
    "set save-configuration interval 31 delay 2",
    "snmp-agent acl 2000",
    "snmp-agent",
    "undo snmp-agent community plaintext enable",
    "snmp-agent community read zabbix@toledo",
    "snmp-agent sys-info contact Alexandro Andrade Toledo",
    "snmp-agent sys-info location Core Tocantins - Brasil",
    "snmp-agent sys-info version all",
    "undo snmp-agent protocol source-status all-interface",
    "snmp-agent protocol source-interface LoopBack0",
    "user-interface con 0",
    "authentication-mode aaa",
    "user privilege level 15",
    "history-command max-size 256",
    "idle-timeout 0 0",
    "user-interface vty 0 4",
    "authentication-mode aaa",
    "user privilege level 15",
    "history-command max-size 256",
    "idle-timeout 5",
    "protocol inbound all",
    "user-interface vty 16 20",
    "quit",
    "quit",
    "save",
]

# Roda para cada IP
for ip in lista_ips:
    enviar_comandos_ssh(ip, username, password, comandos)
