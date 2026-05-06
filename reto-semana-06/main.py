import re
from typing import Dict, List
from datetime import datetime

# Departamentos válidos para empleados
DEPARTAMENTOS_VALIDOS = ['VEN', 'ADM', 'TEC', 'LOG', 'RHH']

# Series válidas para facturas
SERIES_VALIDAS = ['A', 'B', 'C', 'D', 'E']

# --- PARTE 1: Funciones de validación individual ---

def validar_producto(codigo: str) -> Dict:
    """Valida código de producto: ABC-1234-MX"""
    # Patrón: 3 letras mayúsculas, guion, 4 dígitos, guion, 2 letras mayúsculas
    patron = r'^([A-Z]{3})-(\d{4})-([A-Z]{2})$'
    match = re.match(patron, codigo)
    
    resultado = {"valido": False, "categoria": None, "numero": None, "pais": None}
    if match:
        resultado.update({
            "valido": True,
            "categoria": match.group(1),
            "numero": match.group(2),
            "pais": match.group(3)
        })
    return resultado

def validar_envio(codigo: str) -> Dict:
    """Valida código de envío: ENV-YYYY-MM-DD-NNNNNN[cite: 1]"""
    # Patrón: Prefijo ENV, Año (2020-2030), Mes (01-12), Día (01-31), 6 dígitos
    patron = r'^ENV-(202[0-9]|2030)-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])-(\d{6})$'
    match = re.match(patron, codigo)
    
    resultado = {"valido": False, "fecha": None, "secuencial": None}
    if match:
        fecha_str = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
        resultado.update({
            "valido": True,
            "fecha": fecha_str,
            "secuencial": match.group(4)
        })
    return resultado

def validar_empleado(codigo: str) -> Dict:
    """Valida código de empleado: EMP-XXX-NNNN[cite: 1]"""
    # Patrón: Prefijo EMP, 3 letras dep, 4 dígitos (no empieza con 0)
    patron = r'^EMP-([A-Z]{3})-([1-9]\d{3})$'
    match = re.match(patron, codigo)
    
    resultado = {"valido": False, "departamento": None, "numero": None}
    if match:
        depto = match.group(1)
        if depto in DEPARTAMENTOS_VALIDOS:
            resultado.update({
                "valido": True,
                "departamento": depto,
                "numero": match.group(2)
            })
    return resultado

def validar_factura(codigo: str) -> Dict:
    """Valida código de factura: FAC-S-NNNNNN[cite: 1]"""
    # Patrón: Prefijo FAC, 1 letra serie, 6 dígitos
    patron = r'^FAC-([A-Z])-(\d{6})$'
    match = re.match(patron, codigo)
    
    resultado = {"valido": False, "serie": None, "numero": None}
    if match:
        serie = match.group(1)
        if serie in SERIES_VALIDAS:
            resultado.update({
                "valido": True,
                "serie": serie,
                "numero": match.group(2)
            })
    return resultado

# --- PARTE 2: Validador universal ---

def validar_codigo(codigo: str) -> Dict:
    """Detecta el tipo de código y lo valida[cite: 1]"""
    resultado = {"codigo": codigo, "tipo": "desconocido", "valido": False, "detalles": {}}
    
    if codigo.startswith("ENV-"):
        resultado["tipo"] = "envio"
        res = validar_envio(codigo)
    elif codigo.startswith("EMP-"):
        resultado["tipo"] = "empleado"
        res = validar_empleado(codigo)
    elif codigo.startswith("FAC-"):
        resultado["tipo"] = "factura"
        res = validar_factura(codigo)
    elif re.match(r'^[A-Z]{3}-\d', codigo):
        resultado["tipo"] = "producto"
        res = validar_producto(codigo)
    else:
        return resultado

    resultado["valido"] = res.pop("valido")
    resultado["detalles"] = res
    return resultado

# --- PARTE 3: Procesamiento por lotes ---

def procesar_lote(codigos: List[str]) -> Dict:
    """Procesa múltiples códigos y genera estadísticas[cite: 1]"""
    reporte = {
        "total": len(codigos),
        "validos": 0,
        "invalidos": 0,
        "por_tipo": {
            "producto": {"total": 0, "validos": 0},
            "envio": {"total": 0, "validos": 0},
            "empleado": {"total": 0, "validos": 0},
            "factura": {"total": 0, "validos": 0},
            "desconocido": {"total": 0, "validos": 0}
        },
        "detalle": []
    }
    
    for c in codigos:
        res = validar_codigo(c)
        tipo = res["tipo"]
        
        reporte["por_tipo"][tipo]["total"] += 1
        if res["valido"]:
            reporte["validos"] += 1
            reporte["por_tipo"][tipo]["validos"] += 1
        else:
            reporte["invalidos"] += 1
        
        reporte["detalle"].append(res)
        
    return reporte