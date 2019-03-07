import urllib2
import os

url = "http://192.168.0.46:8081/repository/maven-snapshots/"
url += os.environ['POM_GROUPID'].replace('.','/')
url += '/' + os.environ['POM_ARTIFACTID']
url += '/' + os.environ['POM_VERSION']
url += '/' + 'maven-metadata.xml'

print url

# http://192.168.0.46:8081/repository/maven-snapshots/org/springframework/samples/spring-petclinic/1.0.0-SNAPSHOT/maven-metadata.xml
