
from schematics.models import Model
from schematics.types import ModelType, BooleanType, StringType, ListType, DictType


class Template(Model):

    # source jinja2 template name
    src = StringType(required=True)

    # output filename (relative to outdir)
    dst = StringType(default=None)


class Config(Model):
    '''
        Used to validate the batch configuration file
    '''

    # Input C/C++ header files to parse
    headers = ListType(StringType, required=True)

    templates = ListType(ModelType(Template), required=True)

    # Input custom hooks
    hooks = StringType()

    #: YAML file to load with variables
    data = StringType()

    #: Variables to pass to the template
    vars = DictType(StringType, default={})

    #: For macros or other nonsense, these will
    #: be added to CppHeaderParser's ignore list
    ignore_symbols = ListType(StringType)

    #: Enable preprocessing of the file
    preprocess = BooleanType()

    #: Include directories (relative to root) to use for preprocessing
    pp_include_paths = ListType(StringType)


