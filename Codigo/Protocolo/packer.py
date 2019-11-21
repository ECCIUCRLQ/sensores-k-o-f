import struct

# Mensaje que solicita desde ML guardar una página en un NM
# Desde ML hacia ID y de ID a NM
def store_package(op_code, id_page, page_size, data):
    package_format = "=BBI" + str(page_size) + "s"
    package = struct.pack(package_format, op_code, id_page, page_size, data)
    return package

# Mensaje que solicita desde ML lectura de una página en un NM
# Se usa tambien en ID para decir que se pudo guardar una página en NM
# Desde ML hacia ID y de ID a NM
# Desde ID hacia ML
def read_package_store_ok(op_code, id_page):
    package_format = "=BB"
    package = struct.pack(package_format, op_code, id_page)
    return package

# Mensaje que devuelve el NM cuando guarda para la ID
# Desde NM hacia ID
def store_answer_NM_ID(op_code, id_page, node_size):
    package_format = "=BBI"
    package = struct.pack(package_format, op_code, id_page, node_size)
    return package

# Mensaje que informa quien quiere página
# Desde ID hacia ML y de NM a ID
def read_answer(op_code, id_page, data):
    package_format = "=BB" + str(len(data)) + "s"
    package = struct.pack(package_format, op_code, id_page, data)
    return package