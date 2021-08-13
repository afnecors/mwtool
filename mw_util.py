#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

class RevUtil:
    def __init__(self, mwc_revs):
        # lista da più nuova a più vecchia
        self.revs_lista_dritta = mwc_revs

        # lista da più vechia a più nuova
        self.revs_lista_rovesciata = reversed(self.revs_lista_dritta)

        # mappa con id l'id della rev
        self.revs_mappa = {rev['revid']: rev for rev in self.revs_lista_dritta}

        # totale di revs
        self.number_of_revision = len(self.revs_lista_dritta)

    def get_rev_by_id(self, id: int):
        return self.revs_mappa[id]

    def get_parent_rev_by_id(self, id: int):
        # ottieni la rev
        rev = self.get_rev_by_id(id)
        # ottieni la rev parent
        return self.get_rev_by_id(rev['parentid'])

    def get_between(self, from_id: int, to_id: int):
        # from è la rev newer
        # to è la rev older
        if from_id < to_id:
            c = from_id
            from_id = to_id
            to_id = c

        lista = []

        rev = self.get_rev_by_id(from_id)
        lista.append(rev)

        while True:
            # if the parentid is 0 it is the first revision
            if rev['parentid'] == 0:
                break
            else:
                rev = self.get_rev_by_id(rev['parentid'])
                lista.append(rev)
                if rev['parentid'] == to_id:
                    # appendi l'ultima e esci
                    last = self.get_rev_by_id(rev['parentid'])
                    lista.append(last)
                    break

        return lista

    def get_by_user(self, username: str):
        filtered = [
            rev for rev in self.revs_lista_dritta if rev['user'] == username]
        return filtered

    def get_first_revision(self):
        return self.revs_lista_dritta[0]

    def get_last_revision(self):
        return self.revs_lista_dritta[-1]

    def has_revision_by_id(self, id) -> bool:
        return id in self.revs_mappa
