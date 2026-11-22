# Importa la clase base Exception para construir excepciones personalizadas del sistema.
class ErrorSistemaFJ(Exception):
    # Define el constructor de la excepción base con un mensaje y un código opcional.
    def __init__(self, mensaje: str, codigo: str = "ERR_GENERAL"):
        # Guarda el mensaje legible del error en un atributo de instancia.
        self.mensaje = mensaje
        # Guarda un código identificador para facilitar el rastreo en los logs.
        self.codigo = codigo
        # Invoca el constructor de Exception con un formato claro de código y mensaje.
        super().__init__(f"[{self.codigo}] {self.mensaje}")


# Define una excepción específica para datos inválidos o parámetros faltantes/erróneos.
class ErrorValidacionDato(ErrorSistemaFJ):
    # Inicializa la excepción con un código por defecto de validación.
    def __init__(self, mensaje: str, codigo: str = "ERR_VALIDACION"):
        # Pasa el mensaje y el código a la clase base ErrorSistemaFJ.
        super().__init__(mensaje, codigo)


# Define una excepción cuando se intenta usar un servicio no disponible.
class ServicioNoDisponibleError(ErrorSistemaFJ):
    # Inicializa la excepción con un código por defecto de disponibilidad.
    def __init__(self, mensaje: str, codigo: str = "ERR_SERVICIO_NO_DISP"):
        # Pasa el mensaje y el código a la clase base ErrorSistemaFJ.
        super().__init__(mensaje, codigo)


# Define una excepción para operaciones no permitidas o estados inválidos de reserva.
class OperacionReservaInvalidaError(ErrorSistemaFJ):
    # Inicializa la excepción con un código por defecto de operación de reserva.
    def __init__(self, mensaje: str, codigo: str = "ERR_RESERVA_INVALIDA"):
        # Pasa el mensaje y el código a la clase base ErrorSistemaFJ.
        super().__init__(mensaje, codigo)


# Define una excepción cuando ocurren cálculos inconsistentes (valores negativos, cero, etc.).
class CalculoInconsistenteError(ErrorSistemaFJ):
    # Inicializa la excepción con un código por defecto de cálculo.
    def __init__(self, mensaje: str, codigo: str = "ERR_CALCULO"):
        # Pasa el mensaje y el código a la clase base ErrorSistemaFJ.
        super().__init__(mensaje, codigo)
