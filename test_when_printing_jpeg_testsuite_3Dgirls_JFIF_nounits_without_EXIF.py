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
        +purpose:Simple print job of Jpeg TestSuite 3Dgirls JFIF nounits without EXIF Page from *3Dgirls_JFIF_nounits_without_EXIF.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:3Dgirls_JFIF_nounits_without_EXIF.jpg=07010aa839653b2355047c770f6f3631997e0e9172537141d42d185c34f39a1d
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_testsuite_3Dgirls_JFIF_nounits_without_EXIF_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_3Dgirls_JFIF_nounits_without_EXIF
            +guid:fa33d931-c7b3-420c-ba1c-d6e3f3b327ce
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_testsuite_3Dgirls_JFIF_nounits_without_EXIF_then_succeeds(self):
            job_id = self.print.raw.start('07010aa839653b2355047c770f6f3631997e0e9172537141d42d185c34f39a1d')
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()

            logging.info("JPEG TestSuite 3Dgirls JFIF nounits without EXIF Page - Print job completed successfully")
