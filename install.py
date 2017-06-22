import pip
import importlib

def install(requirements="requirements.txt"):
    with open(requirements) as file:
        for line in file:
            module = line.strip()
            print("Setting up... Please wait...")
            for module in get_modules(requirements):
                try:
                    status = importlib.find_loader(module)
                except Exception:
                    status = importlib.util.find_spec(module)
                if status is not None:
                    print("%s module is already installed." % module)
                else:
                    print("%s module is being installed..." % module)
                    if pip.main(['install', module_name]) == 1:
                        print("Some error caused in installing %s module. "
                              "Kindly report back to the forum for further "
                              "information on how to fix the problem." % module)
                        break
                    else:
                        print("%s module was successfully installed." % module)

if __name__ == '__main__':
	install()
