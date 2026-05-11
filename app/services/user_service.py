from app.repositories import user_repo as crud

def registrar_nuevo_usuario(db, email, gender):
    # Lógica de negocio: Verificar si existe antes de crear
    existente = crud.get_usuario_by_email(db, email)
    if existente:
        raise Exception("El usuario ya existe")
    
    usuario = crud.crear_usuario(db, email, gender)
    # Lógica extra: Enviar email (pseudocódigo)
    # email_service.send_welcome(email)
    return usuario