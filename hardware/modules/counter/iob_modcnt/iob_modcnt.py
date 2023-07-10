import os
import shutil

from iob_module import iob_module
from setup import setup

from iob_counter import iob_counter


class iob_modcnt(iob_module):
    name = "iob_modcnt"
    version = "V0.10"
    flows = "sim"
    setup_dir = os.path.dirname(__file__)

    @classmethod
    def _run_setup(cls):
        super()._run_setup()

        # Setup dependencies

        iob_modcnt.setup()
        iob_counter.setup()

        # Setup flows of this core using LIB setup function
        setup(cls, disable_file_gen=True)
