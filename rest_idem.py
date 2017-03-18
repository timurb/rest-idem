#!/usr/bin/python

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pycompat24 import get_exception


class Endpoint:
    def __init__(self, url):
        self.url = url

    def get(self):
        return {'foo': 'bar',
                'baz': 'qux1',
                'hey': 'yo'}

    def post(self, payload):
        print "post", payload

    def delete(self, payload):
        print "delete", payload


def diff_state(current, desired):
    missing = {}
    extra = {}

    for key in desired:
        if key in current:
            if current[key] != desired[key]:
                missing[key] = desired[key]
                extra[key] = current[key]
        else:
            missing[key] = desired[key]

    return missing, extra


def main():
    module = AnsibleModule(
        argument_spec=dict(
            endpoint=dict(required=True),
            payload_file=dict(required=True)
        )
    )

    params = module.params

    endpoint_url = params['endpoint']
    payload_file = params['payload_file']

    try:
        with open(payload_file) as f:
            desired_state = json.load(f)
    except IOError:
        e = get_exception()
        module.fail_json(msg="Reading payload from file failed: %s" % str(e))

    endpoint = Endpoint(url=endpoint_url)
    current_state = endpoint.get()

    missing, extra = diff_state(current=current_state, desired=desired_state)

    try:
        for key in extra:
            endpoint.delete({key: extra[key]})
    except Exception:
        e = get_exception()
        module.fail_json(msg="Error happened while deleting keys: %s" % str(e))

    try:
        for key in missing:
            endpoint.post({key: missing[key]})
    except Exception:
        e = get_exception()
        module.fail_json(msg="Error happened while creating keys: %s" % str(e))

    module.exit_json(changed=True, missing=missing, extra=extra)


if __name__ == '__main__':
    main()
