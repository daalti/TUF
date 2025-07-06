from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.localization.LocalizationHelper import LocalizationHelper

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
        +purpose:Test print multiple jobs
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-6717
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ProductQA
        +test_framework:TUF
        +external_files:lenna_without_resolution_info_EXIF_NONE.jpg=0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_print_multiple_jobs_then_succeeds
        +test:
            +title:test_jpeg_print_multiple_jobs
            +guid:b5ce7f6f-5f5a-4893-9141-65ff8db2aeae
            +dut:
                +type:Simulator, Emulator
                +configuration:DocumentFormat=JPEG & PrintEngineType=Maia
    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_print_multiple_jobs_then_succeeds(self):

            # Go to Job Queue App screen
            self.spice.cleanSystemEventAndWaitHomeScreen()
            self.spice.main_app.get_home()
            self.spice.main_app.goto_job_queue_app()

            # Send job to print
            printjob.start_print('0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19')

            # Get last job in queue by CDM
            queue = self.job.get_job_queue()
            first_job_id = queue[-1]["jobId"]

            # Send job to print
            printjob.start_print('0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19')

            # Get last job in queue by CDM
            queue = self.job.get_job_queue()
            second_job_id = queue[-1]["jobId"]

            # Send job to print
            printjob.start_print('0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19')

            # Get last job in queue by CDM
            queue = self.job.get_job_queue()
            third_job_id = queue[-1]["jobId"]

            #Wait for first job completion
            self.job.wait_for_job_completion_cdm(first_job_id)
            self.spice.job_ui.goto_job(first_job_id)
            assert self.spice.job_ui.recover_job_status() == LocalizationHelper.get_string_translation(self.net,"cJobStateTypeCompleted", self.locale)

            #Wait for second job completion
            self.job.wait_for_job_completion_cdm(second_job_id)
            self.spice.job_ui.goto_job(second_job_id)
            assert self.spice.job_ui.recover_job_status() == LocalizationHelper.get_string_translation(self.net,"cJobStateTypeCompleted", self.locale)

            #Wait for third job completion
            self.job.wait_for_job_completion_cdm(third_job_id)
            self.spice.job_ui.goto_job(third_job_id)
            assert self.spice.job_ui.recover_job_status() == LocalizationHelper.get_string_translation(self.net,"cJobStateTypeCompleted", self.locale)

            # Go to homescreen
            self.spice.goto_homescreen()
