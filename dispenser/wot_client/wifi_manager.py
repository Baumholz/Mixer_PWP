from wot_client.settings_manager import global_settings

import network
import time
import ubinascii


# Network Interfaces
WIFI_STA = network.WLAN(network.STA_IF)
WIFI_AP = network.WLAN(network.AP_IF)


def get_device_id():
    #"""Get the unique ID of the device (MAC Address)"""
    #mac_address = ubinascii.hexlify(WIFI_STA.config('mac'),':').decode()
    #return mac_address.replace(':', '_')
    
    device_id = global_settings.data['hub_mqtt_broker']['device_id']
    print(device_id)
    return device_id


def connect_stationary_wifi(ssid=None, password=None) -> bool:
    """
    Try to connect to the given ssid with given password via the given network connection.
    If no ssid or password are given, the "hub settings" from the global settings are used.

    Args:
        ssid: SSID/Name of the network to connect to.
        password: Password for the WiFi network.

    Returns:
        connected: True, if connection could be established, False otherwise.
    """

    ssid = ssid if ssid else global_settings.data['hub_wifi']['ssid']
    password = password if password else global_settings.data['hub_wifi']['password']

    WIFI_STA.active(True)
    if WIFI_STA.isconnected():
        print('Already connected!')
        return True
    print('Trying to connect to "{}"...'.format(ssid))
    WIFI_STA.connect(ssid, password)
    for _ in range(300):
        connected = WIFI_STA.isconnected()
        if connected:
            break
        time.sleep(0.5)
        print('.', end='')
    if connected:
        print('\nConnected. Network config: ', WIFI_STA.ifconfig())
    else:
        print('\nFailed. Not Connected to: ' + ssid)
    return connected


def stationary_ifconfig():
    if not WIFI_STA.isconnected():
        return None
    ip, netmask, gateway, dns_server = WIFI_STA.ifconfig
    return {'ip': ip, 'netmask': netmask, 'gateway': gateway, 'dns_server': dns_server}


def disable_stationary_wifi():
    WIFI_STA.active(False)


def start_ap_wifi():
    """Start the "Access Point" mode/WiFi of the device."""
    ap_ssid = global_settings.data['ap_wifi']['ssid'] + '_' + get_device_id()
    ap_password = global_settings.data['ap_wifi']['password']
    ap_authmode = global_settings.data['ap_wifi']['authmode']

    WIFI_AP.active(True)
    WIFI_AP.config(essid=ap_ssid, password=ap_password, authmode=ap_authmode)
    print('Connect to WiFi "{}", password: "{}"'.format(ap_ssid, ap_password))
    print('and access the ESP via 192.168.4.1.')


def disable_ap_wifi():
    WIFI_AP.active(False)
