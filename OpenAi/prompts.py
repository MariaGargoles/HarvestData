
prompt = (
    "Genera una lista completa de espectáculos independientes actuales en España, "
    "proporcionando detalles sobre el nombre del espectáculo, la fecha y el lugar. "
    "La respuesta debe estar estrictamente en formato JSON con la siguiente estructura: "
    "{ 'espectaculos': { 'Nombre de la compañía': [ { 'nombre': 'Nombre del espectáculo', 'fecha': 'DD/MM/AAAA', 'lugar': 'Ubicación' } ] } }. "
    "A continuación, algunos ejemplos de la estructura esperada: "
    "{ 'espectaculos': { 'Carabdanza': [ { 'nombre': 'Four Seasons', 'fecha': '02/01/2025', 'lugar': 'Albacete' } ] } }. "
    "Proporciona la información solo si es relevante y está disponible. "
    "Si no hay información, devuelve un JSON vacío: { 'espectaculos': {} }."
)



prompt = (
    "Recopila todas las funciones programadas para el año 2025 de la Compañía Nómada en el Teatro Victoria. "
    "Asegúrate de obtener la información desde cualquier sección relevante dentro del sitio web del Teatro Victoria (https://elteatrovictoria.com/cia-nomada/). "
    "Devuelve la respuesta en formato JSON con la siguiente estructura: "
    "{ "
    "\"Compañía Nómada\": [ "
    "{ "
    "\"nombre\": \"Nombre del espectáculo\", "
    "\"fecha\": \"Fecha del evento\", "
    "\"lugar\": \"Lugar del evento\" "
    "} "
    "] "
    "} "
    "Si no encuentras información específica sobre funciones en 2025, responde con un JSON vacío bajo la clave \"Compañía Nómada\"."
)

prompt = (
    f"Lista todas las funciones actuales y próximas de la compañía {nombre}, "
    "incluyendo el nombre del espectáculo, la fecha y la ubicación. "
    "Si no hay información disponible sobre funciones específicas, responde con 'No hay datos disponibles'. "
    "Devuelve la respuesta en formato JSON con la estructura: "
    "{ 'espectaculos': [ { 'nombre': 'Nombre del espectáculo', 'fecha': 'DD/MM/AAAA', 'ubicacion': 'Lugar' } ] }."
)
