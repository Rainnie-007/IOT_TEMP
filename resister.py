import spidev
import time
import paho.mqtt.client as mqtt

# MQTT Settings
MQTT_BROKER = "mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_TOPIC = "test/resister"

# SPI setup for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel):
    adc = spi.xfer2([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    data = ((adc[1] & 15) << 8) + adc[2]
    return data

def publish_value(client):
    adc_value = read_adc(0)  # Reading from channel 0
    client.publish(MQTT_TOPIC, str(adc_value))
    print(f"Published: {adc_value}")
    time.sleep(1)

def main():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    try:
        while True:
            publish_value(client)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        client.loop_stop()
        spi.close()

if __name__ == "__main__":
    main()
