import grpc
from tensorflow_serving.apis import predict_pb2 as tensorflow__serving_dot_apis_dot_predict__pb2
from tensorflow_serving.apis import prediction_service_pb2 as tensorflow__serving_dot_apis_dot_prediction_service__pb2
import tensorflow as tf

def run():
    channel = grpc.insecure_channel("127.0.0.1:7000")
    stub = tensorflow__serving_dot_apis_dot_prediction_service__pb2.PredictionServiceStub(channel)

    request = tensorflow__serving_dot_apis_dot_predict__pb2.PredictRequest()
    request.model_spec.name = "sum-model"
    request.model_spec.signature_name = "predict_ints"
    request.inputs["X"].CopyFrom(
        tf.contrib.util.make_tensor_proto([1, 4, 3, 4], shape=[4]))
    response = stub.Predict(request)
    print(response)

if __name__ == "__main__":
    run()