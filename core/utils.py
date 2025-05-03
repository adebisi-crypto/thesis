# QRISK3_COEFFICIENTS = {
#     'intercept': -29.799,  # baseline intercept
#     'age': 0.04823,
#     'sex_female': -0.213,  # 1 if female, 0 if male
#     'smoker': 0.855,       # 1 if current smoker
#     'diabetes': 0.799,
#     'systolic_bp': 0.0184,
#     'chol_hdl_ratio': 0.180,
#     'bmi': 0.0715,
#
#     # Example ethnicity coefficients (choose one)
#     'ethnicity': {
#         'white': 0,
#         'black_african': 0.290,
#         'black_caribbean': 0.285,
#         'indian': 0.127,
#         'pakistani': 0.246,
#         'bangladeshi': 0.255,
#         'other': 0.150
#     }
# }
#
# def calculate_qrisk3_score(age, sex, smoker, diabetes, systolic_bp, chol_hdl_ratio, bmi, ethnicity):
#     coeffs = QRISK3_COEFFICIENTS
#     sex_female = 1 if sex.lower() == 'female' else 0
#     smoker_val = 1 if smoker else 0
#     diabetes_val = 1 if diabetes else 0
#     ethnicity_coeff = coeffs['ethnicity'].get(ethnicity.lower(), 0)
#
#     score = (
#         coeffs['intercept']
#         + coeffs['age'] * age
#         + coeffs['sex_female'] * sex_female
#         + coeffs['smoker'] * smoker_val
#         + coeffs['diabetes'] * diabetes_val
#         + coeffs['systolic_bp'] * systolic_bp
#         + coeffs['chol_hdl_ratio'] * chol_hdl_ratio
#         + coeffs['bmi'] * bmi
#         + ethnicity_coeff
#     )
#
#     # Normalize to 0–100 range using sigmoid approximation
#     import math
#     probability = 1 / (1 + math.exp(-score)) * 100
#     return round(probability, 2)
#


def calculate_qrisk3_score(age, sex, smoker, diabetes, systolic_bp, chol_hdl_ratio, bmi, ethnicity):
    # Weights loosely based on relative clinical importance
    weights = {
        'age': 0.25,
        'sex_female': -3,  # Males generally at higher risk
        'smoker': 8,
        'diabetes': 8,
        'systolic_bp': 0.1,
        'chol_hdl_ratio': 1.5,
        'bmi': 0.3,
        'ethnicity': {
            'white': 0,
            'black_african': 3,
            'black_caribbean': 2.8,
            'indian': 1.5,
            'pakistani': 2,
            'bangladeshi': 2.2,
            'other': 1
        }
    }

    sex_female = 1 if sex.lower() == 'female' else 0
    smoker_val = 1 if smoker else 0
    diabetes_val = 1 if diabetes else 0
    ethnicity_score = weights['ethnicity'].get(ethnicity.lower(), 0)

    score = (
        weights['age'] * age +
        weights['sex_female'] * sex_female +
        weights['smoker'] * smoker_val +
        weights['diabetes'] * diabetes_val +
        weights['systolic_bp'] * systolic_bp +
        weights['chol_hdl_ratio'] * chol_hdl_ratio +
        weights['bmi'] * bmi +
        ethnicity_score
    )

    # Clamp to a realistic range
    score = max(0, min(score / 2, 100))
    return round(score, 2)
