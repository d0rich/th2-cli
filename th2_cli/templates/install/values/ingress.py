yaml = '''
imagePullSecrets:
controller:
  service:
    type: NodePort
    nodePorts:
      http: 30000
  # image:
  #   repository: k8s.gcr.io/ingress-nginx/controller
  #   tag: "v0.41.2"
  admissionWebhooks:
    enabled: false
# defaultBackend:
#   image:
#     repository: defaultbackend-amd64
#     tag: "1.5"
'''