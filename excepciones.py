# Importa la clase base Exception de Python para crear excepciones propias del sistema.
class ErrorSistemaFJ(Exception):
    # Define el constructor de la excepción base con mensaje y código opcional.
    def __init__(self, mensaje: str, codigo: str = "ERR_GENERAL"):
        # Almacena el mensaje descriptivo del error en el atributo de instancia.
        self.mensaje = mensaje
        # Almacena el código identificador del error en el atributo de instancia.
        self.codigo = codigo
        # Llama al constructor de Exception formateando código y mensaje.
        super().__init__(f"[{self.codigo}] {self.mensaje}")


# Define una excepción específica para datos inválidos o parámetros incorrectos.
class ErrorValidacionDato(ErrorSistemaFJ):
    # Inicializa la excepción de validación con su código por defecto.
    def __init__(self, mensaje: str, codigo: str = "ERR_VALIDACION"):
        # Envía el mensaje y el código a la clase base ErrorSistemaFJ.
        super().__init__(mensaje, codigo)


# Define una excepción cuando se intenta usar un servicio no disponible.
class ServicioNoDisponibleError(ErrorSistemaFJ):
    # Inicializa la excepción de disponibilidad con su código por defecto.
    def __init__(self, mensaje: str, codigo: str = "ERR_SERVICIO_NO_DISP"):
        # Envía el mensaje y el código a la clase base ErrorSistemaFJ.
        super().__init__(mensaje, codigo)


# Define una excepción para operaciones no permitidas o estados inválidos de reserva.
class OperacionReservaInvalidaError(ErrorSistemaFJ):
    # Inicializa la excepción de reserva inválida con su código por defecto.
    def __init__(self, mensaje: str, codigo: str = "ERR_RESERVA_INVALIDA"):
        # Envía el mensaje y el código a la clase base ErrorSistemaFJ.
        super().__init__(mensaje, codigo)


# Define una excepción para cálculos inconsistentes durante la operación.
class CalculoInconsistenteError(ErrorSistemaFJ):
    # Inicializa la excepción de cálculo con su código por defecto.
    def __init__(self, mensaje: str, codigo: str = "ERR_CALCULO"):
        # Envía el mensaje y el código a la clase base ErrorSistemaFJ.
        super().__init__(mensaje, codigo)
