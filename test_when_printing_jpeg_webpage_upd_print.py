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
        +purpose:Jpeg test using **Webpage_UPD_PRint.JPG
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Webpage_UPD_PRint.JPG=a89ef72d5101dabbf55a0722d57141626372518bfd7fa6b3ba53808ba7d1e0f5
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_webpage_upd_print_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_webpage_upd_print
            +guid:9879404e-8d7e-4072-b20a-085d2e7c1852
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_webpage_upd_print_then_succeeds(self):
            job_id = self.print.raw.start('a89ef72d5101dabbf55a0722d57141626372518bfd7fa6b3ba53808ba7d1e0f5')
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()
