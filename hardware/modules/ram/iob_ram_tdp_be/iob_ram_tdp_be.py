import os
import shutil

from iob_module import iob_module
from iob_ram_tdp import iob_ram_tdp


class iob_ram_tdp_be(iob_module):
    name = "iob_ram_tdp_be"
    version = "V0.10"
    setup_dir = os.path.dirname(__file__)

    @classmethod
    def _run_setup(cls):
        out_dir = super()._run_setup()
        # Copy source to build directory
        shutil.copyfile(
            os.path.join(cls.setup_dir, "iob_ram_tdp_be.v"),
            os.path.join(cls.build_dir, out_dir, "iob_ram_tdp_be.v"),
        )

        # Ensure sources of other purposes are deleted (except software)
        # Check that latest purpose is hardware
        if cls._setup_purpose[-1]=='hardware' and len(cls._setup_purpose)>1:
            # Purposes that have been setup previously
            for purpose in [x for x in cls._setup_purpose[:-1] if x!="software"]:
                # Delete sources for this purpose
                os.remove(os.path.join(cls.build_dir, cls.PURPOSE_DIRS[purpose], "iob_ram_tdp_be.v"))

        # Setup dependencies

        iob_ram_tdp.setup()
