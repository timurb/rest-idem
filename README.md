# Testing the module

The module is work in progress.
At the moment testing can be done by doing the following:
1. Put JSON to `test.json` for desired state.
2. Update JSON in `rest_idem.py` (method `Endpoint.get`) for the current state.
3. Run the module using stock ansible `test-module` tool (see details below).
4. Watch the diff in the output.

TODOs:
* Write unit tests for the module (no idea how to do that)
* Confirm that the behaviour is desired and add the real REST requests for HTTP endpoint


### Doing the test run

Git clone ansible in standalone dir -- it is required for development.

```
$ . ../ansible/hacking/env-setup # preparation step
.....output skipped.....
$ ../ansible/hacking/test-module -m rest_idem.py -a 'endpoint=www.google.com payload_file=test.json'
* including generated source, if any, saving to: /Users/timurb/.ansible_module_generated
* ansiballz module detected; extracted module source to: /Users/timurb/debug_dir
***********************************
RAW OUTPUT
DELETE {"baz": "qux1"}
POST {"baz": "qux"}
POST {"bah": "boom"}

{"invocation": {"module_args": {"payload_file": "test.json", "endpoint": "www.google.com"}}, "changed": true, "missing": {"baz": "qux", "bah": "boom"}, "extra": {"baz": "qux1"}}


***********************************
INVALID OUTPUT FORMAT
DELETE {"baz": "qux1"}
POST {"baz": "qux"}
POST {"bah": "boom"}

{"invocation": {"module_args": {"payload_file": "test.json", "endpoint": "www.google.com"}}, "changed": true, "missing": {"baz": "qux", "bah": "boom"}, "extra": {"baz": "qux1"}}

Traceback (most recent call last):
  File "../ansible/hacking/test-module", line 218, in runtest
    results = json.loads(out)
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/__init__.py", line 338, in loads
    return _default_decoder.decode(s)
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/decoder.py", line 366, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/decoder.py", line 384, in raw_decode
    raise ValueError("No JSON object could be decoded")
ValueError: No JSON object could be decoded
```

The error is ok at the current moment. Watch the delete/post lines instead.
