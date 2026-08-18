from flask import Flask, render_template, jsonify
import threading

from udp_receiver import UDPReceiver
from telemetry.telemetry_parser import TelemetryParser

app = Flask(__name__)

# Global telemetri verisi
latest_telemetry = {
    "gear": "N",
    "accel": 0,
    "brake": 0,
    "speed": 0,
    "rpm": 0,
    "max_rpm": 0,
    "fl": 0, "fr": 0, "rl": 0, "rr": 0
}

def telemetry_background_worker():
    """Arka planda sürekli Forza'dan UDP verisi dinleyen iş parçacığı"""
    global latest_telemetry
    receiver = UDPReceiver(port=8000)
    parser = TelemetryParser()

    print("UDP Telemetri Dinleyicisi Arka Planda Başlatıldı...")

    while True:
        try:
            packet = receiver.receive()
            t = parser.parse(packet)

            # Vites formatı
            gear_str = "R" if t.gear == 0 else ("N" if t.gear == 11 else str(t.gear))

            # Yüzde ve Derece hesaplamaları
            accel_pct = int((t.accel / 255.0) * 100) if t.accel > 0 else 0
            brake_pct = int((t.brake / 255.0) * 100) if t.brake > 0 else 0
            
            fl_c = int((t.tireTempFL - 32) * 5 / 9)
            fr_c = int((t.tireTempFR - 32) * 5 / 9)
            rl_c = int((t.tireTempRL - 32) * 5 / 9)
            rr_c = int((t.tireTempRR - 32) * 5 / 9)

            # Sözlüğü güncelle
            latest_telemetry = {
                "gear": gear_str,
                "accel": accel_pct,
                "brake": brake_pct,
                "speed": int(t.speed),
                "rpm": int(t.currentRPM),
                "max_rpm": int(t.engineMaxRPM),
                "fl": fl_c, "fr": fr_c, "rl": rl_c, "rr": rr_c
            }
        except Exception:
            pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    """Web sayfasının saniyede birkaç kez güncel veriyi isteyeceği adres"""
    return jsonify(latest_telemetry)

if __name__ == '__main__':
    # Arka plan dinleyicisini thread olarak başlat
    t = threading.Thread(target=telemetry_background_worker, daemon=True)
    t.start()

    # Flask sunucusunu başlat
    print("Web Paneli Çalıştırılıyor: http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)