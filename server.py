import grpc
from concurrent import futures
import requests
import currency_converter_pb2
import currency_converter_pb2_grpc

API_KEY = '482488c653929630c62e5332'
API_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/'

class CurrencyConverterServicer(currency_converter_pb2_grpc.CurrencyConverterServicer):
    def Convert(self, request, context):
        from_currency = request.from_currency
        to_currency = request.to_currency
        amount = request.amount
        
        # Fazer a requisição para obter a taxa de conversão
        try:
            response = requests.get(f'{API_URL}{from_currency}/{to_currency}')
            data = response.json()

            # Verifica se a resposta da API foi bem-sucedida
            if response.status_code == 200 and data['result'] == 'success':
                conversion_rate = data['conversion_rate']
                converted_amount = amount * conversion_rate
                return currency_converter_pb2.ConvertResponse(converted_amount=converted_amount)
            else:
                context.set_details(f"Erro ao obter taxa de conversão: {data.get('error-type', 'Erro desconhecido')}")
                context.set_code(grpc.StatusCode.INTERNAL)
                return currency_converter_pb2.ConvertResponse()

        except Exception as e:
            context.set_details(f"Erro na requisição à API: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return currency_converter_pb2.ConvertResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    currency_converter_pb2_grpc.add_CurrencyConverterServicer_to_server(CurrencyConverterServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor de conversão de moedas rodando na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
