import pyshark

def contar_pacotes_saida(interface, tempo_captura):
    print(f"Capturando pacotes de saída na interface {interface} por {tempo_captura} segundos...")
    
    try:
        # Configura a captura apenas para pacotes de saída
        captura = pyshark.LiveCapture(interface=interface, display_filter='outbound')
        captura.sniff(timeout=tempo_captura)
        
        contador = 0
        for _ in captura:
            contador += 1
        
        print(f"Total de pacotes de saída: {contador}")
    
    except Exception as e:
        print(f"Erro na captura: {e}")

interface = input("Interface para monitorar:")
tempo = int(input("Tempo de execução (s):"))

# Exemplo de uso:
contar_pacotes_saida(interface, tempo)
