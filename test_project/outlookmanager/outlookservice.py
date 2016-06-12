import json
import requests
import uuid

outlook_api_endpoint = 'https://outlook.office.com/api/beta'


def make_api_call(method, url, token, user_email, payload=None, parameters=None):
    headers = {
        'User-Agent': 'outlookmanager/beta',
        'Authorization': 'Bearer %s' % token,
        'Accept': 'application/json',
        'X-AnchorMailbox': user_email,
    }

    request_id = str(uuid.uuid4())
    instrumentation = {
        'client-request-id': request_id,
        'return-client-request-id': 'true',
    }

    headers.update(instrumentation)

    response = None

    import logging
    logging.warning(headers)
    logging.warning(method.upper() == 'GET')
    logging.warning(url)
    if method.upper() == 'GET':
        response = requests.get(url, headers=headers, params=parameters)
    elif method.upper() == 'DELETE':
        response = requests.delete(url, headers=headers, params=parameters)
    elif method.upper() == 'PATCH':
        response = requests.patch(url, headers=headers, params=parameters)
    elif method.upper() == 'POST':
        headers.update({
            'Content-Type': 'application/json',
        })
        response = requests.post(url, headers=headers, data=json.dumps(payload), params=parameters)
    logging.warning(response)
    return response


def get_my_messages(access_token, user_email):
    get_messages_url = outlook_api_endpoint + '/me/messages'
    import logging
    logging.warning(get_messages_url)
    query_parameters = {
        '$top': '10',
        '$select': 'ReceivedDateTime,Subject,From',
        '$orderby': 'ReceivedDateTime DESC',
    }

    r = make_api_call('GET', get_messages_url, access_token, user_email, parameters=query_parameters)
    logging.warning(r)
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return '%s: %s' % (r.status_code, r.text)
