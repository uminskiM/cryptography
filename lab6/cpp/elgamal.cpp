#include <gmp.h>
#include <string.h>
#include "edwards.cpp"
#include "byteutils.cpp"

class ElGamal {
    public:
        char get_random_byte(void) {
            static FILE *r = NULL;
            if (r == NULL) {
                r = fopen("/dev/urandom", "r");
                if (r == NULL) {
                    perror("/dev/urandom");
                    exit(1);
                }
            }
            return fgetc(r);
        }


        void encrypt(gmp_randstate_t random_state, EdwardsCurve382 *curve, Point *base, Point *public_key, const char *message, Point *base_to_private_key, Point *encryption_result) {
            Point encrypted_point;
            mpz_t random_number;
            mpz_inits(random_number, encrypted_point.x, encrypted_point.y, NULL);

            mpz_urandomb(random_number, random_state, 16);

            ByteUtils byte_utils;
            byte_utils.push_byte(encrypted_point.x, strlen(message));

            for (size_t i = 0; message[i] != '\0'; i++) {
                byte_utils.push_byte(encrypted_point.x, message[i]);
            }

            for (;;) {
                curve->find_y_for_x_on_curve(&encrypted_point);
                if (mpz_cmp_ui(encrypted_point.y, 0) != 0) {
                    break;
                }
                byte_utils.push_byte(encrypted_point.x, get_random_byte());
            }

            curve->multiply_point_by_scalar(encryption_result, public_key, random_number);
            curve->multiply_point_by_scalar(base_to_private_key, base, random_number);
            curve->add_points(encryption_result, encryption_result, &encrypted_point);

            mpz_clears(random_number, encrypted_point.x, encrypted_point.y, NULL);
        }

        char *decrypt(EdwardsCurve382 *curve, Point *base, const mpz_t private_key, Point *base_to_private_key, Point *encryption_result) {
            Point auxiliary_point, decrypted_point;
            mpz_inits(auxiliary_point.x, auxiliary_point.y, decrypted_point.x, decrypted_point.y, NULL);

            curve->multiply_point_by_scalar(&auxiliary_point, base_to_private_key, private_key);
            curve->subtract_points(&decrypted_point, encryption_result, &auxiliary_point);

            ByteUtils byte_utils;
            ssize_t binary_number_length = (mpz_sizeinbase(decrypted_point.x, 2) + 7) / 8;
            ssize_t byte_from_numnber = byte_utils.get_byte_from_number(decrypted_point.x, binary_number_length - 1);

            char *message = (char*)malloc(byte_from_numnber + 1);
            if (message == NULL) {
                perror("malloc");
                exit(1);
            }

            ssize_t i, n = 0;
            for (i = binary_number_length - 2; i > binary_number_length - byte_from_numnber - 2; i--) {
                message[n++] = byte_utils.get_byte_from_number(decrypted_point.x, i);
            }
            message[n] = '\0';

            mpz_clears(auxiliary_point.x, auxiliary_point.y, decrypted_point.x, decrypted_point.y, NULL);
            return message;
        }
};
