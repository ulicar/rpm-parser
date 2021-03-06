#!/usr/bin/python3


from .constants import *
from .utility import *
import pdb

class Lead(object):
    def __init__(self):
        self.version = None
        self.type = None
        self.arhitecture = None                   # 2
        self.package_name = None                  # 66
        self.operating_system = None              # 2
        self.signature = None                     # 2
        self.reserved = None                      # 4

    @staticmethod
    def size():
        return 96

    def __str__(self):
        return "Version: {0}\nPackageType: {1}\nArhitecture: {2}\n"\
            "PackageName: {3}\nOperatingSystem: {4}\nSignature: {5}\n"\
            "".format(
                    self.version, self.type, self.arhitecture,
                    self.package_name, self.operating_system, self.signature,
                    )

    @classmethod
    def parse(cls, archive, entry_point=4):
        archive.seek(entry_point)

        lead = cls()
        rpm_version = archive.read(2)
        lead.version = '{major}.{minor}'.format(major=c2i(rpm_version[0:1]), minor=c2i(rpm_version[1:2]))
        lead.type = PackageType(s2i(archive.read(2)))
        lead.arhitecture = Arhitecture(s2i(archive.read(2)))
        lead.package_name = archive.read(66).decode('utf-8').strip('\0')
        lead.operating_system = OperatingSystem(s2i(archive.read(2)))
        lead.signature = SignatureType(s2i(archive.read(2)))
        lead.reserved = archive.read(16)

        return lead


class Index(object):
    def __init__(self):
        self.tag = None
        self.type = None
        self.offset = None
        self.count = None

    def read(self, archive):
        if self.type in [IndexTags.STRING, IndexTags.I18STRING, IndexTags.BIN]:

            return read_string(archive)

        if self.type in [IndexTags.STRING_ARRAY]:

            return ','.join(read_string(archive) for _ in range(self.count))

        if self.type in [IndexTags.INT16, IndexTags.INT32]:
            type_size = IndexSettings[self.type.name].value[0]
            extractor = IndexSettings[self.type.name].value[1]

            return str(extractor(archive.read(type_size)))

    def __str__(self):
        return "Tag: {0},\tType: {1},\tOffset: {2},\tCount: {3}"\
                "".format(self.tag, self.type, self.offset, self.count)

    @classmethod
    def parse(cls, archive, entry_point, tags):
        archive.seek(entry_point)

        index = cls()
        index.tag = tags(i2i(archive.read(4)))
        index.type = IndexTags(i2i(archive.read(4)))
        index.offset = i2i(archive.read(4))
        index.count = i2i(archive.read(4))

        return index

    def aquire(self, archive, base_position):
        archive.seek(base_position + self.offset)

        return self.read(archive)


class Header(object):
    MAGIC = b'\x8e\xad\xe8'
    def __init__(self):
        self.version = None
        self.reserverd = None
        self.index_entries_count = None
        self.index_enties = None
        self.header_size = None

    def size(self):
        return self.header_size

    def __str__(self):
        representation = "HeaderVersion: {0}\nIndexEntriesCount: {1}\nEntries:\n"\
                "".format(self.version, self.index_entries_count)

        for index_entry in self.index_entries:
            entry = "\t{}\n".format(index_entry)

            representation += entry

        representation += "HeaderSize: {}".format(self.header_size)

        return representation  


    @classmethod
    def parse(cls, archive, entry_point, tags):
        archive.seek(entry_point)

        assert cls.MAGIC == archive.read(3), 'Wrong header in RPM archive'

        header = cls()
        header.version = c2i(archive.read(1))
        header.reserved = archive.read(4)
        header.index_entries_count = i2i(archive.read(4))
        header.header_size = i2i(archive.read(4))
        header.index_entries = list()

        for _ in range(0, header.index_entries_count):
            index = Index.parse(archive, archive.tell(), tags) 
            header.index_entries.append(index)

        header.index_entries.sort(key=lambda index: index.offset)
    
        return header


class Store(object):
    def __init__(self, starting_point=None):
        self.starting_point = starting_point
        self.data = dict()

    def __str__(self):
        pass
    
    @classmethod
    def parse(cls, archive, starting_point, index_entries):
        store = cls(starting_point)

        for index in index_entries:
            data = index.aquire(archive, starting_point)
            log(index.tag.name +'  '+ str(data))
            
            #store.data[index.tag] = data

        return store
            


class RPM(object):
    MAGIC = b'\xed\xab\xee\xdb'

    def __init__(self):
        self.lead = None
        self.signature = None
        self.header = None
        self.store = None

    def __str__(self):
        return "Lead: \n{0}\nSignature: {1}\nHeader: {2}".format(
                str(self.lead).replace('\n', '\t\n'),
                str(self.signature).replace('\n', '\t\n'),
                str(self.header).replace('\n', '\t\n')
                )

    @classmethod
    def parse(cls, archive, entry_point=0):
        assert cls.MAGIC == archive.read(4), 'File {f} is not a RPM self.archive'.format(f=self.__archive)
        
        rpm = cls()
        rpm.lead = Lead.parse(archive, 4)
        #log(rpm.lead)


        rpm.signature = Header.parse(archive, rpm.lead.size(), SignatureTags)
        #log(rpm.signature)

        rpm.header = Header.parse(archive, 456, HeaderTags)

        rpm.store = Store.parse(archive, archive.tell(), rpm.header.index_entries)

        return None

