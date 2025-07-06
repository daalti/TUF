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
        +purpose:Simple print job of Jpeg Performance of 10_2000cm Page from *10_2000cm.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:360
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:10_2000cm.jpg=c99290a709203b35b2e7c8520e9764b1648ec79354af4bddfa7aa14b52848dad
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_performance_10_2000cm_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_performance_10_2000cm
            +guid:e74d7487-1394-4f89-9dd5-0241be6577d3
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=Letter
    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_performance_10_2000cm_then_succeeds(self):

            # Not using print_verify for a reason
            # We want to handle media mismatch alert on design products before job completion
            jobid = printjob.start_print('c99290a709203b35b2e7c8520e9764b1648ec79354af4bddfa7aa14b52848dad')

            # This jpeg job has large dimensions
            # On non-multiroll products, it will print on Letter
            if 'roll-1' in self.tray.trays:
                # On multi-roll, it will print on roll-1 after out of range media check clipping target size leading to a prompt
                # required rendering time will be bigger
                self.media.wait_for_alerts('mediaMismatchSizeFlow', 300)
                self.media.alert_action("mediaMismatchSizeFlow", "continue")

            # for non design products total test timeout will be 240
            # for design 300
            printjob.wait_verify_job_completion(jobid, timeout=240)

            logging.info("JPEG Performance 10_2000cm Page - Print job completed successfully")
