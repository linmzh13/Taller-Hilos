import socket
import threading

HOST = '127.0.0.1'
PORT = 5050

usuarios = {}
registro_lock = threading.Lock()


def enviar_linea(conexion, envio_lock, mensaje):
    with envio_lock:
        conexion.sendall((mensaje + '\n').encode('utf-8'))


def difundir(mensaje, excluir=None):
    with registro_lock:
        destinos = list(usuarios.values())

    for conexion, envio_lock in destinos:
        if conexion is excluir:
            continue
        try:
            enviar_linea(conexion, envio_lock, mensaje)
        except OSError:
            pass


def atender_cliente(conexion, direccion):
    nombre = None
    archivo = None
    envio_lock = threading.Lock()

    try:
        archivo = conexion.makefile(
            'r',
            encoding='utf-8',
            newline='\n'
        )

        enviar_linea(conexion, envio_lock, 'Escribe tu nombre:')
        recibido = archivo.readline()

        if not recibido:
            return

        candidato = recibido.strip()

        if not candidato or candidato.startswith('/'):
            enviar_linea(conexion, envio_lock, 'Nombre no válido.')
            return

        nombre = candidato.casefold()

        with registro_lock:
            if nombre in usuarios:
                ocupado = True
            else:
                ocupado = False
                usuarios[nombre] = (conexion, envio_lock)

        if ocupado:
            enviar_linea(conexion, envio_lock, 'Nombre en uso.')
            nombre = None
            return

        enviar_linea(
            conexion,
            envio_lock,
            f'Bienvenido, {nombre}. Comandos: /usuarios, /salir'
        )

        difundir(
            f'[Sistema] {nombre} se ha conectado.',
            excluir=conexion
        )

        for linea in archivo:
            mensaje = linea.rstrip('\r\n')

            if mensaje == '/usuarios':
                with registro_lock:
                    nombres = sorted(usuarios.keys())
                enviar_linea(
                    conexion,
                    envio_lock,
                    'Usuarios conectados: ' + ', '.join(nombres)
                )

            elif mensaje == '/salir':
                enviar_linea(conexion, envio_lock, 'Hasta pronto.')
                break

            elif mensaje:
                difundir(
                    f'[{nombre}] {mensaje}',
                    excluir=conexion
                )

    except (OSError, UnicodeError) as exc:
        print(f'Conexión interrumpida ({direccion}): {exc}')

    finally:
        if archivo is not None:
            archivo.close()

        if nombre is not None:
            with registro_lock:
                actual = usuarios.get(nombre)
                if actual is not None and actual[0] is conexion:
                    del usuarios[nombre]

            difundir(
                f'[Sistema] {nombre} ha salido.',
                excluir=conexion
            )

        try:
            conexion.close()
        except OSError:
            pass


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()
        print(f'Servidor escuchando en {HOST}:{PORT}')

        try:
            while True:
                conexion, direccion = servidor.accept()
                threading.Thread(
                    target=atender_cliente,
                    args=(conexion, direccion),
                    daemon=True
                ).start()
        except KeyboardInterrupt:
            print('\nServidor detenido.')


if __name__ == '__main__':
    main()