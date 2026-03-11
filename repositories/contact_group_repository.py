from sqlalchemy.orm import Session

from models.contact_group import ContactGroup, ContactGroupContact


class ContactGroupRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_id: int, title: str) -> int:
        contact_group_model = ContactGroup(
            user_id = user_id,
            title = title
            )
        self.db.add(contact_group_model)
        self.db.commit()
        self.db.refresh(contact_group_model)
        return contact_group_model.id
    
    def delete(self, contact_group_id: int):
        self.db.query(ContactGroup).filter(
            ContactGroup.id == contact_group_id
        ).delete()
        self.db.commit()
    
    def add_contact_into_group(self, contact_group_id: int, contact_id: int):
        contact_group_model = ContactGroupContact(
            contact_group_id = contact_group_id,
            contact_id = contact_id
        )
        self.db.add(contact_group_model)
        self.db.commit()
    
    def delete_contact_from_group(self, contact_group_id: int, contact_id: int):
        self.db.query(ContactGroupContact).filter(
            ContactGroupContact.contact_group_id == contact_group_id,
            ContactGroupContact.contact_id == contact_id
        ).delete()
        self.db.commit()