import json

from .utils import is_json_serializable


def get_colab_content():
    from google.colab import _message
    import json
    notebook_dict = _message.blocking_request('get_ipynb', request='', timeout_sec=5000)
    return notebook_dict


def write_colab(cache):
    r  = {}
    for var in cache.vars:
        if var in globals():

            if cache.mode == "json":

                content = get_colab_content()

                if is_json_serializable(globals()[var]):
                    r[var] = globals()[var]
                else:
                    cache.failures.append(var)
                    if cache.log_failures:
                        r[var] = f"Variable {var} is not JSON serializable"

                content['metadata']['nbcache'] = r

                # send content variable to github gist 

                payload = {
                    "description": "nbcache gist for variables: " + ", ".join(r.keys()),
                    "public": False,  # still viewable by anyone with the URL, just not listed/searchable
                    "files": {
                        content['metadata']['colab']['name']: {
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
                        "raw_url": gist["files"][content['metadata']['colab']['name']]["raw_url"],
                        "html_url": gist["html_url"]
                    }
                )
            
            else:
                raise ValueError(f"Missing mode or mode {cache.mode} is not supported.")
            
        else:
            raise ValueError(f"Variable {var} is not defined in the global scope.")

            
