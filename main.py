from udp_receiver import UDPReceiver
from telemetry.telemetry_parser import TelemetryParser


def main():

    # UDP alıcısını başlat
    receiver = UDPReceiver(port=8000)
    parser = TelemetryParser()

    print("==========================================================================")
    print("                      FORZA HORIZON 6 TELEMETRY")
    print("==========================================================================")
    print("Çıkmak için CTRL + C\n")

    try:
        while True:
            # UDP paketini al ve çöz
            packet = receiver.receive()
            telemetry = parser.parse(packet)

            # Vites (0: Geri, 11: Boş)
            gear_str = "R" if telemetry.gear == 0 else ("N" if telemetry.gear == 11 else str(telemetry.gear))

            # Gaz ve Fren'i %0-100 aralığına çevir
            accel_pct = (telemetry.accel / 255.0) * 100 if telemetry.accel > 0 else 0
            brake_pct = (telemetry.brake / 255.0) * 100 if telemetry.brake > 0 else 0

            # Lastik sıcaklıklarını Fahrenheit'tan Celsius'a çevir
            # Formül: C = (F - 32) * 5/9
            fl_c = (telemetry.tireTempFL - 32) * 5 / 9
            fr_c = (telemetry.tireTempFR - 32) * 5 / 9
            rl_c = (telemetry.tireTempRL - 32) * 5 / 9
            rr_c = (telemetry.tireTempRR - 32) * 5 / 9

            # Ekran Çıktısı (Çok uzun olmaması için kompakt hale getirildi)
            print(
                f"\r"
                f"Vites:[{gear_str:^1}] | "
                f"Gaz:%{accel_pct:3.0f} | "
                f"Fren:%{brake_pct:3.0f} | "
                f"Hız:{telemetry.speed:4.0f}km/h | "
                f"Lastik(°C): ÖN({fl_c:3.0f} {fr_c:3.0f}) ARKA({rl_c:3.0f} {rr_c:3.0f})",
                end="",
                flush=True
            )

    except KeyboardInterrupt:
        print("\n\nProgram sonlandırıldı.")


if __name__ == "__main__":
    main()