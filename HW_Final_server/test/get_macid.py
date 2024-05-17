import uuid

def get_mac_address():
    try:
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e+2] for e in range(0, 11, 2)])
    except:
        return "00:00:00:00:00:00"
    
print(get_mac_address())