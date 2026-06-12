from sqlalchemy.orm import Session
from models.contact import Contact
from repositories.abstract_repository import AbstractRepository


class ContactRepository(AbstractRepository):
    def create(self, user_id: int, contact_id: int):
        contact_model = Contact(
            user_id = user_id,
            contact_id = contact_id
        )
        self.db.add(contact_model)
        self.db.commit()
    
    def delete(self, user_id: int, contact_id: int):
        self.db.query(Contact).filter(
            Contact.user_id == user_id,
            Contact.contact_id == contact_id
        ).delete()
        self.db.commit()