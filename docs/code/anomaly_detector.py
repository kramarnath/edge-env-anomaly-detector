import config

class StatisticalAnomalyDetector:
    def __init__(self):
        self.prev_temp = None
        self.prev_humi = None

    def evaluate(self, current_temp, current_humi):
        reasons = []
        is_anomaly = False

        # 1. Absolute Boundary Checks
        temp_out = current_temp < config.TEMP_MIN or current_temp > config.TEMP_MAX
        humi_out = current_humi < config.HUMI_MIN or current_humi > config.HUMI_MAX

        if temp_out:
            is_anomaly = True
            reasons.append("Temp Exceeded")

        if humi_out:
            is_anomaly = True
            reasons.append("Humi Exceeded")

        # 2. Rate of Change Checks (if previous reading exists)
        dt = 0.0
        dh = 0.0
        if self.prev_temp is not None and self.prev_humi is not None:
            dt = abs(current_temp - self.prev_temp)
            dh = abs(current_humi - self.prev_humi)

            if dt > config.MAX_TEMP_ROC:
                is_anomaly = True
                reasons.append("Temp Spike")

            if dh > config.MAX_HUMI_ROC:
                is_anomaly = True
                reasons.append("Humi Spike")

        # Update previous readings for next loop
        self.prev_temp = current_temp
        self.prev_humi = current_humi

        return {
            "status": "ANOMALY" if is_anomaly else "NORMAL",
            "reasons": reasons if is_anomaly else ["Normal"],
            "delta_temp": dt,
            "delta_humi": dh
        }