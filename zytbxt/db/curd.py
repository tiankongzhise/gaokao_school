from tk_db_utils import BaseCurd
from .models import SchoolInfoTable, ZyzInfoTable,ZyInfoTable,LsZyzInfoTable,LsZyInfoTable


from typing import Iterable


class SchoolInfoCurd(BaseCurd):
    
    def bulk_insert(self, objects: Iterable, chunk_size: int = 3000) -> int:    
        return super().bulk_insert(SchoolInfoTable, objects, chunk_size)

    def bulk_insert_ignore(self, objects: Iterable, chunk_size: int = 3000) -> int:
        return super().bulk_insert_ignore(SchoolInfoTable, objects, chunk_size)

    def bulk_insert_ignore_in_chunks(self, objects: Iterable, chunk_size: int = 3000) -> int:
        return super().bulk_insert_ignore_in_chunks(SchoolInfoTable, objects, chunk_size)
        
    def bulk_replace_into(self, objects: Iterable, chunk_size: int = 3000) -> int:
        return super().bulk_replace_into(SchoolInfoTable, objects, chunk_size)

class ZyzInfoCurd(BaseCurd):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_chunk_size()
        
    def set_chunk_size(self, chunk_size: int = 3000):
        self.chunk_size = chunk_size

    def bulk_insert(self, objects: Iterable) -> int:    
        return super().bulk_insert(ZyzInfoTable, objects, self.chunk_size)
    
    def bulk_insert_ignore(self, objects: Iterable) -> int:
        return super().bulk_insert_ignore(ZyzInfoTable, objects, self.chunk_size)
    
    def bulk_insert_ignore_in_chunks(self, objects: Iterable) -> int:
        return super().bulk_insert_ignore_in_chunks(ZyzInfoTable, objects, self.chunk_size)
    
    def bulk_replace_into(self, objects: Iterable) -> int:
        return super().bulk_replace_into(ZyzInfoTable, objects, self.chunk_size)

class ZyInfoCurd(BaseCurd):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_chunk_size()
        
    def set_chunk_size(self, chunk_size: int = 3000):
        self.chunk_size = chunk_size

    def bulk_insert(self, objects: Iterable) -> int:    
        return super().bulk_insert(ZyInfoTable, objects, self.chunk_size)
    
    def bulk_insert_ignore(self, objects: Iterable) -> int:
        return super().bulk_insert_ignore(ZyInfoTable, objects, self.chunk_size)
    
    def bulk_insert_ignore_in_chunks(self, objects: Iterable) -> int:
        return super().bulk_insert_ignore_in_chunks(ZyInfoTable, objects, self.chunk_size)
    
    def bulk_replace_into(self, objects: Iterable) -> int:
        return super().bulk_replace_into(ZyInfoTable, objects, self.chunk_size)

class LsZyzInfoCurd(BaseCurd):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_chunk_size()
        
    def set_chunk_size(self, chunk_size: int = 3000):
        self.chunk_size = chunk_size

    def bulk_insert(self, objects: Iterable) -> int:    
        return super().bulk_insert(LsZyzInfoTable, objects, self.chunk_size)
    
    def bulk_insert_ignore(self, objects: Iterable) -> int:
        return super().bulk_insert_ignore(LsZyzInfoTable, objects, self.chunk_size)

    
    def bulk_insert_ignore_in_chunks(self, objects: Iterable) -> int:
        return super().bulk_insert_ignore_in_chunks(LsZyzInfoTable, objects, self.chunk_size)
    
    def bulk_replace_into(self, objects: Iterable) -> int:
        return super().bulk_replace_into(LsZyzInfoTable, objects, self.chunk_size)

class LsZyInfoCurd(BaseCurd):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_chunk_size()
        
    def set_chunk_size(self, chunk_size: int = 3000):
        self.chunk_size = chunk_size

    def bulk_insert(self, objects: Iterable) -> int:    
        return super().bulk_insert(LsZyInfoTable, objects, self.chunk_size)
    
    def bulk_insert_ignore(self, objects: Iterable) -> int:
        return super().bulk_insert_ignore(LsZyInfoTable, objects, self.chunk_size)
    
    def bulk_insert_ignore_in_chunks(self, objects: Iterable) -> int:
        return super().bulk_insert_ignore_in_chunks(LsZyInfoTable, objects, self.chunk_size)
    
    def bulk_replace_into(self, objects: Iterable) -> int:
        return super().bulk_replace_into(LsZyInfoTable, objects, self.chunk_size)
    