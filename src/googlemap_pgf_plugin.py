'''
Created on Oct 6, 2010

@author: anders
'''
import GmapCreator

def generate(files, arguments):
  creator = GmapCreator.GmapCreator(files[0])
  img = creator.create_image()
  l = len(arguments)
  filename=None
  for i in range(l):
    if arguments[i] == "outfile":
      filename = arguments[i+1]
      break
  
  img.save(filename, transparency=0)
  return None

if __name__ == '__main__':
    pass