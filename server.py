import grpc
from concurrent import futures
import currency_converter_pb2
import currency_converter_pb2_grpc

# Taxas de conversão
conversion_rates = {
    ('USD', 'BRL'): 5.4,
    ('USD', 'EUR'): 0.85,
    ('BRL', 'USD'): 0.19,
    ('BRL', 'EUR'): 0,16,
    ('EUR', 'USD'): 1.18,
    ('EUR', 'BRL'): 6.15
}

class CurrencyConverterServicer(currency_converter_pb2_grpc.CurrencyConverterServicer):
    def Convert(self, request, context):
        from_currency = request.from_currency
        to_currency = request.to_currency
        amount = request.amount
        
        # Verifica se a conversão é possível
        if (from_currency, to_currency) in conversion_rates:
            rate = conversion_rates[(from_currency, to_currency)]
            converted_amount = amount * rate
            return currency_converter_pb2.ConvertResponse(converted_amount=converted_amount)
        else:
            context.set_details(f"Conversão de {from_currency} para {to_currency} não suportada.")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
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