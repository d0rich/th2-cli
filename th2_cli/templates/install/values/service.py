yaml = '''
infraMgr:
  git:
    repository: <repository>
    httpAuthUsername: <username>
    httpAuthPassword: <password>

infraOperator:
  config:
    k8sUrl: "<host>"
    
infraEditor:
  image:
    repository: ghcr.io/th2-net/th2-infra-editor
    tag: 1.0.65

ingress:
  host: &host <hostname>

dashboard:
  metrics-server:
    enabled: false
  ingress:
    paths:
      - /dashboard($|/.*)

rabbitmq:
  prometheus:
    operator:
      enabled: true
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
    datacenter: <cassandra-dc>
'''
