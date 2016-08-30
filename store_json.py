from collections import defaultdict
import json

accuracy = {'blue': 0.94, 'intermed': 0.74, 'brown': 0.95}

with open('/Users/apple/digital-phenotyping/self-report/eye_accuracy.json', 'w') as fp:
    json.dump(accuracy, fp, sort_keys=True, indent=4)