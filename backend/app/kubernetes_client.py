from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException


def load_kubernetes_config() -> None:
    try:
        config.load_incluster_config()
    except ConfigException:
        config.load_kube_config()


load_kubernetes_config()

core_v1 = client.CoreV1Api()

