import time

from wot_client.settings_manager import global_settings
import wot_client.mqtt_client as mqtt_client
import wot_client.wifi_manager as wifi_manager


MODE_OFFLINE = 0  # no connection
MODE_AP_ONLY = 1  # only access point acces
MODE_HUB_LOCAL = 2  # local access via hub
MODE_HUB_INTERNET = 3  # internet access via hub

# initially unkown
current_mode = -1


def set_access_mode(mode: int, save_mode: bool = True):
    """Connect/Disconnect WiFi networks according to the selected mode.

    This method relies on the correct hub wifi credentials being set in the
    global hub settings.
    
    Args:
        mode: The mode to set the device to.
        save_mode: Flag, whether to save the current mode to the global settings, or not.
    """
    global current_mode

    def announce_offline_if_was_connected_to_hub(old_mode: int, new_mode: int):
        if old_mode in [MODE_HUB_LOCAL, MODE_HUB_INTERNET]:
            announce_access_mode(new_mode)
            time.sleep(2)  # wait to ensure mqtt message can be send

    if mode == MODE_OFFLINE:
        announce_offline_if_was_connected_to_hub(current_mode, mode)
        wifi_manager.disable_ap_wifi()
        wifi_manager.disable_stationary_wifi()
    elif mode == MODE_AP_ONLY:
        announce_offline_if_was_connected_to_hub(current_mode, mode)
        wifi_manager.disable_stationary_wifi()
        wifi_manager.start_ap_wifi()
    elif mode == MODE_HUB_LOCAL:
        wifi_manager.disable_ap_wifi()
        # assuming the correct hub credentials are set in the global settings
        wifi_manager.connect_stationary_wifi()
        mqtt_client.connect_to_broker()
        announce_access_mode(mode)
    elif mode == MODE_HUB_INTERNET:
        wifi_manager.disable_ap_wifi()
        # assuming the correct hub credentials are set in the global settings
        wifi_manager.connect_stationary_wifi()
        mqtt_client.connect_to_broker()
        announce_access_mode(mode)
    else:
        raise Exception('Invalid access mode!')

    current_mode = mode
    if save_mode:
        global_settings.data['access_mode'] = mode
        global_settings.save()


def announce_access_mode(mode: int):
    if mode not in [MODE_OFFLINE, MODE_AP_ONLY, MODE_HUB_LOCAL, MODE_HUB_INTERNET]:
        raise Exception('Invalid mode!')

    mode_status_mapping = {
        MODE_OFFLINE: 'OFFLINE', MODE_AP_ONLY: 'OFFLINE', MODE_HUB_LOCAL: 'LOCAL',
        MODE_HUB_INTERNET: 'INTERNET'}
    status = mode_status_mapping[mode]

    mqtt_client.publish('properties/access_mode', status, retain=True)
