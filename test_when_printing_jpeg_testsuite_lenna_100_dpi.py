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
        +purpose:Simple print job of Jpeg TestSuite lenna 100 dpi Page from *lenna_100_dpi.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:lenna_100_dpi.jpg=7a2e13bafa3b09a94ae8a5c92592c36f3104d8eb862dd121f505fd11262fc242
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_testsuite_lenna_100_dpi_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_lenna_100_dpi
            +guid:3e001bad-63d9-465d-8f39-8d48f171a859
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_testsuite_lenna_100_dpi_then_succeeds(self):
            self.outputsaver.operation_mode('TIFF')

            default = self.tray.get_default_source()
            default_size = self.tray.get_default_size(default)

            if self.tray.is_size_supported('anycustom', default):
                self.tray.configure_tray(default, "anycustom", 'stationery')

            else:
                self.tray.configure_tray(default, 'custom', 'stationery')

            job_id = self.print.raw.start('7a2e13bafa3b09a94ae8a5c92592c36f3104d8eb862dd121f505fd11262fc242', timeout=300)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()
            self.outputsaver.operation_mode('NONE')
            self.tray.reset_trays()

            logging.info("JPEG TestSuite lenna 100 dpi Page - Print job completed successfully")
