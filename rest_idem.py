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
        print "POST", json.dumps(payload)

    def delete(self, payload):
        print "DELETE", json.dumps(payload)


class IdempotentRest:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    @staticmethod
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

        for key in current:
            if key not in desired:
                extra[key] = current[key]

        return missing, extra

    def match(self, desired_state):
        current_state = self.endpoint.get()

        return self.diff_state(current=current_state, desired=desired_state)

    def delete(self, values):
        for key in values:
            self.endpoint.delete({key: values[key]})

    def post(self, values):
        for key in values:
            self.endpoint.post({key: values[key]})

    def update(self, desired_state):
        missing, extra = self.match(desired_state)

        self.delete(extra)
        self.post(missing)

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
    endpoint = Endpoint(url=endpoint_url)

    payload_file = params['payload_file']
    try:
        with open(payload_file) as f:
            desired_state = json.load(f)
    except IOError:
        e = get_exception()
        module.fail_json(msg="Reading payload from file failed: %s" % str(e))

    idempotent_endpoint = IdempotentRest(endpoint)

    try:
        missing, extra = idempotent_endpoint.update(desired_state)
    except Exception:
        e = get_exception()
        module.fail_json(msg="Error while processing keys: %s" % str(e))

    module.exit_json(changed=True, missing=missing, extra=extra)


if __name__ == '__main__':
    main()
