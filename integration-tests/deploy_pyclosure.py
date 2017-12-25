

from clipper_admin import ClipperConnection, DockerContainerManager
from clipper_admin.deployers import gRPCpython as python_deployer

args = {"ports" : {"7000/tcp": 7000}}

clipper_conn = ClipperConnection(DockerContainerManager(
extra_container_kwargs = args
))



def feature_sum(xs):
    return [str(sum(xs))]



python_deployer.deploy_python_closure(clipper_conn, name="sum-model", version=1, input_type="ints", func=feature_sum)