import pprint

# Configure PrettyPrint
pp = pprint.PrettyPrinter(indent=4)

def object_print(pre, obj):
    print(f"{pre}:\n{pp.pformat(obj)}")

def op(pre, obj):
    object_print(pre, obj)