import os
from ext.data_encrypt import DataEncrypt
from ext.database import db
from ext.message_status_generator import MessageStatusGenerator
from flask import Response, url_for  # type: ignore
from model.livro_model import LivroModel
from sqlalchemy.exc import IntegrityError  # type: ignore
from urllib.parse import unquote
from utils.minio_utils import MinioUtil
from werkzeug.datastructures import FileStorage  # type: ignore
from sqlalchemy import func  # type: ignore


class LivroController:
    def __init__(self, form: dict | None = None, files: dict | None = None):
        if form:
            self.titulo: str = form.get('titulo')
            self.autor: str = form.get("autor")
            self.editora: str = form.get("editora")
        if files:
            self.capa: FileStorage = files.get("capa")
            self.livro: FileStorage = files.get("livro")
        self.result = None


    def get_result(self):
        return self.result

    def save_livro_on_db(self) -> dict:
        livro: object = LivroModel(
            titulo=self.titulo,
            autor=self.autor,
            editora=self.editora)
        try:
            db.session.add(livro)
            db.session.commit()
            self.codigo = livro.id
            return MessageStatusGenerator.build_status_success('Livro cadastrado com sucesso')
        except IntegrityError:
            db.session.rollback()
            return MessageStatusGenerator.build_status_error('Erro ao cadastrar livro')

    def remove_livro(self):
        livro = self.get_livro_by_codigo(self.codigo)
        db.session.delete(livro)
        db.session.commit()

    
    def set_livro_id(self, livro_id):
        self.codigo=livro_id


    def create_documentos_list(self) -> list:
        BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        UPLOAD_FOLDER: str = os.path.join(BASE_DIR, 'static', 'uploads')
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        capa_path: str | None = None
        livro_path: str | None = None
        if self.capa:
            capa_path = os.path.join(UPLOAD_FOLDER, self.capa.filename)
            self.capa.save(capa_path)
        if self.livro:
            livro_path = os.path.join(UPLOAD_FOLDER, self.livro.filename)
            self.livro.save(livro_path)

        self.documentos: list = [
            {'tipo': 'capa', 'arquivo': self.capa, 'path': capa_path, 'ext': 'jpeg'},
            {'tipo': 'livro', 'arquivo': self.livro, 'path': livro_path, 'ext': 'pdf'}
        ]

        
    def create_documentos_on_bucket_and_db(self) -> dict:
        for doc in self.documentos:
            if doc['arquivo']:
                caminho_arquivo: str = f"{self.codigo}/{doc['tipo']}/{self.titulo}.{doc['ext']}"
                doc['arquivo'].stream.seek(0, os.SEEK_END)
                file_length: int = doc['arquivo'].stream.tell()
                doc['arquivo'].stream.seek(0)
                try:
                    MinioUtil().upload_file(
                        bucket_name='biblioteca',
                        arquivo_local=caminho_arquivo,
                        data=doc['arquivo'].stream,
                        length=file_length,
                        content_type=doc['arquivo'].content_type,
                    )
                    self.update_livro_on_db(doc, caminho_arquivo)                  
                except Exception:
                    db.session.rollback()
                    self.remove_livro()
                    self.result = MessageStatusGenerator.build_status_error('Erro ao salvar arquivos do livro.')
                    if doc['path'] and os.path.exists(doc['path']):
                        os.remove(doc['path'])
                    return self.result
                if doc['path'] and os.path.exists(doc['path']):
                    os.remove(doc['path'])
                self.result = MessageStatusGenerator.build_admin_status_success('Livro finalizado com sucesso')


    def update_livro_on_db(self, doc: dict, caminho_arquivo: str) -> dict:
        livro = self.get_livro_by_codigo(self.codigo)
        if livro is None:
            raise ValueError("Livro não encontrado")

        if doc['tipo'] == 'capa':
            livro.capa_url = DataEncrypt.get_encrypted_aead(caminho_arquivo)    
        else:
            livro.livro_url = DataEncrypt.get_encrypted_aead(caminho_arquivo)

        db.session.commit()
        return livro
    
    def update_livro(self):
        
        livro = self.get_livro_by_codigo(self.codigo)
        livro.titulo = self.titulo
        livro.autor = self.autor
        livro.editora = self.editora
        db.session.commit()


    def get_minio_file(path: str) -> Response:
        decoded_path = path
        decrypted_path = DataEncrypt.get_decrypted_aead(decoded_path)
        minio_cliente: object = MinioUtil()
        document_data = minio_cliente.get_minio_object_data(decrypted_path)
        return document_data

    def get_document_perfil_name(path: str) -> str:
        decoded_path = path
        decrypted_path = DataEncrypt.get_decrypted_aead(decoded_path)
        if decrypted_path:
            return decrypted_path.split('/')[-1].replace('_', ' ')

    @staticmethod
    def get_all_livros_dict() -> list:
        livros = LivroModel.query.all()
        if livros:
            return [{
                    'id': livro.id,
                    'titulo': livro.titulo,
                    'autor': livro.autor,
                    'editora': livro.editora,
                    'capa_url': livro.capa_url,
                    'livro_url': livro.livro_url
                } for livro in livros]

    @staticmethod
    def get_all_livros_decrypted_dict() -> list:
        livros = LivroModel.query.all()
        if livros:
            return [{
                    'id': livro.id,
                    'titulo': livro.titulo,
                    'autor': livro.autor,
                    'editora': livro.editora,
                    'capa_url': DataEncrypt.get_decrypted_aead(livro.capa_url),
                    'livro_url': DataEncrypt.get_decrypted_aead(livro.livro_url)
                } for livro in livros]

    @staticmethod
    def get_random_book_covers():
        livros = LivroModel.query.order_by(func.random()).limit(10).all()
        capas = [DataEncrypt.get_decrypted_aead(livro.capa_url) for livro in livros]
        return capas
    
    @staticmethod
    def get_livro_by_codigo(codigo: int) -> object:
        return LivroModel.query.filter_by(id=codigo).first()
    
    @staticmethod
    def get_livro_dict_by_codigo(codigo: int) -> dict:
        livro = LivroModel.query.filter_by(id=codigo).first()
        if livro:
            livro_dict = {c.name: getattr(livro, c.name) for c in livro.__table__.columns}
            return livro_dict
        return None

    def delete_livro_by_id(self, livro_id):
        livro = LivroController.get_livro_by_codigo(livro_id)
        livro_nome = livro.titulo
        if livro:
            try:
                db.session.delete(livro)
                db.session.commit()
                self.result = MessageStatusGenerator.build_admin_status_success(f'Livro {livro_nome} excluido')
            except Exception:
                self.result = MessageStatusGenerator.build_status_error(f'Erro ao excluir livro {livro_nome}')

    def delete_book_from_minio(self, livro_id):
        minio_cliente: object = MinioUtil()
        minio_cliente.delete_minio_file(bucket_name='biblioteca', object_name=livro_id)