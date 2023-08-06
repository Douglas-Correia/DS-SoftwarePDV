from pynfse import NFSe
import pynfe
def integrar_nfse(numero_nfse, valor_nfse, cnpj_emitente, cnpj_destinatario):
    # Crie uma instância da classe NFSe
    nfse = NFSe()

    # Defina as informações da nota fiscal eletrônica
    nfse.numero_nfse = numero_nfse
    nfse.valor_nfse = valor_nfse
    nfse.cnpj_emitente = cnpj_emitente
    nfse.cnpj_destinatario = cnpj_destinatario

    # Faça a integração com o provedor de nota fiscal eletrônica
    nfse.enviar()

    # Verifique o resultado da integração
    if nfse.sucesso:
        return "Integração realizada com sucesso!"
    else:
        return "Erro na integração: " + nfse.mensagem_erro