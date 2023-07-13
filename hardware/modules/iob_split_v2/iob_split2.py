import os

from iob_module import iob_module

from iob_reg import iob_reg
from iob_mux import iob_mux
from iob_demux import iob_demux


class iob_split2(iob_module):
    name = "iob_split2"
    version = "V0.10"
    flows = "sim"
    setup_dir = os.path.dirname(__file__)

    @classmethod
    def _create_submodules_list(cls):
        """Create submodules list with dependencies of this module"""
        super()._create_submodules_list(
            [
                "clk_en_rst_portmap",
                "clk_en_rst_port",
                iob_reg,
                iob_mux,
                iob_demux,
            ]
        )
