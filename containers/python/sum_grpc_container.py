from __future__ import print_function
import grpc_server
import os
import sys

class SumContainer(grpc_server.ModelContainerBase):
    def __init__(self):
        pass

    def predict_ints(self, inputs):
        sum = 0
        for item in inputs:
            sum += item
        return [sum]

    def predict_floats(self, inputs):
        sum = 0.0
        for item in inputs:
            sum += item
        return [sum]

    def predict_doubles(self, inputs):
        sum = 0.0
        for item in inputs:
            sum += item
        return sum

    def predict_bytes(self, inputs):
        pass

    def predict_strings(self, inputs):
        sum = ""
        for item in inputs:
            sum += item
        return sum

if __name__ == "__main__":

    port = 7000

    model_name = "sum-model"
    model_version = 1

    input_type = "ints"

    model = SumContainer()
    rpc_service = grpc_server.GrpcServer()
    rpc_service.start(model, port, model_name, model_version, input_type)