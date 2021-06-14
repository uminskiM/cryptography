#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <gmp.h>
#include "elgamal.cpp"

gmp_randstate_t random_state;

int main() {
    gmp_randinit_default(random_state);
    ElGamal el_gamal;
    mpz_t private_key;
    EdwardsCurve382 edwards_elliptic_curve;
    Point base_of_encryption, public_key, base_to_private_key, encryption_result;
    mpz_inits(private_key, edwards_elliptic_curve.n, edwards_elliptic_curve.d, base_of_encryption.x, base_of_encryption.y, public_key.x, public_key.y, base_to_private_key.x, base_to_private_key.y, encryption_result.x, encryption_result.y, NULL);

    mpz_set_str(edwards_elliptic_curve.n,  "0x3fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff97", 0);
    mpz_set_str(edwards_elliptic_curve.d,  "-67254", 0);
    mpz_set_str(base_of_encryption.x, "0x196f8dd0eab20391e5f05be96e8d20ae68f840032b0b64352923bab85364841193517dbce8105398ebc0cc9470f79603", 0);
    mpz_set_str(base_of_encryption.y, "0x11", 0);

    mpz_urandomb(private_key, random_state, 16);
    edwards_elliptic_curve.multiply_point_by_scalar(&public_key, &base_of_encryption, private_key);

    el_gamal.encrypt(random_state, &edwards_elliptic_curve, &base_of_encryption, &public_key, "Lets check if ElGamal encrypts correctly", &base_to_private_key, &encryption_result);

    char *result = el_gamal.decrypt(&edwards_elliptic_curve, &base_of_encryption, private_key, &base_to_private_key, &encryption_result);
    puts(result);
    free(result);

    mpz_clears(private_key, edwards_elliptic_curve.n, edwards_elliptic_curve.d, base_of_encryption.x, base_of_encryption.y, public_key.x, public_key.y, base_to_private_key.x, base_to_private_key.y, encryption_result.x, encryption_result.y, NULL);

    return 0;
}
