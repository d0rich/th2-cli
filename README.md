Works with th2 1.5.4

## Using

Install:

```commandline
pip install th2-cli
```

### Install th2

If you already have configurations in `th2-cli-install-config.yaml` or `secrets.yaml`, it will be convenient to run process from the directory with these files.
In other case CLI will create these config files during installation.

```commandline
th2 install
```

### Delete th2

```commandline
th2 delete
```

### Update th2

```commandline
th2 delete
```

Wait until all required namespaces are terminated.

```commandline
th2 install
```

## Configurations templates

### th2-cli-install-config.yaml

```yaml
cassandra:
  datacenter: datacenter1
  host: host.minikube.internal
infra-mgr:
  git:
    http-auth-password: pat_token
    http-auth-username: pat_token
    repository: https://github.com/schema/repository
kubernetes:
  host: 192.168.49.2
  pvs-node: minikube
```

### secrets.yaml

```yaml
# required only for images from a private registry, will be attached as the first PullSecret to deployments
#productRegistry:
#  username: user
#  password: password
#  name: private-registry-1.example.com # core components registry

# required only for images from a private registry, will be attached as the second PullSecret to deployments
#solutionRegistry:
#  username: user
#  password: password
#  name: private-registry-2.example.com # components registry

# required only for images from a private registry, will be attached as the third PullSecret to deployments
#proprietaryRegistry:
#  username: user
#  password: password
#  name: private-registry-3.example.com # components registry

cassandra:
# set credentials for the existing Cassandra cluster
  dbUser:
    user: cassandra
    password: cassandra

rabbitmq:
# set admin user credentials, it will be created during deployment
  rabbitmqUsername: th2
  rabbitmqPassword: rab-pass
  # must be random string
  rabbitmqErlangCookie: cookie
```

## Development

```
poetry install
poetry shell
```

```commandline
th2 install
```