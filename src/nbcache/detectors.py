def detect_colab() -> bool:
    import sys
    return 'google.colab' in sys.modules

def detect_databricks() -> bool:
    import os
    return True if os.environ.get('DATABRICKS_RUNTIME_VERSION') else False


