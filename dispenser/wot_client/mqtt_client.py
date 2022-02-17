from wot_client.settings_manager import global_settings
from wot_client.wifi_manager import get_device_id
from lib.umqtt.robust2 import MQTTClient

from machine import Timer


STATUS_DISCONNECTED = 0
STATUS_CONNECTED = 1


timer_id = global_settings.data['mqtt_timer_id']
mqtt_timer = Timer(timer_id)

client = None
expected_status = STATUS_DISCONNECTED

on_action_handler = None


def on_mqtt_message_handler(topic, msg, retained, duplicate):
    """Callback Handler for received messages over MQTT.

    Args:
        topic: Topic of the received message.
        msg: Actual received message.
    """
    global on_action_handler

    # decode topic and msg to strings
    topic = topic.decode('UTF-8')
    msg = msg.decode('UTF-8')

    print('New message on this topic "{}": {}'.format(topic, msg))

    # currently, only to actions topic is subscribed -> no check necessary before
    # calling the on_action_handler
    if on_action_handler is not None:
        try:
            on_action_handler(topic, msg)
        except Exception as e:
            print(f'Could not call on_action_handler! Exception: {e}')


def set_on_action_handler(handler):
    global on_action_handler
    on_action_handler = handler


def connect_to_broker():
    global client, mqtt_timer, expected_status

    broker_host = global_settings.data['hub_mqtt_broker']['host']
    broker_port = global_settings.data['hub_mqtt_broker']['port']
    mqtt_check_period = global_settings.data['mqtt_check_period']

    client = MQTTClient(get_device_id(), broker_host, broker_port)
    client.connect()
    client.set_callback(on_mqtt_message_handler)
    mqtt_timer.init(period=mqtt_check_period, mode=Timer.PERIODIC,
                    callback=lambda t: client.check_msg())
    expected_status = STATUS_CONNECTED

    # subscribe to required topics
    base_topic = global_settings.data['hub_mqtt_broker']['base_topic']
    device_id = get_device_id()
    actions_topic = f'{base_topic}/{device_id}/actions/#'
    client.subscribe(actions_topic)


def disconnect():
    global client, mqtt_timer, expected_status

    client.disconnect()
    mqtt_timer.deinit()
    expected_status = STATUS_DISCONNECTED


def publish(topic: str, message, add_device_id_topic=True, add_base_topic=True,
            retain=False):
    global client, mqtt_timer, expected_status

    if expected_status == STATUS_DISCONNECTED:
        print('WARNING! Cannot publish due to not being connected!')
        return

    base_topic = global_settings.data['hub_mqtt_broker']['base_topic']
    device_id = get_device_id()
    if add_device_id_topic:
        topic = '{}/{}'.format(device_id, topic)
    if add_base_topic and len(base_topic) > 0:
        topic = '{}/{}'.format(base_topic, topic)
    
    client.publish(topic, str(message), retain=retain)


def get_client():
    global client
    return client
