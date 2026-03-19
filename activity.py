from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass(frozen=True)
class Persona:
    dni: str
    nombre: str
    apellido: str
    edad: int

    def __post_init__(self):
        # Validación de nulos (asumiendo que nombre y apellido no pueden ser vacíos)
        if not self.nombre or not self.apellido:
            raise ValueError("El nombre y el apellido no pueden ser nulos o vacíos.")
        # Validación de edad
        if self.edad < 0:
            raise ValueError(f"La edad no puede ser negativa. Valor recibido: {self.edad}")
        
class RegistroPersonas:
    def __init__(self, datos: List[Tuple[str, str, str, int]]):
        self._personas: Dict[str, Persona] = {}
        self._cargar_datos(datos)

    def _cargar_datos(self, datos: List[Tuple[str, str, str, int]]):
        for dni, nombre, apellido, edad in datos:
            if dni in self._personas:
                raise ValueError(f"Error: DNI duplicado encontrado ({dni}).")
            
            # Instanciamos la persona. Si hay un error de validación, se lanzará desde __post_init__
            nueva_persona = Persona(dni, nombre, apellido, edad)
            self._personas[dni] = nueva_persona

    def formatear_registros(self) -> Dict[str, Tuple[str, str, int]]:
        """Devuelve un diccionario con el DNI como clave y el resto como tupla."""
        return {dni: (p.nombre, p.apellido, p.edad) for dni, p in self._personas.items()}

    def obtener_mayor_edad(self) -> Persona:
        if not self._personas:
            raise ValueError("El registro está vacío.")
        # Compara basándose en el atributo 'edad' de cada objeto Persona
        return max(self._personas.values(), key=lambda p: p.edad)

    def obtener_menor_edad(self) -> Persona:
        if not self._personas:
            raise ValueError("El registro está vacío.")
        return min(self._personas.values(), key=lambda p: p.edad)

    def segmentar_por_edad(self, umbral: int = 25) -> Tuple[List[Persona], List[Persona]]:
        """Devuelve dos listas: (menores al umbral, mayores o iguales al umbral)."""
        menores = [p for p in self._personas.values() if p.edad < umbral]
        mayores = [p for p in self._personas.values() if p.edad >= umbral]
        return menores, mayores

    def promedio_edad(self) -> float:
        if not self._personas:
            return 0.0
        suma_edades = sum(p.edad for p in self._personas.values())
        return suma_edades / len(self._personas)

    def consultar_edad_por_dni(self, dni: str) -> int:
        """Acceso en tiempo O(1) gracias al uso del diccionario interno."""
        if dni not in self._personas:
            raise KeyError(f"El DNI {dni} no se encuentra registrado.")
        return self._personas[dni].edad
    
if __name__ == "__main__":
    # Estos son los datos de prueba simulando el sistema legacy
    datos_crudos = [
        ('11111111', 'Pedro', 'Paez', 24),
        ('22222222', 'Maria', 'Gomez', 30),
        ('33333333', 'Juan', 'Perez', 19),
        ('44444444', 'Ana', 'Lopez', 25)
    ]

    # Creamos el registro
    registro = RegistroPersonas(datos_crudos)

    # Imprimimos los resultados en la terminal
    print("--- Formateo de Registros ---")
    print(registro.formatear_registros())

    print("\n--- Extremos de Edad ---")
    print("Mayor:", registro.obtener_mayor_edad().nombre)
    print("Menor:", registro.obtener_menor_edad().nombre)

    print("\n--- Segmentación (Umbral 25) ---")
    menores, mayores = registro.segmentar_por_edad(25)
    print(f"Menores de 25: {[p.nombre for p in menores]}")
    print(f"Mayores o iguales a 25: {[p.nombre for p in mayores]}")

    print("\n--- Promedio de Edad ---")
    print(f"{registro.promedio_edad()} años")

    print("\n--- Acceso Directo por DNI ---")
    print("Edad del DNI '22222222':", registro.consultar_edad_por_dni('22222222'))