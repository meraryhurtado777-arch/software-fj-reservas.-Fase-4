# Importa datetime para añadir fecha y hora exacta a cada evento o error registrado.
from datetime import datetime


# Define la clase GestorLogs para escribir eventos y errores en un archivo de texto.
class GestorLogs:
    # Inicializa el gestor con el nombre del archivo de log por defecto.
    def __init__(self, ruta_archivo: str = "software_fj.log"):
        # Guarda la ruta donde se almacenarán los registros del sistema.
        self.ruta_archivo = ruta_archivo

    # Escribe un registro en el archivo aplicando try/except/else/finally.
    def registrar(self, nivel: str, mensaje: str, detalle_extra: str = "") -> bool:
        # Obtiene la marca de tiempo actual con formato año-mes-día hora:minuto:segundo.
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Construye un segmento adicional si se proporciona información extra.
        extra = f" | {detalle_extra}" if detalle_extra else ""
        # Formatea la línea completa que se añadirá al archivo de log.
        linea = f"[{marca_tiempo}] [{nivel.upper()}]{extra} - {mensaje}\n"
        # Inicializa la variable de control de éxito en False.
        exito = False
        # Prepara la variable del archivo antes del bloque try.
        archivo = None
        # Intenta abrir y escribir en el archivo de log de forma segura.
        try:
            # Abre el archivo en modo anexar ('a') usando codificación UTF-8.
            archivo = open(self.ruta_archivo, mode="a", encoding="utf-8")
            # Escribe la línea formateada en el archivo.
            archivo.write(linea)
        # Captura errores del sistema operativo o de entrada/salida al manejar el archivo.
        except OSError as error_io:
            # Informa por consola sin detener el funcionamiento de la aplicación.
            print(f"[AVISO LOG] No fue posible escribir en '{self.ruta_archivo}': {error_io}")
        # Se ejecuta solo si el bloque try concluyó sin errores.
        else:
            # Marca el registro como guardado correctamente.
            exito = True
        # Se ejecuta siempre al final para liberar el recurso del archivo.
        finally:
            # Verifica que el archivo exista y siga abierto antes de cerrarlo.
            if archivo is not None and not archivo.closed:
                # Cierra el archivo de forma explícita.
                archivo.close()
        # Devuelve True si se escribió el log o False si ocurrió un fallo.
        return exito

    # Registra un evento informativo en el log.
    def registrar_info(self, mensaje: str, detalle_extra: str = "") -> bool:
        # Llama a registrar() con nivel INFO.
        return self.registrar("INFO", mensaje, detalle_extra)

    # Registra un error o excepción en el log.
    def registrar_error(self, mensaje: str, detalle_extra: str = "") -> bool:
        # Llama a registrar() con nivel ERROR.
        return self.registrar("ERROR", mensaje, detalle_extra)
            