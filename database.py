from models import Session, Command, File, Admin
import json

def get_files_by_command(command_id):
    session = Session()
    command = session.query(Command).filter_by(command_id=command_id).first()
    if command:
        files = command.files
        session.close()
        file_ids = [file.file_id for file in files]
        print(f"Найденные файлы для команды {command_id}: {file_ids}")  # Вывод в консоль
        return file_ids
    session.close()
    return []



def add_command_with_files(command_id, file_ids):
    session = Session()
    command = session.query(Command).filter_by(command_id=command_id).first()
    if not command:
        # Если команды еще нет, создаем новую
        command = Command(command_id=command_id)
        session.add(command)
        session.commit()
    
    for file_id in file_ids:
        new_file = File(file_id=file_id, command=command)
        session.add(new_file)
    try:
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении файлов: {e}")
        return False
    finally:
        session.close()

def add_admin(user_id):
    session = Session()
    exists = session.query(Admin).filter_by(user_id=user_id).first()
    if not exists:
        new_admin = Admin(user_id=user_id)
        session.add(new_admin)
        session.commit()
        session.close()
        return True
    session.close()
    return False

def remove_admin(user_id):
    session = Session()
    admin = session.query(Admin).filter_by(user_id=user_id).first()
    if admin:
        session.delete(admin)
        session.commit()
        result = True
    else:
        result = False
    session.close()
    return result

def is_admin(user_id):
    session = Session()
    admin = session.query(Admin).filter_by(user_id=user_id).first()
    session.close()
    return bool(admin)

def remove_file(command_id):
    session = Session()
    command = session.query(Command).filter_by(command_id=command_id).first()
    if command:
        # Если команда найдена, удаляем все связанные файлы
        for file in command.files:
            session.delete(file)
        session.delete(command)  # Опционально: удаляем саму команду, если необходимо
        session.commit()
        session.close()
        return True
    else:
        session.close()
        return False

def command_exists(command_id):
    session = Session()
    exists = session.query(Command).filter_by(command_id=command_id).first() is not None
    session.close()
    return exists
