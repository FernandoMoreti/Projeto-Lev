from ..mapper import Mapper

class C6bank(Mapper):

    def map(self, line):
        model = self.createNullModel()

        model[""]