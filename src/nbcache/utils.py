def is_json_serializable(obj):
    import json
    try:
        json.dumps(obj)
        return True
    except:
        return False