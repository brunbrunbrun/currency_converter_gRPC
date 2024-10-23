import grpc
import currency_converter_pb2
import currency_converter_pb2_grpc

def run():
    # Conectar ao servidor
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = currency_converter_pb2_grpc.CurrencyConverterStub(channel)
        
        # Solicitar a conversão
        from_currency = 'USD'
        to_currency = 'BRL'
        amount = 100.0
        
        request = currency_converter_pb2.ConvertRequest(from_currency=from_currency, to_currency=to_currency, amount=amount)
        try:
            response = stub.Convert(request)
            print(f'{amount} {from_currency} convertido para {to_currency}: {response.converted_amount}')
        except grpc.RpcError as e:
            print(f"Erro na conversão: {e.details()}")

if __name__ == '__main__':
    run()
