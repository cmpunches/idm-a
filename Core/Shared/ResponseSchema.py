from enum import Enum, auto
import json


def is_serializable( obj ):
    try:
        json.dumps( obj )
        return True
    # fuck PEP8
    except:
        return False


class STATUS(Enum):
    SUCCESS         = auto()
    DATA_CONFLICT   = auto()
    DATA_STRUCTURE  = auto()
    FAILURE         = auto()


class EResp:
    def __init__( self, status, message, attachment=None ):
        self.status = status
        self.message = message

        if attachment is not None:
            self.attachment = attachment
        else:
            self.attachment = "NULL"

    def to_json(self):
        serialized_self = dict()
        serialized_self['status'] = self.status.name
        serialized_self['message'] = self.message
        if self.attachment != "NULL" and is_serializable( self.attachment ):
            serialized_self['attachment'] = json.loads( self.attachment )
        else:
            serialized_self['attachment'] = None

        return serialized_self

    def __repr__(self):
        return json.dumps( self.to_json(), indent=4, sort_keys=True )

    def __str__(self):
        return json.dumps( self.to_json(), indent=4, sort_keys=True )