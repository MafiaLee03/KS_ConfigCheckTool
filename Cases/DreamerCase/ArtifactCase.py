from Core.BaseCase import BaseCase

class ArtifactCase(BaseCase):
    """
    Artifact表检查 1、id不能重复
    """
    def run(self):
        self.add_depends('Artifact')
        Artifact = self._Artifact
        self.add_depends('Language')
        Language = self._Language
        self.tag_repeat(Artifact,'id')
        self.a_in_b(Artifact,Language,'name')
        self.a_in_b(Artifact,Language,'des')
        self.a_in_b(Artifact,Language,'skillDes',va=-1)
