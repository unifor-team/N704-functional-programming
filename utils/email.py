from .emailutils import construir_email, receber_dados_envio, enviar_email_smtp

def enviar_email(destinatario, assunto, corpo):
    dados = receber_dados_envio()
    msg = construir_email(dados['remetente'], destinatario, assunto, corpo)
    enviar_email_smtp(dados['remetente'], dados['senha'], msg)
    
def criar_assunto_corpo(msg, corpo):
    return {"assunto": msg, "corpo": corpo}

def retornar_assunto_exclusao(user_id):
    assunto = "Conta excluída"
    corpo = f"Olá,\n\nSua conta com o ID {user_id} foi excluída com sucesso."
    return criar_assunto_corpo(assunto, corpo)
    