import json

from .utils import is_json_serializable


def get_colab_content():
    from google.colab import _message
    import json
    notebook_dict = _message.blocking_request('get_ipynb', request='', timeout_sec=5000)
    return notebook_dict


def get_notebook_name():
    import os
    import requests
    import urllib.parse

    # Construct the local Jupyter API URL using environment variables
    jupyter_ip = os.environ.get("COLAB_JUPYTER_IP", "172.28.0.2")
    jupyter_port = os.environ.get("KMP_TARGET_PORT", "9000")
    session_url = f'http://{jupyter_ip}:{jupyter_port}/api/sessions'

    # Fetch the session data
    response = requests.get(session_url)
    session_data = response.json()

    # Extract and decode the notebook name
    notebook_name = session_data[0]['name']
    notebook_name = urllib.parse.unquote(notebook_name)

    return notebook_name



def write_colab(cache):
    from IPython import get_ipython
    notebook_globals = get_ipython().user_ns

    r  = {}
    for var in cache.vars:
        if var in notebook_globals:

            if cache.mode == "json":

                content = get_colab_content()

                if is_json_serializable(notebook_globals[var]):
                    r[var] = notebook_globals[var]
                else:
                    cache.failures.append(var)
                    if cache.log_failures:
                        r[var] = f"Variable {var} is not JSON serializable"

                try:
                    content['metadata']['nbcache'] = r
                except:
                    content['metadata'] = {}
                    content['metadata']['nbcache'] = r

                # send content variable to github gist 

                payload = {
                    "description": "nbcache gist for variables: " + ", ".join(r.keys()),
                    "public": False,  # still viewable by anyone with the URL, just not listed/searchable
                    "files": {
                        get_notebook_name(): {
                            "content": json.dumps(content, indent = 4)
                        }
                    }
                }

                import requests
                resp = requests.post("https://api.github.com/gists", json=payload)
                resp.raise_for_status()
                gist = resp.json()
                
                print(
                    {
                        "gist_id": gist["id"],
                        "raw_url": gist["files"][get_notebook_name()]["raw_url"],
                        "html_url": gist["html_url"]
                    }
                )
            
            else:
                raise ValueError(f"Missing mode or mode {cache.mode} is not supported.")
            
        else:
            raise ValueError(f"Variable {var} is not defined in the global scope.")

            
