import time
from hashlib import sha256
from random import randint

NONCE_BYTES = 16
def get_nonce():
    return "{:032x}".format(randint(0, 2**(8 * NONCE_BYTES)))


def sign(params, secret):
    signed_params = dict(params)
    algo = sha256()
    signed_params.update(nonce=get_nonce())
    signed_params.update(timestamp=time.time())
    for key, value in sorted(signed_params.iteritems()):
        algo.update(str(value))
    algo.update(secret)

    signature = algo.hexdigest()
    return dict(signed_params,
                signature=signature)


def verify(signed_params, secret):
    timestamp = signed_params.get("timestamp")
    if timestamp is None:
        return False
    try:
        timestamp = float(timestamp)
    except (TypeError, ValueError):
        return False
    now = time.time()
    if abs(now - timestamp) > 3 * 60:
        return False
    signature = signed_params.pop('signature', None)
    if signature is None:
        return False
    algo = sha256()
    for key, value in sorted(signed_params.iteritems()):
        algo.update(str(value))
    algo.update(secret)
    return algo.hexdigest() == signature
