import os
import sys
import configparser
import subprocess
import logging

config = configparser.ConfigParser() 
try:
    basename = os.path.splitext(os.path.split(sys.argv[0])[1])[0] # Path to working folder
    config.read(basename+'.ini') # Path to config
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S', filename=basename+'.log', level=logging.DEBUG)
    # Read configs
    paths = config["default"]["walk"].split(";") # Paths for walk
    filetypes = config["default"]["filetypes"].lower().split(";")
    filetypes=["."+filetype for filetype in filetypes]
    outtype= config["default"]["outtype"].lower()
    handbrake = config["handbrake"]["path"]
    options = config["handbrake"]["options"]
    removeOriginal=int(config["default"]["remove_original"])
    for path in paths: # for all files in all selected folders
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1].lower() in filetypes:
                    inPath=os.path.join(root, file) # path of input file
                    outPath=os.path.join(root, ".".join((os.path.splitext(file)[0],outtype))) # path of encoded file
                    print(' '.join([handbrake, " ".join(("-i",'"'+inPath+'"',"-o",'"'+outPath+'"',options))]))
                    if subprocess.call(" ".join(('"'+handbrake+'"',"-i",'"'+inPath+'"',"-o",'"'+outPath+'"',options))) == 0: # call of HandBrake
                        logging.info(" ".join((inPath,"successfully converted to",outPath)))
                        print(" ".join((inPath,"successfully converted to",outPath)))
                        if removeOriginal and os.path.isfile(outPath):
                            os.remove(inPath) # delete if necessary
                            logging.info("%s deleted",inPath)
                            print(inPath, "deleted")
                    else:
                        logging.warning(" ".join("Problems during convertion",inPath))
                        print("Problems during convertion",inPath)

except KeyError as err:
    print("Couldn't find option ", err)
    logging.debug("Couldn't find option: "+str(err))
except EnvironmentError as err:
    print(err)
    logging.debug("Environment error: "+str(err))
finally:
    logging.shutdown() 
