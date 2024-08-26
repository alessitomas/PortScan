import streamlit as st
import socket
import ipaddress


well_known_ports = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    3306: "MySQL", 5432: "PostgreSQL", 8080: "HTTP Alternate", 8501: "Streamlit"
}

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_range(ip, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        if scan_port(ip, port):
            service = well_known_ports.get(port, "Desconhecido")
            open_ports.append((port, service))
    return open_ports

st.title("Escaneador de Portas")


target = st.text_input("Digite o host ou rede a ser escaneado:")


col1, col2 = st.columns(2)
with col1:
    start_port = st.number_input("Porta inicial", min_value=1, max_value=65535, value=1)
with col2:
    end_port = st.number_input("Porta final", min_value=1, max_value=65535, value=1000)

if st.button("Escanear"):
    if target and start_port <= end_port:
        try:
            
            network = ipaddress.ip_network(target, strict=False)
            
            for ip in network.hosts():
                st.subheader(f"Resultados para {ip}:")
                open_ports = scan_range(str(ip), start_port, end_port)
                
                if open_ports:
                    for port, service in open_ports:
                        st.write(f"Porta {port}: {service}")
                else:
                    st.write("Nenhuma porta aberta encontrada.")
                
                st.write("---")
        
        except ValueError:
            st.error("Endereço IP ou rede inválido.")
    else:
        st.error("Por favor, preencha todos os campos corretamente.") 