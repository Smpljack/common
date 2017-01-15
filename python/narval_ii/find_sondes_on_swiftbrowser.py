import sys
import yaml
from narval_ii.data import mk_narval_ii_swift_browser_accessor

def _main():
    import requests_cache
    requests_cache.install_cache("test_cache")
    
    sba = mk_narval_ii_swift_browser_accessor()
    sondes = [filename[-1][:-7]
              for filename in sba.walk_files(["HALO_data"])
              if "Dropsondes_ASPEN" in filename]
    yaml.dump(list(sorted(sondes)), sys.stdout, default_flow_style=False)

if __name__ == '__main__':
    _main()
