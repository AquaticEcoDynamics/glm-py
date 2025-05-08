def sensitivity_index(out_new, out_original, param_new, param_original):
    si = ((out_new - out_original) / out_original) / (
        (param_new - param_original) / param_original
    )
    return si
