#!/usr/bin/python3

from enum import Enum
from .utility import *

__all__ = [
    'PackageType', 
    'OperatingSystem',
    'Arhitecture',
    'SignatureType',
    'SignatureTags',
    'HeaderTags',
    'IndexTags',
    'IndexSettings'
]

class PackageType(Enum):
    Binary = 0
    Source = 1


class OperatingSystem(Enum):
    Linux = 1


class Arhitecture(Enum):
    i386    = 1
    Alpha   = 2
    Sparc   = 3
    MIPS    = 4
    PowerPC = 5
    m68000  = 6
    SGI     = 7


class SignatureType(Enum):
    VERSION3 = 5


class SignatureTags(Enum):
    SIGTAG_DSA            = 267
    SIGTAG_RSA            = 268
    SIGTAG_SHA1           = 269
    SIGTAG_SIZE           = 1000
    SIGTAG_LEMD5_1        = 1001
    SIGTAG_PGP            = 1002
    SIGTAG_LEMD5_2        = 1003  
    SIGTAG_MD5            = 1004
    SIGTAG_GPG            = 1005
    SIGTAG_PGP5           = 1006
    SIGTAG_PAYLOADSIZE    = 1007
    SIGTAG_BADSHA1_1      = 1008
    SIGTAG_BADSHA1_2      = 1009
    SIGTAG_SHA1HEADER     = 1010
    SIGTAG_DSAHEADER      = 1011
    SIGTAG_RSAHEADER      = 1012
    # Private tags
    TAG_HEADERSIGNATURES  = 62
    TAG_HEADERIMMUTABLE   = 63
    TAG_HEADERI18NTABLE   = 100


class HeaderTags(Enum):
    TAG_HEADERSIGNATURES  = 62
    TAG_HEADERIMMUTABLE   = 63
    TAG_HEADERI18NTABLE   = 100
    TAG_NAME              = 1000
    TAG_VERSION           = 1001
    TAG_RELEASE           = 1002
    RAG_SERIAL            = 1003
    TAG_SUMMARY           = 1004
    TAG_DESCRIPTION       = 1005
    TAG_BUILDTIME         = 1006
    TAG_BUILDHOST         = 1007
    TAG_ISNTALLTIME       = 1008
    TAG_SIZE              = 1009
    TAG_DISTRIBUTION      = 1010
    TAG_VENDOR            = 1011
    TAG_GIF               = 1012
    TAG_XPM               = 1013
    TAG_LICENSE           = 1014
    TAG_PACKAGER          = 1015
    TAG_GROUP             = 1016
    TAG_CHANGELOG         = 1017
    TAG_SOURCE            = 1018
    TAG_PATCH             = 1019
    TAG_URL               = 1020
    TAG_OS                = 1021
    TAG_ARCH              = 1022
    TAG_PREIN             = 1023
    TAG_POSTIN            = 1024
    TAG_PREUN             = 1025
    TAG_POSTUN            = 1026
    TAG_OLDFILENAMES      = 1027
    TAG_FILESIZES         = 1028
    TAG_FILESTATS         = 1029
    TAG_FILEMODES         = 1030
    TAG_FILEUIDS          = 1031
    TAG_FILEGIDS          = 1032
    TAG_FILERDEVS         = 1033
    TAG_FILEMTIMES        = 1034
    TAG_FILEMD5S          = 1035
    TAG_FILELINKTOS       = 1036
    TAG_FILEFLAGS         = 1037
    TAG_FILEUSERNAME      = 1039
    TAG_FILEGROUPNAME     = 1040
    TAG_EXCLUDE           = 1041
    TAG_EXCLUSIVE         = 1042
    TAG_ICON              = 1043
    TAG_SOURCERPM         = 1044
    TAG_FILEVERIFYFLAGS   = 1045
    TAG_ARCHIVESIZE       = 1046
    TAG_PROVIDENAME       = 1047
    TAG_REQUIREFLAGS      = 1048
    TAG_REQUIRENAME       = 1049
    TAG_REQUIREVERSION    = 1050
    TAG_NOSOURCE          = 1051
    TAG_NOPATCH           = 1052
    TAG_CONFLICTFLAGS     = 1053
    TAG_CONFLICTNAME      = 1054
    TAG_CONFLICTVERSION   = 1055
    TAG_DEFAULTPREFIX     = 1056
    TAG_BUILDROOT         = 1057
    TAG_INSTALLPREFIX     = 1058
    TAG_EXCLDUEARCH       = 1059
    TAG_EXCLUDEOS         = 1060
    TAG_EXCLUSIVEARCH     = 1061
    TAG_EXCLUSIVEOS       = 1062
    TAG_AUTOREQPROV       = 1063
    TAG_RPMVERSION        = 1064
    TAG_TRIGGERSCRIPTS    = 1065
    TAG_TRIGGERNAME       = 1066
    TAG_TRIGGERVERSION    = 1067
    TAG_TRIGGERFLAGS      = 1068 
    TAG_TRIGGERINDEX      = 1069

    TAG_VERIFYSCRIPT      = 1079
    TAG_CHANGELOGTIME     = 1080
    TAG_CHANGELOGNAME     = 1081
    TAG_CHANGELOGTEXT     = 1082
    TAG_BROKENMD5         = 1083
    TAG_PREREQ            = 1084
    TAG_PREINPROG         = 1085
    TAG_POSTINPROG        = 1086
    TAG_PREUNPROG         = 1087
    TAG_POSTUNPROG        = 1088
    TAG_BUILDARCHS        = 1089 
    TAG_VERIFYSCRIPTPROG  = 1091
    TAG_TRIGGERSCRIPTPROG = 1092
    TAG_DOCDIR            = 1093
    TAG_COOKIE            = 1094
    TAG_FILEDEVICES       = 1095
    TAG_FILEINODES        = 1096
    TAG_FILELANGS         = 1097
    TAG_PREFIXES          = 1098
    TAG_INSTPREFIXES      = 1099
    TAG_TRIGGERIN         = 1100
    TAG_TRIGGERUN         = 1101
    TAG_TRIGGERPOSTUN     = 1102
    TAG_AUTOREQ           = 1103
    TAG_AUTOPROV          = 1104
    TAG_CAPABILITY        = 1105
    TAG_SOURCEPACKAGE     = 1106
    TAG_OLDORIGFILENAMES  = 1107
    TAG_BUILDPREREQ       = 1108
    TAG_BUILDREQUIRES     = 1109
    TAG_BUILDCONFLICTS    = 1110
    TAG_BUILDMACROS       = 1111
    TAG_PROVIDEFLAGS      = 1112
    TAG_PROVIDEVERSION    = 1113
    TAG_OBSOLETEFLAGS     = 1114
    TAG_OBSOLETEVERSION   = 1115
    TAG_DIRINDEXES        = 1116
    TAG_BASENAMES         = 1117
    TAG_DIRNAMES          = 1118
    TAG_ORIGDIRINDEXES    = 1119
    TAG_ORIGBASENAMES     = 1120
    TAG_ORIGDIRNAMES      = 1121
    TAG_OPTFLAGS          = 1122
    TAG_DISTURL           = 1123
    TAG_PAYLOADFORMAT     = 1124
    TAG_PAYLOADCOMPRESSOR = 1125
    TAG_PAYLOADFLAGS      = 1126
    TAG_INSTALLCOLOR      = 1127
    TAG_INSTALLTID        = 1128
    TAG_REMOVETID         = 1129
    TAG_SHA1RHN           = 1130
    TAG_RHNPLATFORM       = 1131
    TAG_PLATFORM          = 1132
    TAG_PATCHESNAME       = 1133
    TAG_PATCHESFLAGS      = 1134
    TAG_PATCHESVERSION    = 1135
    TAG_CACHECTIME        = 1136
    TAG_CACHEPKGPATH      = 1137
    TAG_CACHEPKGSIZE      = 1138
    TAG_CACHEPKGMTIME     = 1139
    TAG_FILECOLORS        = 1140
    TAG_FILECLASS         = 1141
    TAG_CLASSDICT         = 1142
    TAG_FILEDEPENDSX      = 1143
    TAG_FILEDEPENDSN      = 1144
    TAG_DEPENDSDICT       = 1145
    TAG_SOURCEPKGID       = 1146
    TAG_FILECONTEXTS      = 1147
    TAG_FSCONTEXTS        = 1148
    TAG_RECONTEXTS        = 1149
    TAG_POLICIES          = 1150
    TAG_PRETRANS          = 1151
    TAG_POSTTRANS         = 1152
    TAG_PRETRANSPROG      = 1153
    TAG_POSTTRANSPROG     = 1154
    TAG_DISTTAG           = 1155
    TAG_SUGGESTSNAME      = 1156
    TAG_SUGGESTSVERSION   = 1157
    TAG_SUGGESTSFLAGS     = 1158
    TAG_ENHANCESNAME      = 1159
    TAG_ENHANCESVERSION   = 1160
    TAG_ENHANCESFLAGS     = 1161
    TAG_PRIORITY          = 1162
    TAG_CVSID             = 1163
    TAG_FIRSTFREE_TAG     = 1164
    TODO = 5011


class IndexTags(Enum):
    NULL         = 0
    CHAR         = 1  
    INT8         = 2 
    INT16        = 3 
    INT32        = 4 
    INT64        = 5 
    STRING       = 6 
    BIN          = 7 
    STRING_ARRAY = 8 
    I18STRING    = 9 


class IndexSettings(Enum):
    NULL         = (0, ())
    CHAR         = (1, lambda d: c2i(d[0:1]))
    INT8         = (2, lambda d: c2i(d[0:1]))
    INT16        = (2, lambda d: s2i(d[0:2]))
    INT32        = (4, lambda d: i2i(d[0:4]))
    INT64        = (0, ())
    STRING       = (0, lambda d: d.hex())
    BIN          = (1, lambda d: d.hex())
    STRING_ARRAY = (0, ())
    I18STRING    = (0, lambda d: d.hex())


