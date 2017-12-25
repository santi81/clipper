import grpc_server
import json

class GrpcTestContainer(grpc_server.ModelContainerBase):
    def __init__(self, grpc_service):
        self.grpc_service = grpc_service

    def predict_doubles(self, inputs):
        outputs = []
        for input_item in inputs:
            outputs.append(input_item)
        return outputs

if __name__ == "__main__":
    port = 7000
    model_name = "rpctest_py"
    input_type = "doubles"
    model_version = 1

    rpc_service = grpc_server.GrpcServer()
    model = GrpcTestContainer(rpc_service)
    rpc_service.start(model, port, model_name, model_version, input_type)
