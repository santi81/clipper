import time

from concurrent import futures
from tensorflow_serving.apis import predict_pb2 as tensorflow__serving_dot_apis_dot_predict__pb2
from tensorflow_serving.apis import prediction_service_pb2 as tensorflow__serving_dot_apis_dot_prediction_service__pb2
import grpc
import tensorflow as tf
from tensorflow.python.framework import tensor_util

INPUT_TYPE_BYTES = 0
INPUT_TYPE_INTS = 1
INPUT_TYPE_FLOATS = 2
INPUT_TYPE_DOUBLES = 3
INPUT_TYPE_STRINGS = 4
_ONE_DAY_IN_SECONDS = 60 * 60 *24

def string_to_input_type(input_str):
    input_str = input_str.strip().lower()
    byte_strs = ["b", "bytes", "byte"]
    int_strs = ["i", "ints", "int", "integer", "integers"]
    float_strs = ["f", "floats", "float"]
    double_strs = ["d", "doubles", "double"]
    string_strs = ["s", "strings", "string", "strs", "str"]

    if any(input_str == s for s in byte_strs):
        return INPUT_TYPE_BYTES
    elif any(input_str == s for s in int_strs):
        return INPUT_TYPE_INTS
    elif any(input_str == s for s in float_strs):
        return INPUT_TYPE_FLOATS
    elif any(input_str == s for s in double_strs):
        return INPUT_TYPE_DOUBLES
    elif any(input_str == s for s in string_strs):
        return INPUT_TYPE_STRINGS
    else:
        return -1

class Server(tensorflow__serving_dot_apis_dot_prediction_service__pb2.PredictionServiceServicer):

    def Predict(self, request, context):
        predict_fn = self.get_prediction_function()
        outputs = self.get_output(predict_fn, request)

        response = tensorflow__serving_dot_apis_dot_predict__pb2.PredictResponse(outputs = {"outputs_Y": tf.contrib.util.make_tensor_proto(", "''.join(str(e) for e in outputs), shape=[1])})
        return response

    def get_prediction_function(self):
        if self.model_input_type == INPUT_TYPE_INTS:
            return self.model.predict_ints
        elif self.model_input_type == INPUT_TYPE_FLOATS:
            return self.model.predict_floats
        elif self.model_input_type == INPUT_TYPE_DOUBLES:
            return self.model.predict_doubles
        elif self.model_input_type == INPUT_TYPE_BYTES:
            return self.model.predict_bytes
        elif self.model_input_type == INPUT_TYPE_STRINGS:
            return self.model.predict_strings
        else:
            print(
                "Attempted to get predict function for invalid model input type!"
            )

    def get_output(self, predict_fn, request):
        if self.model_input_type == INPUT_TYPE_INTS:
            return predict_fn(tensor_util.MakeNdarray(request.inputs["X"]))
        if self.model_input_type == INPUT_TYPE_FLOATS:
            return predict_fn(tensor_util.MakeNdarray(request.inputs["X"]))
        if self.model_input_type == INPUT_TYPE_DOUBLES:
            return predict_fn(tensor_util.MakeNdarray(request.inputs["X"]))
        if self.model_input_type == INPUT_TYPE_BYTES:
            return predict_fn(tensor_util.MakeNdarray(request.inputs["X"]))
        if self.model_input_type == INPUT_TYPE_STRINGS:
            return predict_fn(tensor_util.MakeNdarray(request.inputs["X"]))

class ModelContainerBase(object):
    def predict_ints(self, inputs):
        pass

    def predict_floats(self, inputs):
        pass

    def predict_doubles(self, inputs):
        pass

    def predict_bytes(self, inputs):
        pass

    def predict_strings(self, inputs):
        pass

class GrpcServer:
    def __init__(self):
        pass

    def start(self, model, port, model_name, model_version, input_type):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.newServer = Server()
        model_input_type = string_to_input_type(input_type)
        self.newServer.model_name = model_name
        self.newServer.model_version = model_version
        self.newServer.model_input_type = model_input_type
        self.newServer.model = model
        tensorflow__serving_dot_apis_dot_prediction_service__pb2.add_PredictionServiceServicer_to_server(self.newServer, server)

        server.add_insecure_port("[::]:%s" % port)
        server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)