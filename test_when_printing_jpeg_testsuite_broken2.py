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
        +purpose:Simple print job of Jpeg TestSuite broken2 Page from *broken2.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:broken2.jpg=746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_testsuite_broken2_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_broken2
            +guid:53975145-8e48-44de-9f64-7a6e0419c0f8
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_testsuite_broken2_then_succeeds(self):
            default = self.tray.get_default_source()
            if self.tray.is_size_supported('anycustom', default):
                self.tray.configure_tray(default, 'anycustom', 'stationery')
            elif self.tray.is_size_supported("custom", default) and self.tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"] >= 150000:
                # the size of print file should in max/min custom size of printer supported, then could set custom size
                self.tray.configure_tray(default, "custom", 'stationery')

            job_id = self.print.raw.start('746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()

            self.tray.reset_trays()

            logging.info("JPEG TestSuite broken2 Page - Print job completed successfully")
