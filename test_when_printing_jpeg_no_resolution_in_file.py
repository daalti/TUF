from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

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
        +purpose:Test jpeg job when no resolution in specified in file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-215024
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:road_nores.jpeg=116ef2798a4d195fd1e3ea20d81af3b8c20373587e119d10a6ff0f0d70ee6f86
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_no_resolution_in_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_no_resolution_in_file
            +guid:ea4d4400-4e5e-48a5-b30b-210e575a7ca3
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & EngineFirmwareFamily=DoX & PrintResolution=Print300
    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_no_resolution_in_file_then_succeeds(self):
            self.tray.reset_trays()
            default_tray = self.tray.get_default_source()
            if self.tray.is_size_supported('custom', default_tray):
                self.tray.configure_tray(default_tray, 'custom', 'stationery')

            self.outputsaver.validate_crc_tiff(self.udw)

            job_id = self.print.raw.start('116ef2798a4d195fd1e3ea20d81af3b8c20373587e119d10a6ff0f0d70ee6f86', 'SUCCESS', 300, 1)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputverifier.save_and_parse_output()
            logging.info("Get crc value for the current print job")
            Current_crc_value = self.outputsaver.get_crc()
            logging.info("Validate current crc with master crc")
            assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

            self.outputverifier.verify_resolution(Intents.printintent, 600)
            self.outputverifier.verify_page_width(Intents.printintent, 3000)
            self.outputverifier.verify_page_height(Intents.printintent, 3749)
            self.outputsaver.operation_mode('NONE')
            self.tray.reset_trays()
