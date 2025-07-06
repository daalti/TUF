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
        +purpose:Simple print job of Jpeg Regression of AdobeRGB A4 100dpi Page from *AdobeRGB_A4_100dpi.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:200
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:AdobeRGB_A4_100dpi.jpg=acc8383b0992e875904aa4c196a4f0ef47ba8e0bfdd0914159876e64f79d2700
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_regression_AdobeRGB_A4_100dpi_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_regression_AdobeRGB_A4_100dpi
            +guid:d059ea34-de28-4e32-bf36-be98412358c0
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_regression_AdobeRGB_A4_100dpi_then_succeeds(self):
            if self.outputsaver.configuration.productname == "jupiter":
                self.outputsaver.operation_mode('CRC')
            else:
                self.outputsaver.operation_mode('TIFF')
                self.outputsaver.validate_crc_tiff(self.udw)

            default = self.tray.get_default_source()
            default_size = self.tray.get_default_size(default)

            if self.tray.is_size_supported('anycustom', default):
                self.tray.configure_tray(default, "anycustom", 'stationery')

            else:
                self.tray.configure_tray(default, 'custom', 'stationery')

            job_id = self.print.raw.start('acc8383b0992e875904aa4c196a4f0ef47ba8e0bfdd0914159876e64f79d2700', timeout=180)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])

            self.outputsaver.save_output()
            if self.outputsaver.configuration.productname == "jupiter":
                expected_crc = ["0x9350fdc4"]
                self.outputsaver.verify_output_crc(expected_crc)
            else:
                Current_crc_value = self.outputsaver.get_crc()
                logging.info("Validate current crc with master crc")
                assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

            self.outputsaver.operation_mode('NONE')
            self.tray.reset_trays()

            logging.info("JPEG Regression AdobeRGB A4 100dpi Page - Print job completed successfully")
