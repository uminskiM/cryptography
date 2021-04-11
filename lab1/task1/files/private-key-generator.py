from Crypto.PublicKey import RSA 
import base64

e = 0x010001
n = 0x00e649d57f6ff9cff655cb79ee38380c8f8278eb374a90059b0ff06534829d337c753d0e59afed6fa489f015cf33
p = 1385409854850246784644682622624349784560468558795524903
q = 1524938362073628791222322453937223798227099080053904149

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

phi = (p -1)*(q-1)

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

d = modinv(e,phi)


private_key = RSA.construct((n, e, d, p, q))
f = open('generated.pem', 'w')
f.write(private_key.exportKey('PEM').decode())
f.close()