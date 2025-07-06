from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType

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
        +purpose:Simple print job of Jpeg TestSuite lenna without resolution info EXIFNONE Page from *lenna_without_resolution_info_EXIF_NONE.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:420
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:lenna_without_resolution_info_EXIF_NONE.jpg=0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_testsuite_lenna_without_resolution_info_EXIF_NONE_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_lenna_without_resolution_info_EXIF_NONE
            +guid:31967c5b-1079-44c7-bca8-7c7a81066791
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_testsuite_lenna_without_resolution_info_EXIF_NONE_then_succeeds(self):
            self.outputsaver.validate_crc_tiff(self.udw)
            default = self.tray.get_default_source()
            if self.tray.is_size_supported('anycustom', default):
                self.tray.configure_tray(default, "anycustom", 'stationery')
            elif self.tray.is_size_supported('any', default):
                tray_test_name = self.print_mapper.get_media_input_test_name(default)
                self.print_emulation.tray.setup_tray(tray_test_name, MediaSize.Letter.name, MediaType.Plain.name)
                self.tray.configure_tray(default, 'any', 'any')
            else:
                self.tray.configure_tray(default, 'custom', 'stationery')

            job_id = self.print.raw.start('0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19',timeout=420)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()
            self.tray.reset_trays()
            Current_crc_value = self.outputsaver.get_crc()
            logging.info("Validate current crc with master crc")
            assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

            logging.info("JPEG TestSuite lenna without resolution info EXIF NONE Page - Print job completed successfully")
