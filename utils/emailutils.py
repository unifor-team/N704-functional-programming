import email.message
import smtplib
import os

def construir_email(remetente, destinatario, assunto, corpo):
    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo)
    return msg
  
def enviar_email_smtp(remetente, senha, msg):
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        servidor.quit()
        return f"E-mail enviado para {msg['To']} com sucesso!"
    except Exception as e:
        return f"Erro ao enviar o e-mail: {e}"

def receber_dados_envio():
    remetente = os.getenv('EMAIL_REMETENTE')
    senha = os.getenv('SENHA_REMETENTE')
    
    return {"remetente": remetente, "senha": senha}
