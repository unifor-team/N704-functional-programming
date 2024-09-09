from emailutils import construir_email, receber_dados_envio, enviar_email_smtp

def enviar_email(destinatario, assunto, corpo):
    dados = receber_dados_envio()
    msg = construir_email(dados['remetente'], destinatario, assunto, corpo)
    enviar_email_smtp(dados['remetente'], dados['senha'], msg)