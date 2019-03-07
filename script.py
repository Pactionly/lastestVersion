import xmltodict
import urllib2
import os


NEXUS_URL = "http://192.168.0.46:8081/repository/maven-snapshots/"

POM_GROUPID = os.environ['POM_GROUPID']
POM_ARTIFACTID = os.environ['POM_ARTIFACTID']
POM_VERSION = os.environ['POM_VERSION'] if 'POM_VERSION' in os.environ else ""

# Returns a string denoting the newest snapshot version stored in Nexus
def newestVersion():
  url = NEXUS_URL
  url += POM_GROUPID.replace('.','/')
  url += '/' + POM_ARTIFACTID
  url += '/maven-metadata.xml'

  file = urllib2.urlopen(url)
  data = xmltodict.parse(file.read())
  file.close()

  newest = [0,0,0]
  newestString = ""
  for i in data['metadata']['versioning']['versions']['version']:
    sem = i[:-9].split('.')
    for j in sem:
      j = int(j)
    for j in range(3):
      if sem[j] > newest[j]:
        newest = sem
        newestString = i
        break
      if sem[j] < newest[j]:
        break
  return newestString

if(POM_VERSION == ""):
  POM_VERSION = newestVersion()

print "Deploying version %s to Tomcat" % POM_VERSION

url = NEXUS_URL 
url += POM_GROUPID.replace('.','/')
url += '/' + POM_ARTIFACTID
url += '/' + POM_VERSION
meta = url + '/maven-metadata.xml'

file = urllib2.urlopen(meta)
data = xmltodict.parse(file.read())
file.close()

for i in data['metadata']['versioning']['snapshotVersions']['snapshotVersion']:
  if i['extension'] == 'war':
    value =  i['value']
    break

url += '/' + POM_ARTIFACTID + '-' + value +'.war'

print "Deploying from %s to Tomcat" % url

scriptText = "curl -o /usr/share/tomcat/webapps/" + POM_ARTIFACTID + ".war " + url
file = open('tomcat.sh', 'w')
file.write(scriptText)
file.close()
