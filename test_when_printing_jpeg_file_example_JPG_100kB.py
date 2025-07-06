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
        +purpose:Simple print job of Jpeg file of 100kB from *file_example_JPG_100kB.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:360
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:file_example_JPG_100kB.jpg=88aeb1f4467bd1e50cf624de972fbf3f40801632fedb64aaa7b1a8a9ef786fc6
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_file_example_JPG_100kB_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_file_example_JPG_100kB
            +guid:6bcdc78d-42b7-446c-950d-162c8fe43572
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_file_example_JPG_100kB_then_succeeds(self):
            self.outputsaver.validate_crc_tiff(self.udw)
            default = self.tray.get_default_source()
            media_width_maximum = self.tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
            media_length_maximum = self.tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
            media_width_minimum = self.tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
            media_length_minimum = self.tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
            if self.tray.is_size_supported('anycustom', default):
                self.tray.configure_tray(default, 'anycustom', 'stationery')
            elif self.tray.is_size_supported('custom', default) and media_width_maximum > 85000 and media_length_maximum >= 110000 and media_width_minimum < 85000 and media_length_minimum <= 110000:
                self.tray.configure_tray(default, 'custom', 'stationery')
            elif self.tray.is_size_supported('na_letter_8.5x11in', default):
                self.tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

            job_id = self.print.raw.start('88aeb1f4467bd1e50cf624de972fbf3f40801632fedb64aaa7b1a8a9ef786fc6', timeout=360)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()
            self.tray.reset_trays()
            Current_crc_value = self.outputsaver.get_crc()
            logging.info("Validate current crc with master crc")
            assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

            logging.info("Jpeg file example JPG 100kB Page - Print job completed successfully")
