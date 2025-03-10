# Hechos conocidos
hechos = {
    "Juan tiene fiebre": True,
    "Juan tiene tos": True,
    "Juan es adulto": True,
}

# Reglas de inferencia
def regla_1():
    if hechos["Juan tiene fiebre"] and hechos["Juan tiene tos"]:
        return "Juan puede tener gripe"
    return None

def regla_2():
    if hechos["Juan tiene fiebre"] and hechos["Juan es adulto"]:
        return "Juan puede tener COVID-19"
    return None

# Motor de inferencia
def motor_de_inferencia():
    inferencias = []
    inferencia_1 = regla_1()
    if inferencia_1:
        inferencias.append(inferencia_1)

    inferencia_2 = regla_2()
    if inferencia_2:
        inferencias.append(inferencia_2)

    return inferencias

# Ejecutar motor de inferencia
inferencias = motor_de_inferencia()
print("Inferencias:", inferencias)
