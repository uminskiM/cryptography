#include <gmp.h>

class NumberTheory {
    public:
        //C++ Adaptation of https://github.com/nymble/cryptopy/blob/master/ecc/numbertheory.py
        void square_root_modulo(mpz_t result, const mpz_t number, const mpz_t base) {
            mpz_t t, s, n, x, b, g, u;
            mpz_inits(t, s, n, x, b, g, u, NULL);

            if (mpz_legendre(number, base) != 1) {
                mpz_set_ui(result, 0);
                return;
            } else if (mpz_cmp_ui(number, 0) == 0) {
                mpz_set_ui(result, 0);
                return;
            } else if (mpz_cmp_ui(base, 2) == 0) {
                mpz_set(result, base);
                return;
            } else if (mpz_mod_ui(t, base, 4), mpz_cmp_ui(t, 3) == 3) {
                mpz_add_ui(t, base, 1);
                mpz_fdiv_q_ui(t, t, 4);
                mpz_powm(result, number, t, base);
                return;
            }

            mpz_sub_ui(s, base, 1);
            unsigned int e = 0;
            while (mpz_mod_ui(t, s, 2), mpz_cmp_ui(t, 0) == 0) {
                mpz_fdiv_q_ui(s, s, 2);
                e++;
            }

            for (mpz_set_ui(n, 2); mpz_legendre(n, base) != -1; mpz_add_ui(n, n, 1));

            mpz_add_ui(x, s, 1);
            mpz_fdiv_q_ui(x, x, 2);
            mpz_powm(x, number, x, base);
            mpz_powm(b, number, s, base);
            mpz_powm(g, n, s, base);
            unsigned int iterator, rr = e;

            while (true) {
                mpz_set(t, b);
                for (iterator = 0; iterator < rr; iterator++) {
                    if (mpz_cmp_ui(t, 1) == 0) {
                        break;
                    }
                    mpz_powm_ui(t, t, 2, base);
                }

                if (iterator == 0) {
                    mpz_set(result, x);
                    return;
                }

                mpz_ui_pow_ui(t, 2, rr - iterator - 1);
                mpz_powm(u, g, t, base);
                mpz_powm_ui(g, u, 2, base);
                mpz_mul(x, x, u);
                mpz_mod(x, x, base);
                mpz_mul(b, b, g);
                mpz_mod(b, b, base);
                rr = iterator;
            }

            mpz_clears(t, s, n, x, b, g, u, NULL);
        }
};