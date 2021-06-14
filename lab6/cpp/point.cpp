#include <gmp.h>

class Point {
    public:
        mpz_t x;
        mpz_t y;

        Point() {
            mpz_inits(x, y, NULL);
        }

        Point(mpz_t x_value, mpz_t y_value) {
           mpz_set(x, x_value);
           mpz_set(y, y_value); 
        };
};