from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
import logging
from dunetuf.utility.systemtestpath import get_system_test_binaries_path

class TestWhenPrintingJPEGFile():
    @classmethod
    def setup_class(cls):
        cls.job_queue = JobQueue()
        cls.job_history = JobHistory()
        cls.print = Print()

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self):
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        #TODO: Create job_history methods in Ares
        #self.job_history.clear()
        #self.job_history.wait_for_history_empty()

    def teardown_method(self):
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        #TODO: Create job_history methods in Ares
        #self.job_history.clear()
        #self.job_history.wait_for_history_empty()

    """

    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: Print job file *sRGB_A4_600dpi.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:sRGB_A4_600dpi.jpg=86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_sRGB_A4_600dpi_checksum_then_succeeds
        +test:
            +title:test_jpg_sRGB_A4_600dpi_checksum
            +guid:3a942ee5-f517-4493-9bc1-9a4f0a2dc1c0
            +dut:
                +type:Simulator, Emulator
                +configuration:PrintEngineType=Maia & DocumentFormat=JPEG
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_sRGB_A4_600dpi_checksum_then_succeeds(self):

            # CRC will be calculated using the payload of all the RasterDatas
            self.outputsaver.operation_mode('CRC')

            job_id = self.print.raw.start('86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b', timeout=300)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            logging.info("basic file sRGB_A4_600dpi.jpg - Print job completed successfully")

            expected_crc = ["0x35d1f2ef"]

            # Read and verify that obtained checksums are the expected ones
            self.outputsaver.save_output()
            self.outputsaver.verify_output_crc(expected_crc)
            logging.info("basic file sRGB_A4_600dpi.jpg - Checksum(s) verified successfully")
