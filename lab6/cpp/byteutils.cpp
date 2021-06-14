#include <gmp.h>

class ByteUtils {
    public:
        void push_byte(mpz_t number, unsigned char byte_as_char) {
            mpz_mul_ui(number, number, 256);
            mpz_add_ui(number, number, byte_as_char);
        }

        unsigned char get_byte_from_number(mpz_t number, size_t i) {
            int multiplied_by_eight = i * 8;
            return mpz_tstbit(number, multiplied_by_eight + 0) << 0 
            | mpz_tstbit(number, multiplied_by_eight + 1) << 1 
            | mpz_tstbit(number, multiplied_by_eight + 2) << 2 
            | mpz_tstbit(number, multiplied_by_eight + 3) << 3 
            | mpz_tstbit(number, multiplied_by_eight + 4) << 4 
            | mpz_tstbit(number, multiplied_by_eight + 5) << 5 
            | mpz_tstbit(number, multiplied_by_eight + 6) << 6 
            | mpz_tstbit(number, multiplied_by_eight + 7) << 7;
        }
};