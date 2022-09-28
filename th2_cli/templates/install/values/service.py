yaml = '''
infraMgr:
  git:
    repository: <repository>
    httpAuthUsername: <username>
    httpAuthPassword: <password>

infraOperator:
  config:
    k8sUrl: "<host>"

rabbitmq:
  prometheus:
    operator:
      enabled: false
  persistentVolume:
    enabled: true
    storageClass: local-storage
    size: 10Gi
  ingress:
    enabled: true
    hostName: <hostname>

cassandra:
  internal: false
  host: <cassandra-host>
  cluster:
    datacenter: <datacenter>
'''
