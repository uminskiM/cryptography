openssl x509 -pubkey -noout -in cacertSec.pem > pubkey.pem

Download hashclash and build it

Create workdir in the hashclash folder, insert grade.txt and grade_changed.txt

Go to workdir, run `../scripts/cpc.sh grade.txt grade_changed.txt`

grade.txt.coll and grade_changed.txt.coll are generated, check their hashes using `md5sum`