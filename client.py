import grpc
import currency_converter_pb2
import currency_converter_pb2_grpc

def run():
    # Solicita as informações do usuário
    from_currency = input("Digite a moeda de origem (ex: USD): ").upper()
    to_currency = input("Digite a moeda de destino (ex: BRL): ").upper()
    amount = float(input("Digite o valor a ser convertido: "))

    # Conectar ao servidor
    with grpc.insecure_channel('localhost:50051') as channel:  # Substituir pelo IP do servidor
        stub = currency_converter_pb2_grpc.CurrencyConverterStub(channel)
        
        # Solicitar a conversão
        request = currency_converter_pb2.ConvertRequest(from_currency=from_currency, to_currency=to_currency, amount=amount)
        try:
            response = stub.Convert(request)
            print(f'{amount} {from_currency} convertido para {to_currency}: {response.converted_amount}')
        except grpc.RpcError as e:
            print(f"Erro na conversão: {e.details()}")

if __name__ == '__main__':
    run()
