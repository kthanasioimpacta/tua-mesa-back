import time
def setCookie(response,token):
    lease = 14 * 24 * 60 * 60  # 14 days in seconds
    end = time.gmtime(time.time() + lease)
    expires = time.strftime("%a, %d-%b-%Y %T GMT", end)
    response.set_cookie('token', token.decode('ascii'), secure=False, domain='.tuamesa.com.br', expires=expires)
    return response