import socket
import threading

HOST = '127.0.0.1'
PORT = 5050

def recibir(conexion, detener):
    try:
        with conexion.makefile('r', encoding='utf-8', newline='\n') as entrada:
            for linea in entrada:
                print('\n' + linea.rstrip('\r\n'), flush=True)
    except OSError:
        pass
    finally:
        detener.set()
        print('\nConexión finalizada.', flush=True)


def main():
    detener = threading.Event()
    try:
        with socket.create_connection((HOST, PORT)) as conexion:
            receptor = threading.Thread(
                target=recibir,
                args=(conexion, detener),
                daemon=True
            )
            receptor.start()

            nombre = input().strip()
            conexion.sendall((nombre + '\n').encode('utf-8'))

            while not detener.is_set():
                try:
                    mensaje = input('> ')
                except EOFError:
                    mensaje = '/salir'

                conexion.sendall((mensaje + '\n').encode('utf-8'))

                if mensaje == '/salir':
                    break

    except (ConnectionRefusedError, OSError) as exc:
        print('No se pudo conectar:', exc)


if __name__ == '__main__':
    main()