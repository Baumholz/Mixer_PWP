import json

import wot_client.wifi_manager as wifi_manager

from wot_client.settings_manager import global_settings


td_path = None
td_parsed = {}
td_dumped = ''


def set_td_path(new_td_path: str):
    global td_path
    td_path = new_td_path


def parse_and_prepare_thing_description():
    global td_dumped, td_parsed, td_path

    assert td_path is not None, 'No TD-Path set!'

    file = open(td_path)
    td_data = json.load(file)

    # variables for the td
    device_id = wifi_manager.get_device_id()
    broker_host = global_settings.data['hub_mqtt_broker']['host']
    broker_port = global_settings.data['hub_mqtt_broker']['port']
    base_topic = global_settings.data['hub_mqtt_broker']['base_topic']
    mqtt_server_path = f'mqtt://{broker_host}:{broker_port}/{base_topic}/{device_id}'

    # set id
    td_data['id'] = f'pwp:{device_id}'

    # ensure access_mode property is defined
    td_data['properties']['access_mode'] = {
        '@type': 'pwpref:AccessState',
        'type': 'String',
        'observable': True,
    }

    # property forms
    if td_data['properties']:
        for (p_name, p_data) in td_data['properties'].items():
            td_data['properties'][p_name]['forms'] = [{
                'href': f'{mqtt_server_path}/properties/{p_name}',
                'op': 'observeProperty',
                'mqv:controlPacketValue': 'SUBSCRIBE',
            }]

    # action forms
    if td_data['actions']:
        for (a_name, a_data) in td_data['actions'].items():
            td_data['actions'][a_name]['forms'] = [{
                'href': f'{mqtt_server_path}/actions/{a_name}',
                'op': 'invokeaction',
                'mqv:controlPacketValue': 'PUBLISH',
            }]

    # event forms
    if td_data['events']:
        for (e_name, e_data) in td_data['events'].items():
            td_data['events'][e_name]['forms'] = [{
                'href': f'{mqtt_server_path}/events/{e_name}',
                'op': 'subscribeevent',
                'mqv:controlPacketValue': 'SUBSCRIBE',
            }]
    
    td_parsed = td_data
    td_dumped = json.dumps(td_parsed)


def get_thing_description() -> dict:
    global td_parsed
    return td_parsed


def get_thing_description_str() -> str:
    global td_dumped
    return td_dumped
