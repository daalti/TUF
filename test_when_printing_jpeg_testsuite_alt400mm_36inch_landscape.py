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
        +purpose:Simple print job of Jpeg TestSuite alt400mm 36inch landscape Page from *alt400mm_36inch_landscape.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:200
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:alt400mm_36inch_landscape.jpg=8cb2e40ad94a931c43c9c6253ef7f367aa54cabf7b96a09a581c5b621fd00902
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_testsuite_alt400mm_36inch_landscape_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_alt400mm_36inch_landscape
            +guid:5a447aac-a2c5-40d4-8a68-d30bbbd57419
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
    

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator
    

    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_testsuite_alt400mm_36inch_landscape_then_succeeds(self):
            self.outputsaver.validate_crc_tiff(self.udw)

            job_id = self.print.raw.start('8cb2e40ad94a931c43c9c6253ef7f367aa54cabf7b96a09a581c5b621fd00902', timeout=180)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()
            self.outputsaver.operation_mode('NONE')
            logging.info("Get crc value for the current print job")
            Current_crc_value = self.outputsaver.get_crc()
            logging.info("Validate current crc with master crc")
            assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

            logging.info("JPEG TestSuite alt400mm 36inch landscape Page - Print job completed successfully")
