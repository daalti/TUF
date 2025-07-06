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
        +purpose:Simple print job of Jpeg TestSuite lenna 100 dpi EXIF NONE Page from *lenna_100_dpi_EXIF_NONE.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:200
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:lenna_100_dpi_EXIF_NONE.jpg=cc7efdcc505cf95c913aeafa9886ad5a4f2c31b4afefd35d9c9f5fd60f4368d3
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_testsuite_lenna_100_dpi_EXIF_NONE_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_lenna_100_dpi_EXIF_NONE
            +guid:0157a414-3f03-4b85-b754-6cd221bbf7f5
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
        +overrides:
            +Home:
                +is_manual:False
                +timeout:240
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_testsuite_lenna_100_dpi_EXIF_NONE_then_succeeds(self):
            self.outputsaver.validate_crc_tiff(self.udw)
            default = self.tray.get_default_source()
            default_size = self.tray.get_default_size(default)

            if self.tray.is_size_supported('anycustom', default):
                self.tray.configure_tray(default, "anycustom", 'stationery')

            else:
                self.tray.configure_tray(default, 'custom', 'stationery')

            job_id = self.print.raw.start('cc7efdcc505cf95c913aeafa9886ad5a4f2c31b4afefd35d9c9f5fd60f4368d3', timeout=180)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()
            logging.info("Get crc value for the current print job")
            Current_crc_value = self.outputsaver.get_crc()
            logging.info("Validate current crc with master crc")
            assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
            self.tray.reset_trays()

            logging.info("JPEG TestSuite lenna 100 dpi EXIF NONE Page - Print job completed successfully")
