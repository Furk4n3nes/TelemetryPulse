from telemetry.telemetry_reader import TelemetryReader
from telemetry.telemetry_data import TelemetryData


class TelemetryParser:

    def parse(self, data: bytes) -> TelemetryData:

        r = TelemetryReader(data)
        t = TelemetryData()

        # ----------------------------
        # Race
        # ----------------------------

        t.isRaceOn = r.int32()
        t.timestamp = r.uint32()

        # ----------------------------
        # Engine
        # ----------------------------

        t.engineMaxRPM = r.float()
        t.engineIdleRPM = r.float()
        t.currentRPM = r.float()

        # ----------------------------
        # Acceleration
        # ----------------------------

        t.accelerationX = r.float()
        t.accelerationY = r.float()
        t.accelerationZ = r.float()

        # ----------------------------
        # Velocity
        # ----------------------------

        t.velocityX = r.float()
        t.velocityY = r.float()
        t.velocityZ = r.float()

        # Hız (m/s -> km/h)

        t.speed = (
            (
                t.velocityX ** 2 +
                t.velocityY ** 2 +
                t.velocityZ ** 2
            ) ** 0.5
        ) * 3.6

        # ----------------------------
        # Angular Velocity
        # ----------------------------

        t.angularVelocityX = r.float()
        t.angularVelocityY = r.float()
        t.angularVelocityZ = r.float()

        # ----------------------------
        # Orientation
        # ----------------------------

        t.yaw = r.float()
        t.pitch = r.float()
        t.roll = r.float()

        # ----------------------------
        # Suspension
        # ----------------------------

        t.suspensionFL = r.float()
        t.suspensionFR = r.float()
        t.suspensionRL = r.float()
        t.suspensionRR = r.float()

        if len(data) >= 320:
            r.offset = 315          # İşaretçiyi 315'e çekiyoruz
            t.accel = r.uint8()     # 315: Gaz (0-255)
            t.brake = r.uint8()     # 316: Fren (0-255)
            t.clutch = r.uint8()    # 317: Debriyaj (0-255)
            t.handBrake = r.uint8() # 318: El Freni (0-255)
            t.gear = r.uint8()      # 319: Vites

        if len(data) >= 320:
            # 1. Lastik Sıcaklıkları (268. byte'tan başlar - Her biri 4 byte Float)
            r.offset = 268
            t.tireTempFL = r.float()
            t.tireTempFR = r.float()
            t.tireTempRL = r.float()
            t.tireTempRR = r.float()

            # 2. Pedallar ve Vites (315. byte'tan başlar - Her biri 1 byte uint8)
            r.offset = 315
            t.accel = r.uint8()
            t.brake = r.uint8()
            t.clutch = r.uint8()
            t.handBrake = r.uint8()
            t.gear = r.uint8()    

    
        if len(data) >= 320:  
            r.offset = 319  # İşaretçiyi 319'a atlat
            t.gear = r.uint8()
        return t    
        

        # ------------------------------------------------
        # Şimdilik kalan alanları okumuyoruz.
        # Sonraki adımda devam edeceğiz.
        # ------------------------------------------------

        