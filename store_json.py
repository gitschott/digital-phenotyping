from collections import defaultdict
import json

constants_for_the_shape = ['3.84', '0.37']

with open('/Users/apple/digital-phenotyping/self-report/alpha_eye_irisplex.json', 'w') as fp:
    json.dump(constants_for_the_shape, fp, sort_keys=True, indent=4)