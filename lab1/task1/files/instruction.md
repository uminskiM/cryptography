Generate public key from a certificate:
openssl x509 -pubkey -in cacertificate.pem -noout > pubkey.pem

Verify grade.txt file
openssl dgst -md5 -verify pubkey.pem  -signature grade.sign grade.txt

Change the grade.xtt file

Get the modulus from the public key
openssl rsa -inform PEM -text -noout -pubin < pubkey.pem

0x00e649d57f6ff9cff655cb79ee38380c8f8278eb374a90059b0ff06534829d337c753d0e59afed6fa489f015cf33

./cado-nfs.py 2112664634855999140031945945998785346946804826144846396410436155861557104011009549879696604291518474904522547 -t all

p = 1385409854850246784644682622624349784560468558795524903
q = 1524938362073628791222322453937223798227099080053904149

python3 private-key-generator.py

openssl dgst -md5 -sign generated.pem -out generated.sign grade_changed.txt

openssl dgst -md5 -verify pubkey.pem -signature generated.sign grade_changed.txt