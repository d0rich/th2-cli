yaml = '''
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: loki
  namespace: monitoring
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 5Gi
  storageClassName: local-storage
  selector:
    matchLabels:
      app: "loki"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: grafana
  namespace: monitoring
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 1Gi
  storageClassName: local-storage
  selector:
    matchLabels:
      app: "grafana"
'''
