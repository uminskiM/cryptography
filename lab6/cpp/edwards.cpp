#include <gmp.h>
#include "numbertheory.cpp"
#include "point.cpp"

class EdwardsCurve382 {
    public: 
        mpz_t n, d;

    void find_y_for_x_on_curve(Point *point) {
        NumberTheory number_theory;
        mpz_t temporary;
        mpz_init(temporary);
        mpz_pow_ui(temporary, point->x, 2);
        mpz_mul(point->y, d, temporary);
        mpz_sub_ui(point->y, point->y, 1);
        mpz_invert(point->y, point->y, n);
        mpz_sub_ui(temporary, temporary, 1);
        mpz_mul(point->y, point->y, temporary);
        mpz_mod(point->y, point->y, n);
        number_theory.square_root_modulo(point->y, point->y, n);
        mpz_clear(temporary);
    }

    void add_points(Point *result, Point *first, Point *second) {
        Point temporary_result;
        mpz_t temporary, multiplication_result, n_minus_two;
        mpz_inits(temporary, multiplication_result, n_minus_two, temporary_result.x, temporary_result.y, NULL);

        mpz_sub_ui(n_minus_two, n, 2);

        mpz_set(multiplication_result, d);
        mpz_mul(multiplication_result, multiplication_result, first->x);
        mpz_mul(multiplication_result, multiplication_result, first->y);
        mpz_mul(multiplication_result, multiplication_result, second->x);
        mpz_mul(multiplication_result, multiplication_result, second->y);

        // x
        mpz_mul(temporary_result.x, first->x, second->y);
        mpz_mul(temporary, first->y, second->x);
        mpz_add(temporary_result.x, temporary_result.x, temporary);

        mpz_add_ui(temporary, multiplication_result, 1);
        mpz_powm(temporary, temporary, n_minus_two, n);
        mpz_mul(temporary_result.x, temporary_result.x, temporary);
        mpz_mod(temporary_result.x, temporary_result.x, n);

        // y
        mpz_mul(temporary_result.y, first->y, second->y);
        mpz_mul(temporary, first->x, second->x);
        mpz_sub(temporary_result.y, temporary_result.y, temporary);

        mpz_ui_sub(temporary, 1, multiplication_result);
        mpz_powm(temporary, temporary, n_minus_two, n);
        mpz_mul(temporary_result.y, temporary_result.y, temporary);
        mpz_mod(temporary_result.y, temporary_result.y, n);

        mpz_set(result->x, temporary_result.x);
        mpz_set(result->y, temporary_result.y);

        mpz_clears(temporary, multiplication_result, n_minus_two, temporary_result.x, temporary_result.y, NULL);
    }

    void double_point(Point *result, Point *point) {
        Point temporary_result;
        mpz_t temporary, auxiliary_value, n_minus_two;
        mpz_inits(temporary, auxiliary_value, n_minus_two, temporary_result.x, temporary_result.y, NULL);

        mpz_sub_ui(n_minus_two, n, 2);

        mpz_pow_ui(auxiliary_value, point->x, 2);
        mpz_pow_ui(temporary, point->y, 2);
        mpz_sub(temporary_result.y, temporary, auxiliary_value);
        mpz_add(auxiliary_value, auxiliary_value, temporary);

        // x
        mpz_set_ui(temporary_result.x, 2);
        mpz_mul(temporary_result.x, temporary_result.x, point->x);
        mpz_mul(temporary_result.x, temporary_result.x, point->y);

        mpz_powm(temporary, auxiliary_value, n_minus_two, n);
        mpz_mul(temporary_result.x, temporary_result.x, temporary);
        mpz_mod(temporary_result.x, temporary_result.x, n);

        // y
        mpz_ui_sub(temporary, 2, auxiliary_value);
        mpz_powm(temporary, temporary, n_minus_two, n);
        mpz_mul(temporary_result.y, temporary_result.y, temporary);
        mpz_mod(temporary_result.y, temporary_result.y, n);

        mpz_set(result->x, temporary_result.x);
        mpz_set(result->y, temporary_result.y);

        mpz_clears(temporary, auxiliary_value, n_minus_two, temporary_result.x, temporary_result.y, NULL);
    }

    void subtract_points(Point *result, Point *first, Point *second) {
        Point negated_second;
        mpz_inits(negated_second.x, negated_second.y, NULL);
        mpz_neg(negated_second.x, second->x);
        mpz_set(negated_second.y, second->y);
        add_points(result, first, &negated_second);
        mpz_clears(negated_second.x, negated_second.y, NULL);
    }

    void multiply_point_by_scalar(Point *result, Point *point, const mpz_t scalar) {
        Point temporary_result;
        mpz_inits(temporary_result.x, temporary_result.y, NULL);
        mpz_set_ui(temporary_result.x, 0);
        mpz_set_ui(temporary_result.y, 1);
        size_t iterator, scalar_binary_length = mpz_sizeinbase(scalar, 2);

        for (iterator = 0; iterator < scalar_binary_length; iterator++) {
            double_point(&temporary_result, &temporary_result);
            if (mpz_tstbit(scalar, scalar_binary_length - 1 - iterator)) {
                add_points( &temporary_result, &temporary_result, point);
            }
        }
        mpz_set(result->x, temporary_result.x);
        mpz_set(result->y, temporary_result.y);
        mpz_clears(temporary_result.x, temporary_result.y, NULL);
    }
};
