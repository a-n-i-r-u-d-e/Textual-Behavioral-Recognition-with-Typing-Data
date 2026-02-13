def ensemble_predict(rf_pred, gru_pred):
    # Hard override for idle
    if rf_pred == "idle":
        return "idle"

    if gru_pred and gru_pred != "idle":
        return gru_pred

    return rf_pred
