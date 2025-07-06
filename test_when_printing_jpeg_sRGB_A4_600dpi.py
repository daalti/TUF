from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
import logging

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
        +purpose:Simple print job of jpeg_sRGB_A4_600dpi
        +test_tier:1
        +is_manual:True
        +reqid:DUNE-18107
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:sRGB_A4_600dpi.jpg=86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_sRGB_A4_600dpi_then_succeeds
        +test:
            +title:test_jpeg_sRGB_A4_600dpi
            +guid:3a68798d-0c81-49dc-a406-ded51389d2a1
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_sRGB_A4_600dpi_then_succeeds(self):
            self.outputsaver.operation_mode('TIFF')

            default = self.tray.get_default_source()
            if self.tray.is_size_supported('anycustom', default):
                self.tray.configure_tray(default, 'anycustom', 'stationery')
            else:
                self.tray.configure_tray(default, 'custom', 'stationery')

            job_id = self.print.raw.start('86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b', timeout=300)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()
            self.outputsaver.operation_mode('NONE')
            self.tray.reset_trays()

            logging.info("Jpeg sRGB_A4_600dpi- Print job completed successfully")
