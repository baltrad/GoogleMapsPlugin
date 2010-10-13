import xmlrpclib
import sys

if __name__=="__main__":
  if len(sys.argv) != 4:
    print "Usage %s <uri> <infile> <outfile>"%(sys.argv[0])
    sys.exit(0)

  uri = sys.argv[1]
  filename = sys.argv[2]
  outfile = sys.argv[3]
  server = xmlrpclib.ServerProxy(uri)
  
  server.generate("se.smhi.rave.creategmapimage", [filename], ["outfile",outfile])

