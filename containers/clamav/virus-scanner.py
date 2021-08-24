import boto3
import os
import sys
import subprocess
import uuid
import json
#from urllib.parse import unquote_plus

from six.moves.urllib.parse import urlparse

s3_client = boto3.client('s3')

def task_handler():
      
      bucket = os.environ.get('BUCKET')
      key = os.environ.get('KEY')  
      print("S3 bucket from where File needs to be scanned---"+bucket)
      print("Filename in S3 to be scanned --- "+key)
      file_name = '/tmp/' + key.split('/')[-1]

      print("downloading from S3 Bucket....")
      s3_client.download_file(bucket, key, file_name)

#      freshscan_cmd = 'freshclam'
#      print("running freshclam command --" + freshscan_cmd)
#      sp1 = subprocess.Popen(freshscan_cmd,
#                            shell=True,
#                            stdout=subprocess.PIPE,
#                            stderr=subprocess.PIPE,
#                            universal_newlines=True)

#      out, err = sp1.communicate()
#      return_code1 = sp1.wait()
#      print("freshclam command ran ---" + str(return_code1))

      scan_cmd = 'clamscan --quiet ' + file_name
      print("running clamscan command --" + scan_cmd)
      sp = subprocess.Popen(scan_cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

      out, err = sp.communicate()

        # * clamscan return values (documented from man clamscan)
        # *  0 : No virus found.
        # *  1 : Virus(es) found.
        # * 40: Unknown option passed.
        # * 50: Database initialization error.
        # * 52: Not supported file type.
        # * 53: Can't open directory.
        # * 54: Can't open file. (ofm)
        # * 55: Error reading file. (ofm)
        # * 56: Can't stat input file / directory.
        # * 57: Can't get absolute path name of current working directory.
        # * 58: I/O error, please check your file system.
        # * 62: Can't initialize logger.
        # * 63: Can't create temporary files/directories (check permissions).
        # * 64: Can't write to temporary directory (please specify another one).
        # * 70: Can't allocate memory (calloc).
        # * 71: Can't allocate memory (malloc).

      return_code = sp.wait()
      print("clamscan command ran ---" + str(return_code))
      if return_code == 0:
          print("Clean File. Tagging as clean...!")
          tag_response = s3_client.put_object_tagging(
                  Bucket=bucket,
                  Key=key,
                  # versionId=version,
                  Tagging={'TagSet': [
                      {
                          'Key': 'clamscan-status',
                          'Value': 'CLEAN'
                      },
                  ]})

          print("Attempted tagging the tainted object. Result: " + str(tag_response))
      else:
          print("Return Code: " + str(return_code))
          print("Standard out: \n", out)

          preferredAction = os.environ.get('preferredAction')
          if preferredAction == "Delete":
              delete_response = s3_client.delete_object(Bucket=bucket,
                                      Key=key,
                                      # VersionId=version
                                      )
              print("Attempted deleting the tainted object. Result: " + str(delete_response))
          else:
              tag_response = s3_client.put_object_tagging(
                  Bucket=bucket,
                  Key=key,
                  # versionId=version,
                  Tagging={'TagSet': [
                      {
                          'Key': 'clamscan-status',
                          'Value': 'VIRUS FOUND'
                      },
                  ]})

              print("Attempted tagging the tainted object. Result: " + str(tag_response))

if __name__ == '__main__':
    bucket = os.environ.get('BUCKET')
    key = os.environ.get('KEY')
    task_handler()
