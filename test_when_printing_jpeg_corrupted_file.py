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
        +purpose: Simple Print job of Jpeg file of 1MB from **
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:DatastreamCorrupted.JPG=8569b17b86977b3f02e3c5194d6436df02662bc5724f929f007a1a4626a9f122
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_corrupted_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_corrupted_file
            +guid:5ae70a25-db13-4b65-bb7c-144ff7550b17
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
    def test_when_using_corrupted_file_then_succeeds(self):
            job_id = self.print.raw.start('8569b17b86977b3f02e3c5194d6436df02662bc5724f929f007a1a4626a9f122', expected_job_state='FAILED')
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()
            self.outputsaver.clear_output()
            logging.info("Jpeg corrupted file")
