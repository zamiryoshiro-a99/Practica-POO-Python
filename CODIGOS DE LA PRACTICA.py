#PREGUNTA 2 Datos que deben quedar protegidos y sus reglas de validación
#Código  — Validación de los datos de un curso
class Curso:
    def __init__(self, codigo, nombre, creditos, teoricas, practicas):
        if not codigo.strip() or not nombre.strip():
            raise ValueError("Codigo y nombre son obligatorios.")
        self._codigo = codigo.strip()             # Solo lectura
        self.nombre = nombre
        self.creditos = creditos
        self.teoricas = teoricas
        self.practicas = practicas

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip() or len(valor) > 100:
            raise ValueError("Nombre obligatorio, maximo 100 caracteres.")
        self._nombre = valor.strip()

    @property
    def creditos(self):
        return self._creditos

    @creditos.setter
    def creditos(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not 0 < valor <= 10:
            raise ValueError("Los creditos deben ser mayores que 0 y hasta 10.")
        self._creditos = float(valor)  # Se guarda como float

    def validar_horas(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or not 0 <= valor <= 255:
            raise ValueError("Las horas deben ser enteros entre 0 y 255.")
        return valor

    @property
    def teoricas(self):
        return self._teoricas

    @teoricas.setter
    def teoricas(self, valor):
        self._teoricas = self.validar_horas(valor)

    @property
    def practicas(self):
        return self._practicas

    @practicas.setter
    def practicas(self, valor):
        self._practicas = self.validar_horas(valor)

    @property
    def horas_totales(self):
        return self._teoricas + self._practicas  # Se calcula, no se almacena


class Seccion:
    def __init__(self, codigo, vacantes):
        if not codigo.strip() or not isinstance(vacantes, int) or vacantes <= 0:
            raise ValueError("Codigo obligatorio y vacantes enteras positivas.")
        self._codigo = codigo.strip()
        self._vacantes = vacantes
        self._matriculados = 0

    @property
    def matriculados(self):
        return self._matriculados  # No tiene setter: no se cambia directamente

    @property
    def disponibles(self):
        return self._vacantes - self._matriculados  # Dato calculado

    def matricular(self):
        if self.disponibles == 0:
            raise ValueError("No quedan vacantes.")
        self._matriculados += 1

    def retirar(self):
        if self._matriculados == 0:
            raise ValueError("No hay matriculados para retirar.")
        self._matriculados -= 1


class PeriodoAcademico:
    ESTADOS = {1: "Planificado", 2: "En curso", 3: "Matricula cerrada", 4: "Finalizado"}

    def __init__(self, nombre, estado=1):
        if not nombre.strip():
            raise ValueError("El nombre del periodo es obligatorio.")
        self._nombre = nombre.strip()
        self.estado = estado

    @property
    def estado(self):
        return self.ESTADOS[self._estado]  # Se guarda int y se entrega str

    @estado.setter
    def estado(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor not in self.ESTADOS:
            raise ValueError("Estado valido: 1, 2, 3 o 4.")
        self._estado = valor

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado


if __name__ == "__main__":
    print("ACTIVIDAD 2: ENCAPSULAMIENTO - OTI UNSCH")
    print("Curso: IS-283 - Programacion Orientada a Objetos")
    print("Docente encargado: PELAYO BAUTISTA QUISPE\n")

    curso = Curso("IS-283", "Programacion Orientada a Objetos", 4, 3, 2)
    seccion = Seccion("SEC01", 36)  # 36 vacantes; una matricula deja 35 disponibles
    periodo = PeriodoAcademico("2026-I", 2)
    seccion.matricular()
    periodo.cambiar_estado(3)

    print("Curso:", curso.codigo, curso.nombre)
    print("Creditos:", curso.creditos, "| tipo:", type(curso.creditos).__name__)
    print("Horas totales calculadas:", curso.horas_totales)
    print("Matriculados:", seccion.matriculados, "| Vacantes disponibles:", seccion.disponibles)
    print("Estado del periodo:", periodo.estado, "| tipo entregado: str")

    print("=====Resumen de encapsulamiento======:")
    print("1. Protegidos: nombre, creditos, horas, vacantes y estado; validan contenido, rango y tipo.")
    print("2. Calculados: horas_totales y disponibles; evita guardar valores desactualizados.")
    print("3. Sin cambio directo: codigo y matriculados; matricular() y retirar() controlan la matricula, cambiar_estado() cambia el estado.")
    print("4. Tipos distintos: creditos se normaliza a float; estado se guarda como int y se entrega como str descriptivo.")



#######################################################################################################################################################
#PREGUNTA 3-ABSTRACCION: Proponga una mejor forma de representar el estado del periodo académico, de modo que un valor como 7 sea rechazado.
########################################################################################################################################################
from abc import ABC, abstractmethod


def validar_texto(valor, campo, maximo=None):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(campo + " no puede estar vacio.")
    valor = valor.strip()
    if maximo is not None and len(valor) > maximo:
        raise ValueError(campo + " supera el maximo de caracteres.")
    return valor


def validar_numero(valor, campo, minimo=0, maximo=None):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(campo + " debe ser numerico.")
    if valor < minimo:
        raise ValueError(campo + " esta por debajo del minimo.")
    if maximo is not None and valor > maximo:
        raise ValueError(campo + " supera el maximo permitido.")
    if round(valor, 2) != valor:
        raise ValueError(campo + " admite maximo 2 decimales.")
    return valor


class EntidadNombrada(ABC):
    """Clase abstracta para registros con nombre y resumen."""

    def __init__(self, nombre, maximo=None):
        self._maximo_nombre = maximo
        self._nombre = validar_texto(nombre, "Nombre", maximo)

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "Nombre", self._maximo_nombre)

    @abstractmethod
    def resumen(self):
        """Cada clase concreta debe implementar su resumen."""


class Curso(EntidadNombrada):
    """Curso con código, créditos y horas de clase."""
    siguiente_id = 1

    def __init__(self, codigo, nombre, creditos, teoricas=0, practicas=0,
                 seminario=0, virtuales=0):
        self._id = Curso.siguiente_id
        Curso.siguiente_id += 1
        self._codigo = validar_texto(codigo, "Codigo del curso")
        self.creditos = creditos
        super().__init__(nombre, 200)
        self.horas_teoricas = teoricas
        self.horas_practicas = practicas
        self.horas_seminario = seminario
        self.horas_virtuales = virtuales

    @property
    def id(self):
        return self._id

    @property
    def codigo(self):
        return self._codigo

    @property
    def creditos(self):
        return self._creditos

    @creditos.setter
    def creditos(self, valor):
        self._creditos = validar_numero(valor, "Creditos", 0.01)

    def validar_horas(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or not 0 <= valor <= 255:
            raise ValueError("Las horas deben ser enteros entre 0 y 255.")
        return valor

    @property
    def horas_teoricas(self):
        return self._horas_teoricas

    @horas_teoricas.setter
    def horas_teoricas(self, valor):
        self._horas_teoricas = self.validar_horas(valor)

    @property
    def horas_practicas(self):
        return self._horas_practicas

    @horas_practicas.setter
    def horas_practicas(self, valor):
        self._horas_practicas = self.validar_horas(valor)

    @property
    def horas_seminario(self):
        return self._horas_seminario

    @horas_seminario.setter
    def horas_seminario(self, valor):
        self._horas_seminario = self.validar_horas(valor)

    @property
    def horas_virtuales(self):
        return self._horas_virtuales

    @horas_virtuales.setter
    def horas_virtuales(self, valor):
        self._horas_virtuales = self.validar_horas(valor)

    @property
    def horas_totales(self):
        return (self.horas_teoricas + self.horas_practicas
                + self.horas_seminario + self.horas_virtuales)

    def resumen(self):
        return "Curso " + self.codigo + ": " + self.nombre


class Seccion:
    """Sección de un curso en un periodo académico."""

    def __init__(self, codigo, codigo_curso, codigo_periodo, vacantes):
        self._codigo = validar_texto(codigo, "Codigo de seccion")
        self._codigo_curso = validar_texto(codigo_curso, "Codigo de curso")
        self._codigo_periodo = validar_texto(codigo_periodo, "Codigo de periodo")
        self._matriculados = 0
        self.vacantes = vacantes

    @property
    def codigo(self):
        return self._codigo

    @property
    def matriculados(self):
        return self._matriculados

    @property
    def vacantes(self):
        return self._vacantes

    @vacantes.setter
    def vacantes(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise ValueError("Vacantes debe ser un entero.")
        if valor <= 0 or valor < self._matriculados:
            raise ValueError("Vacantes debe ser positivo y no menor que matriculados.")
        self._vacantes = valor

    @property
    def vacantes_disponibles(self):
        return self._vacantes - self._matriculados

    def matricular(self):
        if self._matriculados >= self._vacantes:
            raise ValueError("No quedan vacantes.")
        self._matriculados += 1

    def retirar(self):
        if self._matriculados == 0:
            raise ValueError("No hay estudiantes para retirar.")
        self._matriculados -= 1


class PlanEstudio(EntidadNombrada):
    """Plan con créditos obligatorios, electivos y extracurriculares."""

    def __init__(self, nombre, obligatorios, electivos, extracurriculares, vigente=True):
        super().__init__(nombre, 36)
        self.creditos_obligatorios = obligatorios
        self.creditos_electivos = electivos
        self.creditos_extracurriculares = extracurriculares
        self.vigente = vigente

    @property
    def creditos_obligatorios(self):
        return self._obligatorios

    @creditos_obligatorios.setter
    def creditos_obligatorios(self, valor):
        self._obligatorios = validar_numero(valor, "Creditos obligatorios")

    @property
    def creditos_electivos(self):
        return self._electivos

    @creditos_electivos.setter
    def creditos_electivos(self, valor):
        self._electivos = validar_numero(valor, "Creditos electivos")

    @property
    def creditos_extracurriculares(self):
        return self._extracurriculares

    @creditos_extracurriculares.setter
    def creditos_extracurriculares(self, valor):
        self._extracurriculares = validar_numero(valor, "Creditos extracurriculares")

    @property
    def total_creditos(self):
        return (self.creditos_obligatorios + self.creditos_electivos
                + self.creditos_extracurriculares)

    @property
    def vigente(self):
        return self._vigente

    @vigente.setter
    def vigente(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("Vigente debe ser True o False.")
        self._vigente = valor

    def resumen(self):
        return "Plan de estudio: " + self.nombre


class EscuelaProfesional(EntidadNombrada):
    """Escuela y sus datos principales."""

    def __init__(self, codigo, nombre, informacion, perfil, director, secretario):
        self._codigo = validar_texto(codigo, "Codigo de escuela")
        self._informacion = validar_texto(informacion, "Informacion general")
        self._perfil = validar_texto(perfil, "Perfil del egresado")
        self._director = validar_texto(director, "Codigo del director")
        self._secretario = validar_texto(secretario, "Codigo del secretario academico")
        super().__init__(nombre)

    def resumen(self):
        return "Escuela profesional: " + self.nombre


class PeriodoAcademico(EntidadNombrada):
    """Periodo con fechas, nota mínima y estado controlado."""

    PLANIFICADO = 1
    EN_CURSO = 2
    MATRICULA_CERRADA = 3
    FINALIZADO = 4

    def __init__(self, nombre, numero, año, inicio, fin, inicio_matricula,
                 fin_matricula, es_verano, nota_minima, estado=PLANIFICADO):
        self._numero = numero
        self._año = año
        self.actualizar_fechas(inicio, fin)
        self.actualizar_fechas_matricula(inicio_matricula, fin_matricula)
        self.es_verano = es_verano
        self.nota_minima = nota_minima
        self.estado = estado
        super().__init__(nombre, 45)

    def validar_intervalo(self, inicio, fin, campo):
        validar_texto(inicio, "Inicio de " + campo)
        validar_texto(fin, "Fin de " + campo)
        if (len(inicio) != 10 or len(fin) != 10 or fin < inicio
                or inicio[4:5] != "-" or inicio[7:8] != "-"
                or fin[4:5] != "-" or fin[7:8] != "-"):
            raise ValueError("Fechas de " + campo + " invalidas. Use AAAA-MM-DD.")

    def actualizar_fechas(self, inicio, fin):
        self.validar_intervalo(inicio, fin, "periodo")
        self._inicio, self._fin = inicio, fin

    def actualizar_fechas_matricula(self, inicio, fin):
        self.validar_intervalo(inicio, fin, "matricula")
        self._inicio_matricula, self._fin_matricula = inicio, fin

    @property
    def es_verano(self):
        return self._es_verano

    @es_verano.setter
    def es_verano(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("Es verano debe ser True o False.")
        self._es_verano = valor

    @property
    def nota_minima(self):
        return self._nota_minima

    @nota_minima.setter
    def nota_minima(self, valor):
        self._nota_minima = validar_numero(valor, "Nota minima", 0, 20)

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        estados_validos = (self.PLANIFICADO, self.EN_CURSO,
                           self.MATRICULA_CERRADA, self.FINALIZADO)
        if not isinstance(valor, int) or isinstance(valor, bool) or valor not in estados_validos:
            raise ValueError("Estado no permitido: use 1, 2, 3 o 4.")
        self._estado = valor

    def resumen(self):
        return "Periodo academico: " + self.nombre


class Persona(ABC):
    """Clase abstracta común para estudiantes y docentes."""

    def __init__(self, dni, nombres, apellidos):
        self._dni = validar_texto(dni, "DNI")
        self._nombres = validar_texto(nombres, "Nombres")
        self._apellidos = validar_texto(apellidos, "Apellidos")

    @property
    def nombre_completo(self):
        return self._nombres + " " + self._apellidos

    @abstractmethod
    def obtener_codigo(self):
        """Devuelve el código de la persona."""

    @abstractmethod
    def obtener_rol(self):
        """Devuelve el rol de la persona."""


class Estudiante(Persona):
    """Persona con código de estudiante y escuela."""

    def __init__(self, dni, nombres, apellidos, codigo, codigo_escuela):
        super().__init__(dni, nombres, apellidos)
        self._codigo = validar_texto(codigo, "Codigo de estudiante")
        self._codigo_escuela = validar_texto(codigo_escuela, "Codigo de escuela")

    def obtener_codigo(self):
        return self._codigo

    def obtener_rol(self):
        return "Estudiante"


class Docente(Persona):
    """Persona con código de docente."""

    def __init__(self, dni, nombres, apellidos, codigo):
        super().__init__(dni, nombres, apellidos)
        self._codigo = validar_texto(codigo, "Codigo de docente")

    def obtener_codigo(self):
        return self._codigo

    def obtener_rol(self):
        return "Docente"


def probar_asignacion(nombre, objeto, atributo, valor, debe_fallar=False):
    try:
        setattr(objeto, atributo, valor)
        if debe_fallar:
            print("[ERROR]", nombre + ": se acepto un valor que debia rechazarse.")
        else:
            print("[CORRECTO]", nombre)
    except (ValueError, TypeError) as error:
        if debe_fallar:
            print("[CORRECTO]", nombre + ". Validacion aplicada:", error)
        else:
            print("[ERROR]", nombre + ":", error)


def probar_clase_abstracta(nombre, clase, argumentos):
    try:
        clase(*argumentos)
        print("[ERROR]", nombre + ": la clase abstracta permitio crear un objeto.")
    except TypeError:
        print("[CORRECTO]", nombre + ": no permite crear objetos directamente.")


if __name__ == "__main__":
    print("ACTIVIDAD 3: ABSTRACCION - OTI UNSCH")
    print("Curso: IS-283 - Programacion Orientada a Objetos")
    print("Docente encargado: PELAYO BAUTISTA QUISPE")
    print("\n1. Datos del curso, plan, escuela y periodo:")

    curso = Curso("IS-283", "Programacion Orientada a Objetos", 4, 3, 2, 1, 1)
    plan = PlanEstudio("Computacion e Informatica", 120, 20, 10, True)
    escuela = EscuelaProfesional(
        "EP01", "Ingenieria de Sistemas",
        "Formacion profesional en tecnologia",
        "Diseñar y desarrollar soluciones informaticas",
        "DOC-014", "DOC-015"
    )
    periodo = PeriodoAcademico(
        "2026-I", 1, 2026, "2026-03-01", "2026-07-31",
        "2026-03-01", "2026-03-10", False, 11
    )
    registros = [curso, plan, escuela, periodo]
    for registro in registros:
        print("-", registro.resumen())

    print("\n2. Datos de estudiantes y docentes:")
    print("Horas totales del curso:", curso.horas_totales)
    print("Total de creditos del plan:", plan.total_creditos)
    print("Estado actual del periodo:", periodo.estado)

########################################################################################################################################################
##ACTIVIDAD 4 - PREGUNTA 3:"Demuestre el polimorfismo: recorra una lista mixta de registros pidiendo a cada uno su resumen, sin usar isinstance#########
########################################################################################################################################################
from abc import ABC, abstractmethod


def validar_texto(valor, campo, maximo=None):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(campo + " no puede estar vacio.")
    valor = valor.strip()
    if maximo is not None and len(valor) > maximo:
        raise ValueError(campo + " supera el maximo de caracteres.")
    return valor


def validar_numero(valor, campo, minimo=0, maximo=None):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(campo + " debe ser numerico.")
    if valor < minimo:
        raise ValueError(campo + " esta por debajo del minimo.")
    if maximo is not None and valor > maximo:
        raise ValueError(campo + " supera el maximo permitido.")
    if round(valor, 2) != valor:
        raise ValueError(campo + " admite maximo 2 decimales.")
    return valor


class EntidadNombrada(ABC):
    def __init__(self, nombre, maximo=None):
        self._maximo_nombre = maximo
        self._nombre = validar_texto(nombre, "Nombre", maximo)

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "Nombre", self._maximo_nombre)

    @abstractmethod
    def resumen(self):
        pass


class Curso(EntidadNombrada):
    siguiente_id = 1

    def __init__(self, codigo, nombre, creditos, teoricas=0, practicas=0,
                 seminario=0, virtuales=0):
        self._id = Curso.siguiente_id
        Curso.siguiente_id += 1
        self._codigo = validar_texto(codigo, "Codigo del curso")
        self.creditos = creditos
        super().__init__(nombre, 200)
        self.horas_teoricas = teoricas
        self.horas_practicas = practicas
        self.horas_seminario = seminario
        self.horas_virtuales = virtuales

    @property
    def id(self):
        return self._id

    @property
    def codigo(self):
        return self._codigo

    @property
    def creditos(self):
        return self._creditos

    @creditos.setter
    def creditos(self, valor):
        self._creditos = validar_numero(valor, "Creditos", 0.01)

    def validar_horas(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or not 0 <= valor <= 255:
            raise ValueError("Las horas deben ser enteros entre 0 y 255.")
        return valor

    @property
    def horas_teoricas(self):
        return self._horas_teoricas

    @horas_teoricas.setter
    def horas_teoricas(self, valor):
        self._horas_teoricas = self.validar_horas(valor)

    @property
    def horas_practicas(self):
        return self._horas_practicas

    @horas_practicas.setter
    def horas_practicas(self, valor):
        self._horas_practicas = self.validar_horas(valor)

    @property
    def horas_seminario(self):
        return self._horas_seminario

    @horas_seminario.setter
    def horas_seminario(self, valor):
        self._horas_seminario = self.validar_horas(valor)

    @property
    def horas_virtuales(self):
        return self._horas_virtuales

    @horas_virtuales.setter
    def horas_virtuales(self, valor):
        self._horas_virtuales = self.validar_horas(valor)

    @property
    def horas_totales(self):
        return (self.horas_teoricas + self.horas_practicas
                + self.horas_seminario + self.horas_virtuales)

    def resumen(self):
        return "Curso " + self.codigo + ": " + self.nombre


class Seccion:
    def __init__(self, codigo, codigo_curso, codigo_periodo, vacantes):
        self._codigo = validar_texto(codigo, "Codigo de seccion")
        self._codigo_curso = validar_texto(codigo_curso, "Codigo de curso")
        self._codigo_periodo = validar_texto(codigo_periodo, "Codigo de periodo")
        self._matriculados = 0
        self.vacantes = vacantes

    @property
    def codigo(self):
        return self._codigo

    @property
    def matriculados(self):
        return self._matriculados

    @property
    def vacantes(self):
        return self._vacantes

    @vacantes.setter
    def vacantes(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise ValueError("Vacantes debe ser un entero.")
        if valor <= 0 or valor < self._matriculados:
            raise ValueError("Vacantes debe ser positivo y no menor que matriculados.")
        self._vacantes = valor

    @property
    def vacantes_disponibles(self):
        return self._vacantes - self._matriculados

    def matricular(self):
        if self._matriculados >= self._vacantes:
            raise ValueError("No quedan vacantes.")
        self._matriculados += 1

    def retirar(self):
        if self._matriculados == 0:
            raise ValueError("No hay estudiantes para retirar.")
        self._matriculados -= 1


class PlanEstudio(EntidadNombrada):
    def __init__(self, nombre, obligatorios, electivos, extracurriculares, vigente=True):
        super().__init__(nombre, 36)
        self.creditos_obligatorios = obligatorios
        self.creditos_electivos = electivos
        self.creditos_extracurriculares = extracurriculares
        self.vigente = vigente

    @property
    def creditos_obligatorios(self):
        return self._obligatorios

    @creditos_obligatorios.setter
    def creditos_obligatorios(self, valor):
        self._obligatorios = validar_numero(valor, "Creditos obligatorios")

    @property
    def creditos_electivos(self):
        return self._electivos

    @creditos_electivos.setter
    def creditos_electivos(self, valor):
        self._electivos = validar_numero(valor, "Creditos electivos")

    @property
    def creditos_extracurriculares(self):
        return self._extracurriculares

    @creditos_extracurriculares.setter
    def creditos_extracurriculares(self, valor):
        self._extracurriculares = validar_numero(valor, "Creditos extracurriculares")

    @property
    def total_creditos(self):
        return (self.creditos_obligatorios + self.creditos_electivos
                + self.creditos_extracurriculares)

    @property
    def vigente(self):
        return self._vigente

    @vigente.setter
    def vigente(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("Vigente debe ser True o False.")
        self._vigente = valor

    def resumen(self):
        return "Plan de estudio: " + self.nombre


class EscuelaProfesional(EntidadNombrada):
    def __init__(self, codigo, nombre, informacion, perfil, director, secretario):
        self._codigo = validar_texto(codigo, "Codigo de escuela")
        self._informacion = validar_texto(informacion, "Informacion general")
        self._perfil = validar_texto(perfil, "Perfil del egresado")
        self._director = validar_texto(director, "Codigo del director")
        self._secretario = validar_texto(secretario, "Codigo del secretario academico")
        super().__init__(nombre)

    def resumen(self):
        return "Escuela profesional: " + self.nombre


class PeriodoAcademico(EntidadNombrada):
    PLANIFICADO = 1
    EN_CURSO = 2
    MATRICULA_CERRADA = 3
    FINALIZADO = 4

    def __init__(self, nombre, numero, año, inicio, fin, inicio_matricula,
                 fin_matricula, es_verano, nota_minima, estado=PLANIFICADO):
        self._numero = numero
        self._año = año
        self.actualizar_fechas(inicio, fin)
        self.actualizar_fechas_matricula(inicio_matricula, fin_matricula)
        self.es_verano = es_verano
        self.nota_minima = nota_minima
        self.estado = estado
        super().__init__(nombre, 45)

    def validar_intervalo(self, inicio, fin, campo):
        inicio = validar_texto(inicio, "Inicio de " + campo)
        fin = validar_texto(fin, "Fin de " + campo)
        if (len(inicio) != 10 or len(fin) != 10 or fin < inicio
                or inicio[4] != "-" or inicio[7] != "-"
                or fin[4] != "-" or fin[7] != "-"):
            raise ValueError("Fechas de " + campo + " invalidas. Use AAAA-MM-DD.")
        if not (inicio[:4].isdigit() and inicio[5:7].isdigit()
                and inicio[8:10].isdigit() and fin[:4].isdigit()
                and fin[5:7].isdigit() and fin[8:10].isdigit()):
            raise ValueError("Fecha invalida. Use AAAA-MM-DD.")

    def actualizar_fechas(self, inicio, fin):
        self.validar_intervalo(inicio, fin, "periodo")
        self._inicio, self._fin = inicio, fin

    def actualizar_fechas_matricula(self, inicio, fin):
        self.validar_intervalo(inicio, fin, "matricula")
        self._inicio_matricula, self._fin_matricula = inicio, fin

    @property
    def es_verano(self):
        return self._es_verano

    @es_verano.setter
    def es_verano(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("Es verano debe ser True o False.")
        self._es_verano = valor

    @property
    def nota_minima(self):
        return self._nota_minima

    @nota_minima.setter
    def nota_minima(self, valor):
        self._nota_minima = validar_numero(valor, "Nota minima", 0, 20)

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        estados = (self.PLANIFICADO, self.EN_CURSO,
                   self.MATRICULA_CERRADA, self.FINALIZADO)
        if not isinstance(valor, int) or isinstance(valor, bool) or valor not in estados:
            raise ValueError("Estado no permitido: use 1, 2, 3 o 4.")
        self._estado = valor

    def resumen(self):
        return "Periodo academico: " + self.nombre


class Persona(ABC):
    def __init__(self, dni, nombres, apellidos):
        self._dni = validar_texto(dni, "DNI")
        self._nombres = validar_texto(nombres, "Nombres")
        self._apellidos = validar_texto(apellidos, "Apellidos")

    @property
    def nombre_completo(self):
        return self._nombres + " " + self._apellidos

    @abstractmethod
    def obtener_codigo(self):
        pass

    @abstractmethod
    def obtener_rol(self):
        pass


class Estudiante(Persona):
    def __init__(self, dni, nombres, apellidos, codigo, codigo_escuela):
        super().__init__(dni, nombres, apellidos)
        self._codigo = validar_texto(codigo, "Codigo de estudiante")
        self._codigo_escuela = validar_texto(codigo_escuela, "Codigo de escuela")

    def obtener_codigo(self):
        return self._codigo

    def obtener_rol(self):
        return "Estudiante"


class Docente(Persona):
    def __init__(self, dni, nombres, apellidos, codigo):
        super().__init__(dni, nombres, apellidos)
        self._codigo = validar_texto(codigo, "Codigo de docente")

    def obtener_codigo(self):
        return self._codigo

    def obtener_rol(self):
        return "Docente"


if __name__ == "__main__":
    curso = Curso("IS-283", "Programacion Orientada a Objetos", 4, 3, 2, 1, 1)
    plan = PlanEstudio("Computacion e Informatica", 120, 20, 10)
    escuela = EscuelaProfesional(
        "EP01", "Ingenieria de Sistemas",
        "Formacion profesional en tecnologia",
        "Desarrollar soluciones informaticas", "DOC-014", "DOC-015"
    )
    periodo = PeriodoAcademico(
        "2026-I", 1, 2026, "2026-03-01", "2026-07-31",
        "2026-03-01", "2026-03-10", False, 11
    )
    estudiante = Estudiante("12345678", "Ana", "Perez", "EST-01", "EP01")
    docente = Docente("87654321", "Luis", "Rojas", "DOC-01")

    print("ACTIVIDAD 4: HERENCIA")

    print("\n1. Clases del sistema academico:")
    print("Curso es una EntidadNombrada.")
    print("PlanEstudio es una EntidadNombrada.")
    print("EscuelaProfesional es una EntidadNombrada.")
    print("PeriodoAcademico es una EntidadNombrada.")
    print("Estudiante es una Persona.")
    print("Docente es una Persona.")

    print("\n2. Datos heredados y propios:")
    print("Curso:", curso.nombre, "-", curso.codigo, "-", curso.creditos, "creditos")
    print("Plan:", plan.nombre, "-", plan.total_creditos, "creditos")
    print("Escuela:", escuela.nombre)
    print("Periodo:", periodo.nombre, "-", periodo.estado)
    print("Estudiante:", estudiante.nombre_completo, "-", estudiante.obtener_codigo())
    print("Docente:", docente.nombre_completo, "-", docente.obtener_codigo())

    print("\n3. Resumen de registros:")
    registros = [curso, plan, escuela, periodo]
    for registro in registros:
        print(registro.resumen())


#################################################################################################################################################
### ACTIVIDAD 5:Implemente en Python todas las clases identificadas
##################################################################################################################################################
# ACTIVIDADES 2, 3 y 4: validaciones, fechas y clases abstractas.
# ABC permite aplicar abstraccion sin necesitar librerias adicionales.
# ACTIVIDADES 2, 3 y 4: validaciones, fechas y clases abstractas.
from abc import ABC, abstractmethod

def validar_texto(valor, nombre, maximo=None):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(nombre + " no puede estar vacio.")
    valor = valor.strip()
    if maximo is not None and len(valor) > maximo:
        raise ValueError(nombre + " supera el maximo de caracteres.")
    return valor

def validar_numero(valor, nombre, minimo=None, maximo=None, decimales=2):
    if isinstance(valor, bool):
        raise ValueError(nombre + " debe ser numerico.")
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        raise ValueError(nombre + " debe ser numerico.")
    if numero != numero or numero in (float("inf"), float("-inf")):
        raise ValueError(nombre + " debe ser un numero valido.")
    if minimo is not None and numero < minimo:
        raise ValueError(nombre + " esta por debajo del minimo.")
    if maximo is not None and numero > maximo:
        raise ValueError(nombre + " supera el maximo permitido.")
    if round(numero, decimales) != numero:
        raise ValueError(nombre + " admite como maximo dos decimales.")
    return numero

def validar_entero(valor, nombre, minimo=None, maximo=None):
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError(nombre + " debe ser un numero entero.")
    if minimo is not None and valor < minimo:
        raise ValueError(nombre + " esta por debajo del minimo.")
    if maximo is not None and valor > maximo:
        raise ValueError(nombre + " supera el maximo permitido.")
    return valor

def validar_fecha(valor, nombre):
    if not isinstance(valor, str):
        raise ValueError(nombre + " debe tener el formato AAAA-MM-DD.")
    partes = valor.split("-")
    if len(partes) != 3 or len(partes[0]) != 4 or len(partes[1]) != 2 or len(partes[2]) != 2:
        raise ValueError(nombre + " debe tener el formato AAAA-MM-DD.")
    try:
        anio, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
    except ValueError:
        raise ValueError(nombre + " debe tener el formato AAAA-MM-DD.")
    if anio < 1 or mes < 1 or mes > 12:
        raise ValueError(nombre + " no es una fecha valida.")
    dias_mes = [31, 29 if anio % 400 == 0 or (anio % 4 == 0 and anio % 100 != 0) else 28,
                31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if dia < 1 or dia > dias_mes[mes - 1]:
        raise ValueError(nombre + " no es una fecha valida.")
    return valor

# ACTIVIDAD 3 - ABSTRACCION:

class EntidadNombrada(ABC):
    def __init__(self, nombre):
        self.nombre = validar_texto(nombre, "Nombre")
    @abstractmethod
    def resumen(self):
        pass
# ACTIVIDAD 2: Curso valida sus datos, calcula horas_totales y protege su ID.

class Curso(EntidadNombrada):
    siguiente_id = 1
    def __init__(self, codigo, nombre, creditos, horas_teoria, horas_practica):
        super().__init__(nombre)
        self.__id = Curso.siguiente_id
        Curso.siguiente_id += 1
        self.codigo = codigo
        self.creditos = creditos
        self.horas_teoria = horas_teoria
        self.horas_practica = horas_practica
    @property
    def id(self):
        return self.__id
    @property
    def codigo(self):
        return self.__codigo
    @codigo.setter
    def codigo(self, valor):
        self.__codigo = validar_texto(valor, "Codigo del curso")
    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, valor):
        self.__nombre = validar_texto(valor, "Nombre del curso", 200)
    @property
    def creditos(self):
        return self.__creditos
    @creditos.setter
    def creditos(self, valor):
        self.__creditos = validar_numero(valor, "Creditos", minimo=0.01)
    @property
    def horas_teoria(self):
        return self.__horas_teoria
    @horas_teoria.setter
    def horas_teoria(self, valor):
        self.__horas_teoria = validar_entero(valor, "Horas de teoria", 0, 255)
    @property
    def horas_practica(self):
        return self.__horas_practica
    @horas_practica.setter
    def horas_practica(self, valor):
        self.__horas_practica = validar_entero(valor, "Horas de practica", 0, 255)
    @property
    def horas_totales(self):
        return self.horas_teoria + self.horas_practica
    def resumen(self):
        return "Curso " + self.codigo + ": " + self.nombre
    
# ACTIVIDAD 2: Seccion, matricula y vacantes.
class Seccion:
    def __init__(self, codigo, codigo_curso, codigo_periodo, vacantes):
        self.codigo = validar_texto(codigo, "Codigo de seccion")
        self.codigo_curso = validar_texto(codigo_curso, "Codigo de curso")
        self.codigo_periodo = validar_texto(codigo_periodo, "Codigo de periodo")
        self.__matriculados = 0
        self.vacantes = vacantes
    @property
    def vacantes(self):
        return self.__vacantes
    @vacantes.setter
    def vacantes(self, valor):
        valor = validar_entero(valor, "Vacantes", 1)
        if valor < self.__matriculados:
            raise ValueError("Las vacantes no pueden ser menores que los matriculados.")
        self.__vacantes = valor
    @property
    def matriculados(self):
        return self.__matriculados
    @property
    def vacantes_disponibles(self):
        return self.vacantes - self.matriculados
    def matricular(self):
        if self.vacantes_disponibles == 0:
            raise ValueError("La seccion ya no tiene vacantes.")
        self.__matriculados += 1
    def retirar(self):
        if self.__matriculados == 0:
            raise ValueError("No hay estudiantes para retirar.")
        self.__matriculados -= 1

# ACTIVIDAD 2: valida el plan y calcula creditos_totales.
class PlanEstudio(EntidadNombrada):
    def __init__(self, nombre, año_aprobacion, creditos_obligatorios,
                 creditos_electivos, creditos_extracurriculares, vigente=True):
        super().__init__(nombre)
        self.año_aprobacion = validar_entero(año_aprobacion, "Año de aprobación", 1)
        self.creditos_obligatorios = creditos_obligatorios
        self.creditos_electivos = creditos_electivos
        self.creditos_extracurriculares = creditos_extracurriculares
        self.vigente = vigente
    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, valor):
        self.__nombre = validar_texto(valor, "Nombre del plan", 36)
    @property
    def creditos_obligatorios(self):
        return self.__obligatorios
    @creditos_obligatorios.setter
    def creditos_obligatorios(self, valor):
        self.__obligatorios = validar_numero(valor, "Creditos obligatorios", minimo=0)
    @property
    def creditos_electivos(self):
        return self.__electivos
    @creditos_electivos.setter
    def creditos_electivos(self, valor):
        self.__electivos = validar_numero(valor, "Creditos electivos", minimo=0)
    @property
    def creditos_extracurriculares(self):
        return self.__extracurriculares
    @creditos_extracurriculares.setter
    def creditos_extracurriculares(self, valor):
        self.__extracurriculares = validar_numero(
            valor, "Creditos extracurriculares", minimo=0
        )
    @property
    def vigente(self):
        return self.__vigente
    @vigente.setter
    def vigente(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("Vigente debe ser True o False.")
        self.__vigente = valor
    @property
    def creditos_totales(self):
        return (self.creditos_obligatorios + self.creditos_electivos
                + self.creditos_extracurriculares)
    def resumen(self):
        return "Plan de estudio: " + self.nombre
# ACTIVIDAD 2: comprueba los datos obligatorios de la escuela.
class EscuelaProfesional(EntidadNombrada):
    def __init__(self, codigo, nombre, informacion, perfil, codigo_director,
                 codigo_secretario):
        super().__init__(nombre)
        self.codigo = validar_texto(codigo, "Codigo de escuela")
        self.informacion = validar_texto(informacion, "Informacion")
        self.perfil = validar_texto(perfil, "Perfil profesional")
        self.codigo_director = validar_texto(codigo_director, "Codigo del director")
        self.codigo_secretario = validar_texto(codigo_secretario, "Codigo del secretario")
    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, valor):
        self.__nombre = validar_texto(valor, "Nombre de escuela")
    def resumen(self):
        return "Escuela profesional: " + self.nombre
    
# ACTIVIDAD 2: valida fechas, nota minima, tipo de periodo y estados del 1 al 4.
class PeriodoAcademico(EntidadNombrada):
    ESTADOS = (1, 2, 3, 4)  # 1 planificado, 2 en curso, 3 matricula cerrada, 4 finalizado
    def __init__(self, nombre, numero, año, fecha_inicio, fecha_fin,
                 inicio_matricula, fin_matricula, es_verano, nota_minima, estado):
        super().__init__(nombre)
        self.numero = validar_entero(numero, "Numero de periodo", 1)
        self.año = validar_entero(año, "Año", 1)
        self.fecha_inicio = validar_fecha(fecha_inicio, "Fecha de inicio")
        self.fecha_fin = validar_fecha(fecha_fin, "Fecha de fin")
        self.inicio_matricula = validar_fecha(inicio_matricula, "Inicio de matricula")
        self.fin_matricula = validar_fecha(fin_matricula, "Fin de matricula")
        if self.fecha_inicio > self.fecha_fin:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha de fin.")
        if self.inicio_matricula > self.fin_matricula:
            raise ValueError("El inicio de matricula no puede ser posterior al fin.")
        self.es_verano = es_verano
        self.nota_minima = nota_minima
        self.estado = estado
    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, valor):
        self.__nombre = validar_texto(valor, "Nombre del periodo", 45)
    @property
    def es_verano(self):
        return self.__es_verano
    @es_verano.setter
    def es_verano(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("Es verano debe ser True o False.")
        self.__es_verano = valor
    @property
    def nota_minima(self):
        return self.__nota_minima
    @nota_minima.setter
    def nota_minima(self, valor):
        self.__nota_minima = validar_numero(valor, "Nota minima", 0, 20)
    @property
    def estado(self):
        return self.__estado
    @estado.setter
    def estado(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int) or valor not in self.ESTADOS:
            raise ValueError("Estado debe ser el entero 1, 2, 3 o 4.")
        self.__estado = valor
    def resumen(self):
        return "Periodo academico: " + self.nombre
# ACTIVIDAD 3 - ABSTRACCION:
class Persona(ABC):
    def __init__(self, dni, nombres, apellidos):
        self.dni = validar_texto(dni, "DNI")
        self.nombres = validar_texto(nombres, "Nombres")
        self.apellidos = validar_texto(apellidos, "Apellidos")
    @property
    def nombre_completo(self):
        return self.nombres + " " + self.apellidos
    @abstractmethod
    def obtener_codigo(self):
        pass
    @abstractmethod
    def obtener_rol(self):
        pass
# ACTIVIDADES 3 y 4: Estudiante hereda Persona y agrega sus codigos.
class Estudiante(Persona):
    def __init__(self, dni, nombres, apellidos, codigo_estudiante, codigo_escuela):
        super().__init__(dni, nombres, apellidos)
        self.codigo_estudiante = validar_texto(codigo_estudiante, "Codigo de estudiante")
        self.codigo_escuela = validar_texto(codigo_escuela, "Codigo de escuela")
    def obtener_codigo(self):
        return self.codigo_estudiante
    def obtener_rol(self):
        return "Estudiante"
# ACTIVIDADES 3 y 4: Docente hereda Persona y agrega su codigo.
class Docente(Persona):
    def __init__(self, dni, nombres, apellidos, codigo_docente):
        super().__init__(dni, nombres, apellidos)
        self.codigo_docente = validar_texto(codigo_docente, "Codigo de docente")
    def obtener_codigo(self):
        return self.codigo_docente
    def obtener_rol(self):
        return "Docente"
# Datos del caso OTI / UNSCH
curso = Curso("IS-283", "Programacion Orientada a Objetos", 3.5, 2, 2)
plan = PlanEstudio("Ingenieria de Sistemas", 2025, 160, 20.5, 2)
escuela = EscuelaProfesional("EPIS", "Ingenieria de Sistemas", "Escuela UNSCH", "Formar profesionales", "DOC-001", "DOC-002")
periodo = PeriodoAcademico("2026-I", 1, 2026, "2026-03-16", "2026-07-24", "2026-03-02", "2026-03-13", False, 11, 1)
seccion = Seccion("A", curso.codigo, "2026-I", 2)
estudiante = Estudiante("12345678", "Valeria", "Huaman Quispe", "EST-014", "EPIS")
docente = Docente("87654321", "Pelayo", "Bautista Quispe", "DOC-014")
# Pruebas compactas de propiedades: se comprueba asignacion valida e invalida.
def probar_atributo(nombre, objeto, atributo, bueno, malo):
    try:
        setattr(objeto, atributo, bueno)
        print("ACEPTADO:", nombre, "valor valido")
    except Exception as e:
        print("ERROR INESPERADO:", nombre, e)
    try:
        setattr(objeto, atributo, malo)
        print("RECHAZO FALLIDO:", nombre, "acepto", repr(malo))
    except (ValueError, AttributeError, TypeError) as e:
        print("RECHAZADO:", nombre, "->", e)
def probar_constructor(nombre, clase, args, indice, malo):
    try:
        clase(*args)
        print("ACEPTADO:", nombre, "constructor valido")
    except Exception as e:
        print("ERROR INESPERADO:", nombre, e)
    malos = list(args)
    malos[indice] = malo
    try:
        clase(*malos)
        print("RECHAZO FALLIDO:", nombre, "acepto", repr(malo))
    except (ValueError, TypeError) as e:
        print("RECHAZADO:", nombre, "->", e)
print("=== ACTIVIDAD 2: PRUEBAS PRINCIPALES ===")
# 1-3 Curso: texto, creditos y horas.
probar_constructor("Curso/codigo obligatorio", Curso, ["IS-283", "Programacion", 3, 2, 2], 0, "")
probar_constructor("Curso/nombre maximo 200", Curso, ["IS-283", "Programacion", 3, 2, 2], 1, "N"*201)
probar_atributo("Curso/creditos positivos y maximo 2 decimales", curso, "creditos", 3.25, 3.456)
probar_atributo("Curso/horas entre 0 y 255", curso, "horas_teoria", 3, 256)
try:
    curso.id = 99
    print("RECHAZO FALLIDO: ID modificable")
except AttributeError:
    print("RECHAZADO: ID de solo lectura")
print("ACEPTADO: horas totales calculadas =", curso.horas_totales)
# 5-6 Seccion: vacantes y matricula.
probar_atributo("Seccion/vacantes positivas", seccion, "vacantes", 2, 0)
seccion.matricular(); seccion.matricular()
try:
    seccion.matricular()
    print("RECHAZO FALLIDO: seccion llena")
except ValueError as e:
    print("RECHAZADO: matricula sin vacantes ->", e)
# 7-8 Plan: nombre, creditos y vigente.
probar_constructor("Plan/nombre maximo 36", PlanEstudio, ["Ingenieria", 2025, 100, 20, 2], 0, "N"*37)
probar_atributo("Plan/creditos no negativos", plan, "creditos_obligatorios", 120, -1)
probar_atributo("Plan/vigente booleano", plan, "vigente", False, 1)
print("ACEPTADO: creditos totales calculados =", plan.creditos_totales)
# 9 Escuela: los datos de texto son obligatorios.
probar_constructor("Escuela/codigo obligatorio", EscuelaProfesional, ["EPIS", "Ingenieria", "Info", "Perfil", "DOC-1", "DOC-2"], 0, "")
# 10-13 Periodo: fecha, año, nota y estado.
probar_constructor("Periodo/año positivo", PeriodoAcademico, ["2026-I", 1, 2026, "2026-03-01", "2026-07-01", "2026-02-01", "2026-02-15", False, 11, 1], 2, 0)
probar_constructor("Periodo/fecha real", PeriodoAcademico, ["2026-I", 1, 2026, "2026-03-01", "2026-07-01", "2026-02-01", "2026-02-15", False, 11, 1], 3, "2026-02-30")
probar_atributo("Periodo/nota entre 0 y 20", periodo, "nota_minima", 12, 21)
probar_atributo("Periodo/estado entre 1 y 4", periodo, "estado", 2, 7)
# 14-15 Persona: campos obligatorios y codigo de docente.
probar_constructor("Estudiante/DNI obligatorio", Estudiante, ["12345678", "Ana", "Perez", "EST-1", "EPIS"], 0, "")
probar_constructor("Docente/codigo obligatorio", Docente, ["12345678", "Pelayo", "Bautista Quispe", "DOC-014"], 3, "")
print("\n=== ACTIVIDADES 3 Y 4: ABSTRACCION, HERENCIA Y POLIMORFISMO ===")
for clase, args in [(EntidadNombrada, ("Entidad",)), (Persona, ("12345678", "Ana", "Perez"))]:
    try:
        clase(*args)
        print("RECHAZO FALLIDO: se instancio clase abstracta")
    except TypeError as e:
        print("RECHAZADO: clase abstracta ->", e)
for objeto in [curso, plan, escuela, periodo]:
    print(objeto.resumen())
for persona in [estudiante, docente]:
    print(persona.nombre_completo, "-", persona.obtener_rol(), "-", persona.obtener_codigo())
