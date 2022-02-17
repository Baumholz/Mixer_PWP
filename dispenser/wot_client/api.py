import wot_client.access_mode as access_mode
import wot_client.mqtt_client as mqtt_client
import wot_client.wifi_manager as wifi_manager

from wot_client.settings_manager import global_settings


MODE_OFFLINE = access_mode.MODE_OFFLINE  # no connection
MODE_AP_ONLY = access_mode.MODE_AP_ONLY  # only access point acces
MODE_HUB_LOCAL = access_mode.MODE_HUB_LOCAL  # local access via hub
MODE_HUB_INTERNET = access_mode.MODE_HUB_INTERNET  # internet access via hub


def init():
    """Restore previously used access mode."""
    previous_access_mode = global_settings.data['access_mode']
    access_mode.set_access_mode(previous_access_mode)
    print('Activated access mode: {}'.format(previous_access_mode))


def publish_event(event_name: str, payload):
    """
    Publish a new event (on the MQTT Broker)

    Args:
        event_name: The name of the event which is used for creating the topic.
        payload: Payload to publish for the event.
    """
    topic = f'events/{event_name}'
    mqtt_client.publish(topic, payload)


def publish_property_value(property_name: str, payload):
    """
    Publish a new/updated property value (on the MQTT Broker)

    Args:
        property_name: The name of the property which is used for creating the topic.
        payload: Payload, i.e. the new value, of the property
    """
    topic = f'properties/{property_name}'
    mqtt_client.publish(topic, payload, retain=True)


def get_device_id():
    """Get the unique device ID."""
    return wifi_manager.get_device_id()


def set_on_action_handler(on_action_handler):
    """Set the handler that is called by the libary when a new (requested) action is received."""
    mqtt_client.set_on_action_handler(on_action_handler)


def set_access_mode(mode: int):
    """
    Set the access mode of the device.
    
    Use the available constants from this file:
      - MODE_OFFLINE
      - MODE_AP_ONLY
      - MODE_HUB_LOCAL
      - MODE_HUB_INTERNET
    """
    access_mode.set_access_mode(mode)


def get_global_settings():
    """Get the global settings manager instance."""
    return global_settings
