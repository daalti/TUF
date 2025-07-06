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
        +purpose:Simple print job of Jpeg TestSuite lenna 20dpcm EXIF NONE Page from *lenna_20dpcm_EXIF_NONE.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:200
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:lenna_20dpcm_EXIF_NONE.jpg=cb6e516bebfbd46c2e719ebb1bb3c7f4d49cefb80977a40cc167073712f7ba24
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_testsuite_lenna_20dpcm_EXIF_NONE_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_lenna_20dpcm_EXIF_NONE
            +guid:df7798fe-450e-4268-96b3-54f581d20db3
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_testsuite_lenna_20dpcm_EXIF_NONE_then_succeeds(self):
            default = self.tray.get_default_source()
            default_size = self.tray.get_default_size(default)

            if self.tray.is_size_supported(default_size, default):
                logging.info(f"Set paper tray <{default}> to paper size <{default_size}>")
                self.tray.configure_tray(default, default_size, 'stationery')

            job_id = self.print.raw.start('cb6e516bebfbd46c2e719ebb1bb3c7f4d49cefb80977a40cc167073712f7ba24', timeout=180)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()
            self.tray.reset_trays()

            logging.info("JPEG TestSuite lenna 20dpcm EXIF NONE Page - Print job completed successfully")
