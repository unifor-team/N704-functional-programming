USER_ERROR_MSG = 'Usuário não encontrado'

#lambda functions
USER_DELETED = lambda msg : f'Usuário com ID {msg} excluído com sucesso!'
USER_ERRO_DELETE = lambda e: f'Erro ao excluir o usuário: {e}'
USER_CREATED = lambda name: f"User {name} created!"

INSUFICIENT_MSG = 'Dados insuficientes'

EMAIL_SUCCESSS = 'Email enviado com sucesso!'