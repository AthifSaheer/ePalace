import uuid    


def generate_ref_code():
    code = str(uuid.uuid4()).replace("-","")[:12]
    return code

def generate_cupon():
    cupon_code = str(uuid.uuid4())[:4]
    return cupon_code