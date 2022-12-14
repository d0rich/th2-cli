yaml = '''
loki:
  # image:
  #   pullPolicy: IfNotPresent
  #   repository: grafana/loki
  #   pullSecrets:
  persistence:
    enabled: true
    existingClaim: loki
  config:
    table_manager:
      retention_deletes_enabled: true
      retention_period: 168h
    chunk_store_config:
      max_look_back_period: 168h

promtail:
#   image:
#     pullPolicy: IfNotPresent
#     repository: grafana/promtail
#     pullSecrets:
  resources:
    limits:
      cpu: 500m
      memory: 400Mi
    requests:
      cpu: 200m
      memory: 200Mi
'''
